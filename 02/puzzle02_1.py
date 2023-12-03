"""Day 2: Cube Conundrum (https://adventofcode.com/2023/day/2)
Code for solving part one."""


def get_possible_games(path: str) -> int:
    """Get the sum of the ids  od possible games.
    Possible games can't contain more than 12 red, 13 green or 14 blue cubes.

    Arguments:
        - path: path to input.

    Returns:
        The sum of ids.
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
    games = {game: amount for game, amount in games.items()
             if not (amount[0] > 12 or amount[1] > 13 or amount[2] > 14)}
    return sum(games.keys())


if __name__ == "__main__":
    print("example:", get_possible_games("02/example02_1.txt"))
    print("input:", get_possible_games("02/input02.txt"))
