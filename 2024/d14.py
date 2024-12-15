import re
from collections import Counter
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


print(f"Exercise 1 -> {safetyFactor(100,101,103,robotList)}")
