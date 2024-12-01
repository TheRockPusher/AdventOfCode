from __future__ import annotations

from copy import deepcopy
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


def no_split(text: list[str], curr: current_path, slippery):
    distance = 1
    past = curr
    next = get_neighbours(curr, text, slippery)
    while len(next) == 1:
        if (next[0].x, next[0].y) == (len(text[0]) - 2, len(text) - 1):
            return distance, next[0], []
        past = next[0]
        next = get_neighbours(next[0], text, slippery)
        distance += 1
    return distance, past, next


def node_transversal(text: list[str], slippery=True):
    frontier: Queue[tuple[current_path, current_path]] = Queue()
    start_node = current_path(1, 0, text[0][1])
    frontier.put((start_node, start_node))
    node_dict: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = {}
    ran_nodes = {(1, 0)}

    while not frontier.empty():
        curr, past_node = frontier.get()
        distance, node, next = no_split(text, curr, slippery)
        if (node.x, node.y) not in ran_nodes:
            ran_nodes.add((past_node.x, past_node.y))
            node_dict[(node.x, node.y)] = node_dict.get((node.x, node.y), []) + [
                ((past_node.x, past_node.y), distance)
            ]
            node_dict[(past_node.x, past_node.y)] = node_dict.get(
                (past_node.x, past_node.y), []
            ) + [((node.x, node.y), distance)]
            for next_i in next:
                frontier.put((next_i, node))
    return node_dict


def find_longest_path_graph(
    graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]], end: tuple
):
    long_path = []
    frontier: Queue[tuple[tuple[int, int], list, int]] = Queue()
    start_node: tuple[tuple[int, int], list, int] = ((1, 0), [(1, 0)], 0)
    frontier.put(start_node)

    while not frontier.empty():
        node, past, old_distance = frontier.get()
        for nodes in set(graph[node]):
            if nodes[0] not in past:
                frontier.put(
                    (nodes[0], deepcopy(past + [nodes[0]]), old_distance + nodes[1])
                )
            if nodes[0] == end:
                long_path.append(old_distance + nodes[1])
    return max(long_path)


treated_text = [line.replace("\n", "") for line in lineFiles]
print(f"Result of part 1 -> {find_longest_path(treated_text)}")
graph2 = node_transversal(treated_text, False)
end = (len(treated_text[0]) - 2, len(treated_text) - 1)
# Slow, could be optimized
print(f"Result of part 2 -> {find_longest_path_graph(graph2, end)}")
