import random

def generate_0_grid():
    grid = []
    for r in range(9):
        grid.append([])
        for c in range(9):
            grid[r].append(0)
    return grid


def copy_grid(a):
    copygrid = []
    for r in range(9):
        copygrid.append([])
        for c in range(9):
            copygrid[r].append(a[r][c])
    return copygrid


class Sudoku:
    def __init__(self):
        self.grid = generate_0_grid()
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
        self.counter = 0

    def get_num(self, pos):
        row = self.row_d[pos[0]]
        col = int(pos[1]) - 1
        return self.grid[row][col]

    def set_num(self, pos, num):
        row = self.row_d[pos[0]]
        col = int(pos[1]) - 1
        self.grid[row][col] = num

    def is_not_complete(self, l):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    l[0] = row
                    l[1] = col
                    return True
        return False

    def is_sat(self, row, col, num):
        # check in a row
        for r in range(9):
            if r == row:
                continue
            if self.grid[r][col] == num:
                return False

        for c in range(9):
            if c == col:
                continue
            elif self.grid[row][c] == num:
                return False

        # check in a box
        brow = row - row % 3
        bcol = col - col % 3
        for r in range(3):
            for c in range(3):
                # npos = self.row_d[r + brow] + str(c + bcol + 1)
                if self.grid[r+brow][c+bcol] == num:
                # if self.get_num(npos) == num:
                    return False
        return True


    def fill_spot(self, row, col, nums):
        random.shuffle(nums)
        for num in nums:
            if self.is_sat(row, col, num):
                self.grid[row][col] = num
                return num
        return False


    def display(self):
        print("  1 2 3   4 5 6   7 8 9")
        for i in range(0, 3):
            # print(chr(65+i), end = " ")
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

        # 'l' is a list variable that keeps the
        # record of row and col in
        # find_empty_location Function
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
        random.shuffle(nums)
        for num in nums:

            # if looks promising
            if self.is_sat(row, col, num):

                # make tentative assignment
                self.grid[row][col] = num

                # return, if success,
                # ya !
                # self.display()
                # print()
                if self.generate_grid():
                    return True

                # failure, unmake & try again
                self.grid[row][col] = 0
                self.counter += 1

        # this triggers backtracking
        return False

    def create(self):
        self.generate_grid()
        self.display()
        print()
        difficulty = 25
        counter = 1
        while difficulty > 0:
            row = random.randint(0,8)
            col = random.randint(0,8)
            while self.grid[row][col] == 0:
                row = random.randint(0,8)
                col = random.randint(0,8)

            temp = self.grid[row][col]
            self.grid[row][col] = 0
            copygrid = copy_grid(self.grid)

            self.counter = 0
            self.generate_grid()

            if self.counter > 0:
                self.grid[row][col] = temp
            difficulty -= 1

            self.grid = copy_grid(copygrid)
