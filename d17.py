from queue import PriorityQueue
from dataclasses import dataclass

with open("inputs/d17input.txt") as f:
    lineFile = f.readlines()


@dataclass(frozen=True, order=True)
class Coordinates:
    x: int
    y: int
    past_x: int
    past_y: int


def previous_neighbour_path(
    coord: Coordinates, movement: tuple[int, int]
) -> Coordinates:
    return (
        Coordinates(coord.x + movement[0], coord.y, coord.past_x + movement[0], 0)
        if movement[1] == 0
        else Coordinates(coord.x, coord.y + movement[1], 0, coord.past_y + movement[1])
    )


def return_neighbours(
    path: list[str], coord: Coordinates, max_straight: int
) -> list[Coordinates]:
    return [
        c
        for c in [
            previous_neighbour_path(coord, (1, 0)),
            previous_neighbour_path(coord, (-1, 0)),
            previous_neighbour_path(coord, (0, -1)),
            previous_neighbour_path(coord, (0, 1)),
        ]
        if c.x >= 0
        and c.y >= 0
        and c.x < len(path[0])
        and c.y < len(path)
        and abs(c.past_x) <= max_straight
        and abs(c.past_y) <= max_straight
    ]


def pathfinding(path: list[str], max_straight: int):
    startCoordinate = Coordinates(0, 0, 0, 0)
    frontier: PriorityQueue[tuple[int, Coordinates]] = PriorityQueue()
    frontier.put((0, startCoordinate))
    came_from: dict[Coordinates, Coordinates] = {startCoordinate: startCoordinate}
    cumulative_cost: dict[Coordinates, int] = {startCoordinate: 0}

    while not frontier.empty():
        _, current = frontier.get()
        if (current.x, current.y) == (len(path[0]) - 1, len(path) - 1):
            break
        for next in return_neighbours(path, current, max_straight):
            next_cost = cumulative_cost[current] + int(
                path[current.y][current.x]
            )
            if next not in cumulative_cost or next_cost < cumulative_cost[next]:
                cumulative_cost[next] = next_cost
                came_from[next] = current
                frontier.put((next_cost, next))

    return cumulative_cost, came_from

path = [x.replace("\n", "") for x in lineFile]
coordCostDict, _ = pathfinding(path,3)
#in exercise first values doesn count but last does
factor = int(path[-1][-1])-int(path[0][0])
lastCoordPossibilities = [i for i in coordCostDict if i.x == len(path[0])-1 and i.y == len(path)-1]
print(f"Result of part 1 -> {min([coordCostDict[i]+factor for i in lastCoordPossibilities])}")
