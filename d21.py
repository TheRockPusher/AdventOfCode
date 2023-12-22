from collections import Counter
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


def return_neighbours(current: Coordinates, text: list[str], expand: bool = False):
    all_coords = [
        Coordinates(current.x + 1, current.y),
        Coordinates(current.x - 1, current.y),
        Coordinates(current.x, current.y + 1),
        Coordinates(current.x, current.y - 1),
    ]
    return (
        [
            coord
            for coord in all_coords
            if coord.x > 0
            and coord.y > 0
            and coord.x < len(text[0])
            and coord.y < len(text)
        ]
        if not expand
        else all_coords
    )


def coord_normalizer(coord: Coordinates, x_size: int, y_size: int) -> Coordinates:
    x = coord.x
    y = coord.y
    while x < 0:
        x += x_size
    while y < 0:
        y += y_size
    while x >= x_size:
        x -= x_size
    while y >= y_size:
        y -= y_size
    return Coordinates(x, y)


def pathfinding(
    text: list[str], start_coord: Coordinates, expand: bool = False, max_steps: int = 64
) -> tuple[set[Coordinates], Counter]:
    frontier: Queue[Coordinates] = Queue()
    frontier.put(start_coord)
    all_accessed_coords: set[Coordinates] = {start_coord}
    all_blocked_coords: set[Coordinates] = set()
    n_steps: dict[Coordinates, int] = {start_coord: 0}
    counter: Counter = Counter()
    while not frontier.empty():
        current = frontier.get()
        curr_steps = n_steps[current]
        counter[curr_steps] += 1
        if curr_steps < max_steps:
            new_coords = return_neighbours(current, text, expand)
            for coord in new_coords:
                if coord not in all_accessed_coords and coord not in all_blocked_coords:
                    treated_coord = coord
                    if expand:
                        treated_coord = coord_normalizer(coord, len(text[0]), len(text))
                    if text[treated_coord.y][treated_coord.x] == "#":
                        all_blocked_coords.add(coord)
                    else:
                        frontier.put(coord)
                        all_accessed_coords.add(coord)
                        n_steps[coord] = curr_steps + 1
    return all_accessed_coords, counter


def part_1(all_accessed_coords: set[Coordinates], start_coord: Coordinates) -> int:
    c = 0
    for i in all_accessed_coords:
        if (abs(i.x - start_coord.x) + abs(i.y - start_coord.y)) % 2 == 0:
            c += 1
    return c


start_coord = find_start_coord(lineFile)
coords, _ = pathfinding(lineFile, start_coord)
print(f"Result of part1 -> {part_1(coords, start_coord)}")

zero_layer, counter = pathfinding(lineFile, start_coord, True, 65)


# periodic diamonds
# number of layers of diamonds<-> total steps can be given with
#  Steps = 65+131*diamonds_layers
# Calculate for 0 one and two diamond layers
n_diamonds = (26501365 - 65) / 131
zero_coords, _ = zero_layer, counter = pathfinding(lineFile, start_coord, True, 65)
one_coords, _ = zero_layer, counter = pathfinding(lineFile, start_coord, True, 65 + 131)
two_coords, _ = zero_layer, counter = pathfinding(
    lineFile, start_coord, True, 65 + 131 * 2
)

n_zero = len(zero_coords) - part_1(zero_coords, start_coord)
n_one = part_1(one_coords, start_coord)
n_two = len(two_coords) - part_1(two_coords, start_coord)
print(f"Layer   :   Step\n0 :   {n_zero}\n1 :   {n_one}\n2  :   {n_two} ")

# Trying to fit results in a polinomial
# ax**2+bx+c
# c=n_zero
# a+b+n_zero = n_one
# 4a+2b+n_zero = n_two
c = n_zero
b = (4 * n_one - 3 * n_zero - n_two) / 2
a = n_one - n_zero - b
print(f"{a}x**2 + {b}x  + {c}")

# calculate for x = n_diamonds
print(f"Result of part2  ->  {int(a*(n_diamonds)**2 + b*(n_diamonds)+ c)}")
