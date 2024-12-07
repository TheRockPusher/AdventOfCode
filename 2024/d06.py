from __future__ import annotations

from dataclasses import dataclass

with open("2024/inputs/d06input.txt") as f:
    lineFile = f.readlines()


@dataclass
class Guard:
    x: int
    y: int
    direction: tuple[int, int]
    distinctsteps: int = 0

    def fullWalk(self, lineFile: list[str]):
        self.distinctsteps += 1
        lineFile[self.y] = (
            lineFile[self.y][: self.x] + "X" + lineFile[self.y][self.x + 1 :]
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
                case "X":
                    self.x = nextstep[0]
                    self.y = nextstep[1]
                case _:
                    self.x = nextstep[0]
                    self.y = nextstep[1]
                    self.distinctsteps += 1
                    lineFile[self.y] = (
                        lineFile[self.y][: self.x]
                        + "X"
                        + lineFile[self.y][self.x + 1 :]
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

print(f"Exercise 1 -> {mapGuard.fullWalk(lineFile)}")
