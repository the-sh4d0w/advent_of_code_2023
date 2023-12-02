"""Day 1: Trebuchet?! (https://adventofcode.com/2023/day/1#part2)
Code for solving part two.
"""

import re

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def find_calibration_values(path: str) -> int:
    """Find calibrations values (first an last value in each line)
    in the input.

    Arguments:
        - path: path to input.

    Return:
        The sum of the values.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    values = []
    for line in lines:
        found = re.findall(
            r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", line)
        found = [int(f) if f.isdigit() else NUMBERS[f] for f in found]
        values.append(found[0] * 10 + found[-1])
    return sum(values)


if __name__ == "__main__":
    print("example:", find_calibration_values("01/example01_2.txt"))
    print("input:", find_calibration_values("01/input01.txt"))
