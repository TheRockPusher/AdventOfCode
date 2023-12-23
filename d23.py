from __future__ import annotations

from dataclasses import dataclass, field
from queue import Queue

with open("inputs/d23input.txt") as f:
    lineFiles = f.readlines()


@dataclass(frozen=True, order=True)
class current_path:
    x: int
    y: int
    path: str
    past_path: set[tuple] = field(default_factory=set)


def get_neighbours(
    curr: current_path, text: list[str], slippery: bool = True
) -> list[current_path]:
    if slippery:
        match curr.path:
            case ".":
                mov_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            case ">":
                mov_possibilities = [(1, 0)]
            case "<":
                mov_possibilities = [(-1, 0)]
            case "v":
                mov_possibilities = [(0, 1)]
            case "^":
                mov_possibilities = [(0, -1)]
    else:
        mov_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    res = [
        current_path(x, y, char, curr.past_path.union({(curr.x, curr.y)}))
        for vector in mov_possibilities
        if (x := curr.x + vector[0]) >= 0
        and x < len(text[0])
        and (y := curr.y + vector[1]) >= 0
        and y < len(text)
        and (x, y) not in curr.past_path
        and (char := text[y][x]) != "#"
    ]

    return res


def find_longest_path(text: list[str], slippery: bool = True):
    long_path = 0
    frontier: Queue[current_path] = Queue()
    start_node = current_path(1, 0, text[0][1])
    frontier.put(start_node)

    while not frontier.empty():
        curr = frontier.get()
        if (curr.x, curr.y) != (len(text[0]) - 2, len(text) - 1):
            for next in get_neighbours(curr, text, slippery):
                frontier.put(next)
        else:
            long_path = max(long_path, len(curr.past_path))

    return long_path


treated_text = [line.replace("\n", "") for line in lineFiles]
print(f"Result of part 1 -> {find_longest_path(treated_text)}")
