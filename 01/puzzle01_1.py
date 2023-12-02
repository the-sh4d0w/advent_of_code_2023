"""Day 1: Trebuchet?! (https://adventofcode.com/2023/day/1)
Code for solving part one.
"""


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
        first = -1
        last = -1
        for char in line:
            if char.isdigit():
                if first < 0:
                    first = int(char)
                last = int(char)
        values.append(first * 10 + last)
    return sum(values)


if __name__ == "__main__":
    print("example:", find_calibration_values("01/example01_1.txt"))
    print("input:", find_calibration_values("01/input01.txt"))
