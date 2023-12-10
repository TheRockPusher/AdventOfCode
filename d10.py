from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Vector(x=self.x - other.x, y=self.y - other.y)


with open("inputs/d10input.txt") as f:
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


startLocation = find_S(lineFiles)
possibilities = [Vector(0, 1), Vector(1, 0), Vector(-1, 0), Vector(0, -1)]
steps = 0
for sVel in possibilities:
    res = find_cycle(lineFiles, startLocation, sVel)
    if len(res) > steps:
        steps = len(res)
        maxPosition = res[steps // 2]
print(f"Farthest Point -> {maxPosition}\nStep -> {steps//2}")
