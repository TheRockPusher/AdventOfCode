import math
import re
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, steps: int, mapSizeX: int, mapSizeY: int):
        newX = self.x + steps * self.vx
        newY = self.y + steps * self.vy
        if not 0 <= newX < mapSizeX:
            newX = newX % mapSizeX
        if not 0 <= newY < mapSizeY:
            newY = newY % mapSizeY
        self.x = newX
        self.y = newY
        return self

    def quadrant(self, mapSizeX: int, mapSizeY: int) -> int:
        m: tuple[int, int] = (mapSizeX // 2, mapSizeY // 2)
        if self.x < m[0] and self.y < m[1]:
            return 1
        if self.x > m[0] and self.y < m[1]:
            return 2
        if self.x < m[0] and self.y > m[1]:
            return 3
        if self.x > m[0] and self.y > m[1]:
            return 4
        else:
            return 0


with open("2024/inputs/d14input.txt") as f:
    robotList = [
        Robot(int(parts[1]), int(parts[2]), int(parts[4]), int(parts[5]))
        for line in f.readlines()
        if (parts := re.split(r"[,= ]", line.strip()))
    ]


def safetyFactor(
    steps: int, mapSizeX: int, mapSizeY: int, robotList: list[Robot]
) -> int:
    quadrantCount = Counter(
        [
            robot.move(steps, mapSizeX, mapSizeY).quadrant(mapSizeX, mapSizeY)
            for robot in robotList
        ]
    )
    print(quadrantCount)
    return quadrantCount[1] * quadrantCount[2] * quadrantCount[3] * quadrantCount[4]


print(f"Exercise 1 -> {safetyFactor(100,101,103,deepcopy(robotList))}")


def varianceCalc(mapSizeX: int, mapSizeY: int, robotList: list[Robot]):
    movedRobots = [robot.move(1, mapSizeX, mapSizeY) for robot in robotList]
    XY = [(robot.x, robot.y) for robot in movedRobots]
    allX = 0
    allY = 0
    for x, y in XY:
        allX += x
        allY += y
    meanX = allX / len(XY)
    meanY = allY / len(XY)
    varX = math.sqrt(sum((v[0] - meanX) ** 2 for v in XY) / len(XY))
    varY = math.sqrt(sum((v[1] - meanY) ** 2 for v in XY) / len(XY))
    return (varX, varY, XY, movedRobots)


minVar = 10000000
indexOfMinVar = 0
r = [(0, 0)]
movedRobots = robotList
for i in range(1, 10000):
    j = varianceCalc(101, 103, movedRobots)
    if j[0] + j[1] < minVar:
        minVar = j[0] + j[1]
        r = j[2]
        indexOfMinVar = i
    movedRobots = j[3]

print(f"Exercise 2 -> {indexOfMinVar}")

grid = [["." for _ in range(101)] for _ in range(103)]
for x, y in r:
    grid[y][x] = "X"
for row in reversed(grid):
    print(" ".join(row))
