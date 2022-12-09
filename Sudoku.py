import random
import math
import os

CLEAR = 'clear' if os.name == 'posix' else 'cls'

def generate_0_grid():
    """Return 9x9 zero filled grid"""
    grid = []
    for r in range(9):
        grid.append([])
        for c in range(9):
            grid[r].append(0)
    return grid


def copy_grid(a):
    """Return the copy of grid a"""
    copygrid = []
    for r in range(9):
        copygrid.append([])
        for c in range(9):
            copygrid[r].append(a[r][c])
    return copygrid

def is_valid_grid(a, b):
    """Return True if grid a is equal to grid b, else return False"""
    for r in range(9):
        for c in range(9):
            if a[r][c] != b[r][c]:
                return False
    return True

class Sudoku:
    def __init__(self):
        self.grid = generate_0_grid()
        self.valid_grid = generate_0_grid()
        # to convert alpha to index and index to alpha for row
        self.row_d = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7,
            "I": 8,
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
            8: "I",
        }
        # to store removed elements from the valid grid
        self.removed = {}
    
    def clear(self):
        """Clear terminal"""
        os.system(CLEAR)

    def get_num(self, pos):
        row = self.row_d[pos[0]]
        col = int(pos[1]) - 1
        return self.grid[row][col]

    def set_num(self, pos, num):
        """Update num value in specified position in grid"""
        row = self.row_d[pos[0]]
        col = int(pos[1]) - 1
        self.grid[row][col] = num
    
    def print_fillable(self):
        """Print position that can be filled"""
        nrow = math.ceil(len(self.removed) // 5)
        keys = list(self.removed)
        i = 0
        for row in range(nrow):
            for col in range(5):
                try:
                    print(keys[i],"=",self.removed[keys[i]], end="\t")
                    i += 1
                except:
                    pass
            print()

    def is_not_complete(self, l=[0,0]):
        """Return True is the grid is not complete, else return False"""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    l[0] = row
                    l[1] = col
                    return True
        return False

    def is_sat(self, row, col, num):
        """Return True if all condition is satisfiable, else return False"""
        # check in a row
        for r in range(9):
            if r == row:
                continue
            if self.grid[r][col] == num:
                return False

        # check in a column
        for c in range(9):
            if c == col:
                continue
            elif self.grid[row][c] == num:
                return False

        # check in a box 3x3
        brow = row - row % 3
        bcol = col - col % 3
        for r in range(3):
            for c in range(3):
                if self.grid[r+brow][c+bcol] == num:
                    return False
        return True


    def display_grid(self):
        """Print the grid"""
        # y axis
        print("  1 2 3   4 5 6   7 8 9")
        for i in range(0, 3):
            print(self.row_d[i], end=" ")
            print(
                " | ".join(
                    [
                        " ".join(str(x) for x in self.grid[i][j : j + 3]).replace('0', '-')
                        for j in range(0, 9, 3)
                    ]
                )
            )
        print("  ------+-------+------")
        for i in range(3, 6):
            print(self.row_d[i], end=" ")
            print(
                " | ".join(
                    [
                        " ".join(str(x) for x in self.grid[i][j : j + 3]).replace('0', '-')
                        for j in range(0, 9, 3)
                    ]
                )
            )
        print("  ------+-------+------")
        for i in range(6, 9):
            print(self.row_d[i], end=" ")
            print(
                " | ".join(
                    [
                        " ".join(str(x) for x in self.grid[i][j : j + 3]).replace('0', '-')
                        for j in range(0, 9, 3)
                    ]
                )
            )

    def generate_grid(self):
        """Generate the valid grid"""

        # 'l' is a list variable that keeps the
        # record of row and col in
        # is_not_complete() function
        l = [0, 0]

        # If there is no unassigned
        # location, we are done
        if not self.is_not_complete(l):
            return True

        # Assigning list values to row and col
        # that we got from the above Function
        row = l[0]
        col = l[1]

        # consider digits 1 to 9
        nums = list(range(1,10))
        # random the digits
        random.shuffle(nums)
        for num in nums:

            # if all condition is satisfiable
            if self.is_sat(row, col, num):

                # make tentative assignment
                self.grid[row][col] = num

                # recursive, return True if success
                if self.generate_grid():
                    return True

                # failure, backtrack, restore the value, and try again
                self.grid[row][col] = 0

        # this triggers backtracking
        return False

    def create(self):
        """Create the Sudoku challenge grid"""
        self.generate_grid() # generate the valid grid to self.grid
        self.valid_grid = copy_grid(self.grid) # store the valid grid self.valid_grid
        difficulty = 30 # max removed value

        # removing the value from grid
        while difficulty > 0:
            # randomly pick row and col
            row = random.randint(0,8)
            col = random.randint(0,8)

            # ignore and try again if the value already 0
            if self.grid[row][col] == 0:
                continue

            # convert to string type position ([0,0] to A1, [1,0] to B1, etc)
            pos = self.row_d[row] + str(col+1)
            # store the removed position to self.removed dictionary
            self.removed[pos] = 0

            # store the previous value to temp
            temp = self.grid[row][col]

            # remove the value
            self.grid[row][col] = 0

            # copy the grid
            copygrid = copy_grid(self.grid)

            # try to solve the grid
            self.generate_grid()

            # if the grid is not valid (not equal to the valid_grid), then backtrack
            if not is_valid_grid(self.grid, self.valid_grid):
                # restore the value
                copygrid[row][col] = temp
                # remove the pos from self.removed dictionary
                del self.removed[pos]

            difficulty -= 1

            # restore the grid to the previous state
            self.grid = copy_grid(copygrid)

    def title(self):
        """Print the title"""
        print("       SUDOKU v0.1\n")

    def play(self):
        """Starts the game"""
        err = False
        sat = True
        prev = None
        # initiate the game
        self.create()
        self.removed = dict(sorted(self.removed.items()))
        while True:
            self.clear()
            self.title()
            self.display_grid()
            print()
            if is_valid_grid(self.grid, self.valid_grid):
                print("Congratz, You won!")
                break
            self.print_fillable()
            print()

            print("[XY n] fill n in XY", end='\t')
            print("[r] restart", end='\t')
            print("[q] quit\n")
            try:
                if prev:
                    print("Previous input :", prev)
                if err:
                    print("Invalid input")
                    err = False
                if not sat:
                    print("Not satisfiable")
                    sat = True
                x = input("[>] : ").upper()
                prev = x
                if x == 'Q':
                    print("Good bye.")
                    break
                elif x == 'R':
                    self.__init__()
                    self.create()
                    self.removed = dict(sorted(self.removed.items()))
                    continue
                x = x.split()
                pos = x[0]
                row = self.row_d[pos[0]]
                col = int(pos[1]) - 1
                n = int(x[1])
                if pos not in list(self.removed) or pos[0] not in list(self.row_d) or int(pos[1]) < 1 or int(pos[1]) > 9 or n < 0 or n > 9:
                    err = True
                    continue

                # check if it is not satisfiable, then ignore it
                if not self.is_sat(row, col, n):
                    sat = False
                    continue

                # change the value
                self.set_num(pos, n)
                # update the value in self.removed dictionary
                self.removed[pos] = n

                # check if the grid is already equal to the valid_grid, then the game is finished

            except Exception as e:
                err = True
