#!/usr/bin/env python3
from Sudoku import Sudoku


def main():
    game = Sudoku()
    game.create()
    game.display()
    return 0


if __name__ == "__main__":
    main()
