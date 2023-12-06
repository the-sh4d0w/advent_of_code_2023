"""Day 5: If You Give A Seed A Fertilizer (https://adventofcode.com/2023/day/5)
Code for solving part one.
"""


def find_lowest_location_number(path: str) -> int:
    """Find the lowest corresponding location number to the given seeds.
    Mapping happens through a source start, a destination start and a range.
    A source that isn't mapped to anything maps to itself.

    Arguments:
        - path: path to input.

    Returns:
        The lowest location number.
    """
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    mappings: list[list[tuple[int, int, int]]] = []
    locations: list[int] = []
    seeds = map(int, text.removeprefix("seeds: ").split("\n")[0].split(" "))
    for i, mapping in enumerate(text.split("\n\n")[1:]):
        mappings.append([])
        values = mapping.split(" map:\n")[1]
        for value in values.split("\n"):
            start_out, start_in, end = map(int, value.split())
            mappings[i].append((start_in, start_out, end))
    for seed in seeds:
        val = seed
        for mapping in mappings:
            for map_ in mapping:
                if map_[0] <= val < map_[0] + map_[2]:
                    val = map_[1] + (val - map_[0])
        locations.append(val)
    return min(locations)


if __name__ == "__main__":
    print("example:", find_lowest_location_number("05/example05_1.txt"))
    print("input:", find_lowest_location_number("05/input05.txt"))
