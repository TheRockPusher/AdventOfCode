from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

with open("2024/inputs/d06input.txt") as f:
    lineFile = f.readlines()


def rebuild_line(linefile, x, y, letter: str):
    linefile[y] = linefile[y][:x] + letter + linefile[y][x + 1 :]
    return linefile


@dataclass
class Guard:
    x: int
    y: int
    direction: tuple[int, int]
    distinctsteps: int = 0

    def __post_init__(self):
        self.positionhistory: set[tuple[int, int, tuple[int, int]]] = {
            (self.x, self.y, self.direction)
        }

    def fullWalk(self, lineFile: list[str]) -> int:
        self.distinctsteps += 1
        lineFile[self.y] = (
            lineFile[self.y][: self.x] + "S" + lineFile[self.y][self.x + 1 :]
        )

        while True:
            nextstep = (self.x + self.direction[0], self.y + self.direction[1])
            if not (
                0 <= nextstep[0] < len(lineFile[0]) and 0 <= nextstep[1] < len(lineFile)
            ):
                return self.distinctsteps
            match lineFile[nextstep[1]][nextstep[0]]:
                case "#":
                    self.direction = (-self.direction[1], self.direction[0])
                case pastposition if pastposition in ["X", "S"]:
                    self.x = nextstep[0]
                    self.y = nextstep[1]
                case _:
                    self.x = nextstep[0]
                    self.y = nextstep[1]
                    self.distinctsteps += 1
                    lineFile = rebuild_line(lineFile, self.x, self.y, "X")
            if self.positionhistory & {(self.x, self.y, self.direction)}:
                return 0
            self.positionhistory = self.positionhistory.union(
                {(self.x, self.y, self.direction)}
            )


mapGuard = Guard(0, 0, (0, 0), -1)
for y, line in enumerate(lineFile):
    x = line.find("^")
    if x != -1:
        mapGuard = Guard(x, y, (0, -1))
        exists = True
        break
if mapGuard.distinctsteps == -1:
    raise AttributeError("Guard wasn't found")
ex1Guard = deepcopy(mapGuard)
ex1lineFile = deepcopy(lineFile)
print(f"Exercise 1 -> {ex1Guard.fullWalk(ex1lineFile)}")
uniquePositions = {
    (x, y)
    for x, y, dir in ex1Guard.positionhistory
    if (x, y) != (mapGuard.x, mapGuard.y)
}
print(
    f"Exercise 2 -> {[bool(deepcopy(mapGuard).fullWalk(rebuild_line(deepcopy(lineFile),x,y, "#"))) for x,y in uniquePositions].count(False)}"
)
