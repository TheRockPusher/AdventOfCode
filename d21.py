from dataclasses import dataclass
from queue import Queue

with open("inputs/d21input.txt") as f:
    lineFile = f.readlines()

lineFile = [line.replace("\n", "") for line in lineFile]


@dataclass(frozen=True, order=True)
class Coordinates:
    x: int
    y: int


def find_start_coord(text: list[str]) -> Coordinates:
    for i, line in enumerate(text):
        if "S" in line:
            return Coordinates(line.index("S"), i)
    return Coordinates(0, 0)


def return_neighbours(
    current: Coordinates,
    text: list[str],
):
    all_coords = [
        Coordinates(current.x + 1, current.y),
        Coordinates(current.x - 1, current.y),
        Coordinates(current.x, current.y + 1),
        Coordinates(current.x, current.y - 1),
    ]
    return [
        coord
        for coord in all_coords
        if coord.x > 0
        and coord.y > 0
        and coord.x < len(text[0])
        and coord.y < len(text)
    ]


def pathfinding(text: list[str], start_coord: Coordinates) -> set[Coordinates]:
    frontier: Queue[Coordinates] = Queue()
    frontier.put(start_coord)
    all_accessed_coords: set[Coordinates] = {start_coord}
    all_blocked_coords: set[Coordinates] = set()
    n_steps: dict[Coordinates, int] = {start_coord: 0}
    while not frontier.empty():
        current = frontier.get()
        curr_steps = n_steps[current]
        if curr_steps < 64:
            new_coords = return_neighbours(current, text)
            for coord in new_coords:
                if coord not in all_accessed_coords and coord not in all_blocked_coords:
                    if text[coord.y][coord.x] == "#":
                        all_blocked_coords.add(coord)
                    else:
                        frontier.put(coord)
                        all_accessed_coords.add(coord)
                        n_steps[coord] = curr_steps + 1
    return all_accessed_coords


def part_1(all_accessed_coords: set[Coordinates], start_coord: Coordinates) -> int:
    c = 0
    for i in all_accessed_coords:
        if (abs(i.x - start_coord.x) + abs(i.y - start_coord.y)) % 2 == 0:
            c += 1
    return c


start_coord = find_start_coord(lineFile)
print(start_coord)
coords = pathfinding(lineFile, start_coord)
print(coords)
print(f"Result of part1 -> {part_1(coords, start_coord)}")
