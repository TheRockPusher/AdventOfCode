from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Vector(x=self.x - other.x, y=self.y - other.y)


with open("2023/inputs/d10input.txt") as f:
    lineFiles = f.readlines()

# translation (x,y)
# each letter had  two possible entry/exit points
# centred in 0,0
directions = {
    "|": set([Vector(0, -1), Vector(0, 1)]),
    "-": set([Vector(1, 0), Vector(-1, 0)]),
    "L": set([Vector(0, -1), Vector(1, 0)]),
    "J": set([Vector(-1, 0), Vector(0, -1)]),
    "7": set([Vector(-1, 0), Vector(0, 1)]),
    "F": set([Vector(0, 1), Vector(1, 0)]),
}


def find_S(lines: list[str]) -> Vector:
    for i, line in enumerate(lines):
        if "S" in line:
            res = line.index("S")
            return Vector(res, i)
    return Vector(0, 0)


def find_cycle(lines: list[str], startPosition: Vector, startVelocity: Vector):
    currentPosition = startPosition + startVelocity
    continuous = True
    currentLetter = lines[currentPosition.y][currentPosition.x]
    currentVelocity = startVelocity
    path = [startPosition, currentPosition]
    while continuous and (currentLetter in directions.keys()):
        next_velocity = directions[currentLetter] - set(
            [Vector(0, 0) - currentVelocity]
        )
        if len(next_velocity) == 1:
            currentVelocity = next_velocity.pop()
            currentPosition = currentPosition + currentVelocity
            currentLetter = lines[currentPosition.y][currentPosition.x]
            if currentPosition == startPosition:
                continuous = False
            else:
                path.append(currentPosition)
        else:
            continuous = False
    return path


def find_S_letter(path):
    p1 = path[1] - path[0]
    p2 = path[-1] - path[0]
    setP = set([p1, p2])
    for i in directions.keys():
        if len(directions[i] - setP) == 0:
            return i


def enclosed_squares(path: list[Vector]):
    path = sorted(path, key=lambda pos: (pos.y, pos.x))
    path = path
    crossings = ["|", "J", "L"]
    if find_S_letter(maxRes) in crossings:
        crossings.append("S")
    crossNum = 0
    enclosed_tiles = 0
    for i, tile in enumerate(path[:-1]):
        if lineFiles[tile.y][tile.x] in crossings:
            crossNum += 1
        if crossNum % 2 != 0 and tile.y == path[i + 1].y:
            enclosed_tiles += path[i + 1].x - tile.x - 1

    return enclosed_tiles


startLocation = find_S(lineFiles)
possibilities = [Vector(0, 1), Vector(1, 0), Vector(-1, 0), Vector(0, -1)]
steps = 0
for sVel in possibilities:
    res = find_cycle(lineFiles, startLocation, sVel)
    if len(res) > steps:
        steps = len(res)
        maxRes = res
        maxPosition = res[steps // 2]
print("PART1:")
print(f"Farthest Point -> {maxPosition}\nStep -> {steps//2}")
print(f"PART2 ->  {enclosed_squares(maxRes)}")
