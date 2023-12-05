"""Day 4: Scratchcards (https://adventofcode.com/2023/day/4)
Code for solving part one.
"""

import re


def get_points(path: str) -> int:
    """Get sum of points of the scratch cards. A scratchcard consists of
    winning numbers and other numbers. The first match gives one point and
    every match after that doubles the points.

    Arguments:
        - path: path to input.

    Returns:
        - The sum of points.
    """
    with open(path, "r", encoding="utf-8") as file:
        cards = file.readlines()
    sum_points = 0
    for card in cards:
        card = card.split(": ")[1].strip()
        winning, numbers = card.split(" | ")
        # not necessary, but I don't want to filter that differently
        winning = sorted(map(int, re.findall(r"\d+", winning)))
        numbers = sorted(map(int, re.findall(r"\d+", numbers)))
        points = 0
        for win_num in winning:
            if win_num in numbers:
                if points == 0:
                    points += 1
                else:
                    points *= 2
            else:
                continue
        sum_points += points
    return sum_points


if __name__ == "__main__":
    print("example:", get_points("04/example04_1.txt"))
    print("input:", get_points("04/input04.txt"))
