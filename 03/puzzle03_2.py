"""Day 3: Gear Ratios (https://adventofcode.com/2023/day/3#part2)
Code for solving part two.
"""

import re


def get_coords(matrix: list[str], a: int, b: int, c: int, d: int) \
        -> tuple[int, int]:
    """Select an area of the matrix. A matrix is a list of string, where all
    the strings are the same length. Check if a gear exists and return its
    location.

    Arguments:
        - matrix: list of strings.
        - a: top left x.
        - b: top left y.
        - c: bottom right x.
        - d: bottom right y.

    Returns:
        The coordinates of the gear, False if there is no gear.
    """
    area: list[str] = []
    a = a if a > 0 else 0
    b = b if b > 0 else 0
    c = c + 1 if c + 1 < len(matrix) else len(matrix) - 1
    d = d + 1 if d + 1 < len(matrix) else len(matrix) - 1
    for i in range(b, d):
        area.append(matrix[i][a:c])
    x, y = a, b
    for line in area:
        if "*" in line:
            x += line.index("*")
            return (x, y)
        y += 1
    return (-1, -1)


def get_gear_ratio(path: str) -> int:
    """Get the gear ratio. A gear is a * with two numbers adjacent.
    The gear ratio is both numbers multiplied together.

    Arguments:
        - path: path to input.

    Returns:
        The sum of all gear ratios.
    """
    with open(path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    gear_ratios: dict[tuple[int, int], list[int]] = {}
    for i, line in enumerate(lines):
        for number in re.finditer(r"\d+", line):
            start, end = number.span()
            coords = get_coords(lines, start - 1, i - 1, end, i + 1)
            if coords != (-1, -1):
                if gear_ratios.get(coords) is None:
                    gear_ratios[coords] = []
                gear_ratios[coords].append(int(number.group()))
    gear_ratio_sum = 0
    for nums in gear_ratios.values():
        if len(nums) == 2:
            gear_ratio_sum += nums[0] * nums[1]
    return gear_ratio_sum


if __name__ == "__main__":
    print("example:", get_gear_ratio("03/example03_2.txt"))
    print("input:", get_gear_ratio("03/input03.txt"))
