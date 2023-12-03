"""Day 2: Cube Conundrum (https://adventofcode.com/2023/day/2#part2)
Code for solving part two.
"""


def get_fewest_number(path: str) -> int:
    """Get the sum of the powers of the games.
    The power is the minimum amount of cubes multiplied.

    Arguments:
        - path: path to input.

    Returns:
        The sum of powers.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    games: dict[int, list[int]] = {}
    for line in lines:
        game_id, sets = line.removeprefix("Game ").strip().split(": ")
        sets = [set_.split(", ") for set_ in sets.split(";")]
        games.update({int(game_id): []})
        max_amount = [0, 0, 0]
        for set_ in sets:
            for cubes in set_:
                amount, colour = cubes.strip().split(" ")
                amount = int(amount)
                index = {"red": 0, "green": 1, "blue": 2}[colour]
                if amount > max_amount[index]:
                    max_amount[index] = amount
            games[int(game_id)] = max_amount
    return sum([r * g * b for r, g, b in games.values()])


if __name__ == "__main__":
    print("example:", get_fewest_number("02/example02_2.txt"))
    print("input:", get_fewest_number("02/input02.txt"))
