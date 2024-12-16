from copy import deepcopy

with open("2024/inputs/d15input.txt") as f:
    text: list[str] = f.readlines()
    originalGraph: list[str] = [t.strip() for t in text[:50]]
    movement: str = "".join([t.strip() for t in text[51:]])


def translationCoord(letter: str) -> tuple[int, int]:
    match letter:
        case "v":
            return (0, 1)
        case ">":
            return (1, 0)
        case "^":
            return (0, -1)
        case "<":
            return (-1, 0)
        case _:
            print(letter)
            raise (ValueError)


def push(graph: list[str], coordToPush: tuple[int, int], movement: str) -> bool:
    movementCoordinates = translationCoord(movement)
    nextCoord = (
        coordToPush[0] + movementCoordinates[0],
        coordToPush[1] + movementCoordinates[1],
    )
    match graph[nextCoord[1]][nextCoord[0]]:
        case "#":
            return False
        case ".":
            graph[nextCoord[1]] = (
                graph[nextCoord[1]][: nextCoord[0]]
                + graph[coordToPush[1]][coordToPush[0]]
                + graph[nextCoord[1]][nextCoord[0] + 1 :]
            )
            graph[coordToPush[1]] = (
                graph[coordToPush[1]][: coordToPush[0]]
                + "."
                + graph[coordToPush[1]][coordToPush[0] + 1 :]
            )
            return True
        case "O":
            if push(graph, nextCoord, movement):
                graph[nextCoord[1]] = (
                    graph[nextCoord[1]][: nextCoord[0]]
                    + graph[coordToPush[1]][coordToPush[0]]
                    + graph[nextCoord[1]][nextCoord[0] + 1 :]
                )
                graph[coordToPush[1]] = (
                    graph[coordToPush[1]][: coordToPush[0]]
                    + "."
                    + graph[coordToPush[1]][coordToPush[0] + 1 :]
                )
                return True
            else:
                return False
        case w if w in ["[", "]"]:
            if movementCoordinates in [(1, 0), (-1, 0)]:
                if push(graph, nextCoord, movement):
                    graph[nextCoord[1]] = (
                        graph[nextCoord[1]][: nextCoord[0]]
                        + graph[coordToPush[1]][coordToPush[0]]
                        + graph[nextCoord[1]][nextCoord[0] + 1 :]
                    )
                    graph[coordToPush[1]] = (
                        graph[coordToPush[1]][: coordToPush[0]]
                        + "."
                        + graph[coordToPush[1]][coordToPush[0] + 1 :]
                    )
                    return True
                else:
                    return False
            else:
                tempGraph = deepcopy(graph)
                otherNextCoord = (
                    (nextCoord[0] + 1, nextCoord[1])
                    if w == "["
                    else (nextCoord[0] - 1, nextCoord[1])
                )
                if push(graph, nextCoord, movement) and push(
                    graph, otherNextCoord, movement
                ):
                    graph[nextCoord[1]] = (
                        graph[nextCoord[1]][: nextCoord[0]]
                        + graph[coordToPush[1]][coordToPush[0]]
                        + graph[nextCoord[1]][nextCoord[0] + 1 :]
                    )
                    graph[coordToPush[1]] = (
                        graph[coordToPush[1]][: coordToPush[0]]
                        + "."
                        + graph[coordToPush[1]][coordToPush[0] + 1 :]
                    )
                    return True
                else:
                    graph[:] = tempGraph
                    return False

        case _:
            print(graph[nextCoord[1]][nextCoord[0]])
            raise (TypeError)


def cycle(graph, movement):
    x, y = (-1, -1)
    for y, line in enumerate(graph):
        try:
            x = line.index("@")
            break
        except ValueError:
            pass
    # print(movement)
    for singleMovement in movement:
        moved = push(graph, (x, y), singleMovement)
        if moved:
            movementX, movementY = translationCoord(singleMovement)
            x = x + movementX
            y = y + movementY
    return graph


mapGraph = deepcopy(originalGraph)
print(
    f"Exercise 1 -> {sum([100*y+x for y,row in enumerate(cycle(mapGraph,movement)) for x,char in enumerate(row) if char =='O'])}"
)

mapGraphEx2: list[str] = []
for row in originalGraph:
    stringToAppend = ""
    for char in row:
        match char:
            case "#":
                stringToAppend = stringToAppend + "##"
            case ".":
                stringToAppend = stringToAppend + ".."
            case "O":
                stringToAppend = stringToAppend + "[]"
            case "@":
                stringToAppend = stringToAppend + "@."
            case _:
                raise ValueError
    mapGraphEx2.append(stringToAppend)

print(
    f"Exercise 2 -> {sum([100*y+x for y,row in enumerate(cycle(mapGraphEx2,movement)) for x,char in enumerate(row) if char =='['])}"
)
