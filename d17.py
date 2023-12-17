from queue import PriorityQueue

with open("inputs/d17test") as f:
    lineFile = f.readlines()


def return_neighbours(path: list[str], coord: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (x[0], x[1])
        for x in [
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
        ]
        if x[0] >= 0 and x[1] >= 0 and x[0] < len(path[0]) and x[1] < len(path)
    ]


def pathfinding(path: list[str]):
    frontier: PriorityQueue[tuple[int, tuple[int, int]]] = PriorityQueue()
    frontier.put((0, (0, 0)))
    came_from: dict[tuple[int, int], tuple[int, int]] = {(0, 0): (0, 0)}
    cumulative_cost: dict[tuple[int, int], int] = {(0, 0): 0}

    while not frontier.empty():
        current = frontier.get()
        if current[1] == (len(path[0]) - 1, len(path) - 1):
            break
        for next in return_neighbours(path, current[1]):
            next_cost = cumulative_cost[current[1]] + int(
                path[current[1][1]][current[1][0]]
            )
            if next not in cumulative_cost or next_cost < cumulative_cost[next]:
                cumulative_cost[next] = next_cost
                came_from[next] = current[1]
                frontier.put((next_cost, next))

    return cumulative_cost, came_from


a, b = pathfinding([x.replace("\n", "") for x in lineFile])
print(a)
