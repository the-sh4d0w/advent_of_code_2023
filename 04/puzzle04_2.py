"""Day 4: Scratchcards (https://adventofcode.com/2023/day/4#part2)
Code for solving part two.
"""

import re


def get_scratchcard_amount(path: str) -> int:
    """Get the amount of scratchcards. A scratchcard is added for number of
    matching numbers. The added scratchcards are copies of the following
    cards.

    Arguments:
        - path: path to input.

    Returns:
        Amount of scratchcards.
    """
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    cards: dict[int, tuple[list[int], list[int]]] = {}
    for line in lines:
        card_id, card = line.strip().removeprefix("Card ").split(": ")
        card_id = int(card_id)
        winning, numbers = card.split(" | ")
        winning = list(map(int, re.findall(r"\d+", winning)))
        numbers = list(map(int, re.findall(r"\d+", numbers)))
        cards.update({card_id: (winning, numbers)})
    cards_amount: dict[int, int] = {card_id: 1 for card_id in cards}
    for card_id, card in cards.items():
        i = card_id + 1
        for win_num in card[0]:
            if win_num in card[1]:
                cards_amount[i] += cards_amount[card_id]
                i += 1
    return sum(cards_amount.values())


if __name__ == "__main__":
    print("example:", get_scratchcard_amount("04/example04_2.txt"))
    print("input:", get_scratchcard_amount("04/input04.txt"))
