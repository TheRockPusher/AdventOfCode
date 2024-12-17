from queue import PriorityQueue, Queue

with open("2024/inputs/d16input.txt") as f:
    maze = [t.strip() for t in f.readlines()]

end = (len(maze[0]) - 2, 1)
start = (1, len(maze) - 2)


def dijkstra(maze: list[str], start: tuple[int, int]):
    mapDistance: dict[tuple[int, int], int] = {start: (0)}
    placesToVisit: PriorityQueue[tuple[int, tuple[int, int, int, int]]] = (
        PriorityQueue()
    )
    placesToVisit.put((0, (start[0], start[1], 1, 0)))
    while not placesToVisit.empty():
        score, xy = placesToVisit.get()
        baseX, baseY, pastCoordX, pastCoordY = xy
        for coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = baseX + coord[0]
            y = baseY + coord[1]
            if maze[y][x] != "#":
                oldScore = mapDistance.get((x, y), 9999999999)
                newScore = (
                    1001 if pastCoordX * coord[0] + pastCoordY * coord[1] == 0 else 1
                )
                neighbourScore = score + newScore
                if neighbourScore < oldScore:
                    mapDistance[(x, y)] = neighbourScore
                    placesToVisit.put((neighbourScore, (x, y, coord[0], coord[1])))
    return mapDistance


Ex1 = dijkstra(maze, start)
print(f"Exercise 1 -> {Ex1[end]}")


def pathSearcher(distanceMap: dict[tuple[int, int], int], end: tuple[int, int]):
    placesToSit = Queue()
    placesToSit.put((end[0], end[1], 1, 1))
    seat: set[tuple[int, int]] = {end}
    Turn = 0
    while not placesToSit.empty():
        if Turn:
            Turn -= 1
        baseX, baseY, _, _ = placesToSit.get()
        for coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = baseX + coord[0]
            y = baseY + coord[1]
            if maze[y][x] != "#":
                distance = distanceMap[(baseX, baseY)] - distanceMap[(x, y)]
                if distance == 1:
                    placesToSit.put((x, y, coord[0], coord[1]))
                    seat.add((x, y))
                elif distance == 1001:
                    Turn = 2
                    placesToSit.put((x, y, coord[0], coord[1]))
                    seat.add((x, y))
                elif distance == -999 and Turn:
                    placesToSit.put((x, y, coord[0], coord[1]))
                    seat.add((x, y))
    return seat


# endMaze = dijkstra(maze,end)
# seats = []
# for coordinate,score in endMaze.items():
#     if Ex1[end]-score==Ex1[coordinate]:
#         seats.append(coordinate)

# print(seats)
ex2 = pathSearcher(Ex1, end)
print(f"Exercise 2 -> {len(ex2)}")
