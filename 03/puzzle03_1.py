"""Day 3: Gear Ratios (https://adventofcode.com/2023/day/3)
Code for solving part one.
"""

import re


def find_part_numbers(path: str) -> int:
    """Get the sum of all part numbers.
    A number is a part number if it is adjacent (even diagonal) to a symbol.

    Arguments:
        - path: path to input.

    Returns:
        The sum of part numbers.
    """
    with open(path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    part_numbers = []
    for i, line in enumerate(lines):
        for number in re.finditer(r"\d+", line):
            start, end = number.span()
            # this is stupid and inefficient; can't be bothered to improve it
            adjacent = ""
            if i > 0:
                adjacent += lines[i-1][start:end]
                if start > 0:
                    adjacent += lines[i-1][start-1]
                if end < len(line):
                    adjacent += lines[i-1][end]
            if i < len(lines) - 1:
                adjacent += lines[i+1][start:end]
                if start > 0:
                    adjacent += lines[i+1][start-1]
                if end < len(line):
                    adjacent += lines[i+1][end]
            if start > 0:
                adjacent += line[start-1]
            if end < len(line):
                adjacent += line[end]
            if re.search(r"(\&|\=|\*|\$|\+|\#|\@|\-|\/|\%)", adjacent):
                part_numbers.append(int(number.group()))
    return sum(part_numbers)


if __name__ == "__main__":
    print("example:", find_part_numbers("03/example03_1.txt"))
    print("input:", find_part_numbers("03/input03.txt"))
