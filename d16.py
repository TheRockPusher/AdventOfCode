from __future__ import annotations
from dataclasses import dataclass, field

with open("inputs/d16input.txt") as f:
    lineFile = f.readlines()


@dataclass
class beam:
    x: int
    y: int
    vx: int
    vy: int
    history: list[tuple[int, int]] = field(default_factory=list, init=False)

    def collision(self, mirror: str) -> beam | None:
        match mirror:
            case "\\":
                self.vx, self.vy = self.vy, self.vx
            case "/":
                self.vx, self.vy = -self.vy, -self.vx
            case "|":
                if self.vx != 0:
                    self.vx, self.vy = self.vy, self.vx
                    return beam(self.x, self.y, -self.vx, -self.vy)
            case "-":
                if self.vy != 0:
                    self.vx, self.vy = self.vy, self.vx
                    return beam(self.x, self.y, -self.vx, -self.vy)
        return None

    def movement(self):
        self.history.append((self.x, self.y))
        self.x += self.vx
        self.y += self.vy

    def outside(self, max_x: int, max_y: int) -> bool:
        if 0 > self.x or self.x >= max_x or 0 > self.y or self.y >= max_y:
            return True
        return False


mirrorMap = [line.replace("\n", "") for line in lineFile]
startBeams = [beam(-1, 0, 1, 0)]
max_x = len(mirrorMap[0])
max_y = len(mirrorMap)
historySet: set[tuple[int, int]] = set([])
pipe_coord: list[tuple[int, int]] = []
while startBeams:
    objects_delete = []
    for iBeam in startBeams:
        iBeam.movement()
        if iBeam.outside(max_x, max_y):
            objects_delete.append(iBeam)
        else:
            if mirrorMap[iBeam.y][iBeam.x] != ".":
                childBeam = iBeam.collision(mirrorMap[iBeam.y][iBeam.x])
                if childBeam and (childBeam.x, childBeam.y) in pipe_coord:
                    objects_delete.append(iBeam)
                elif childBeam:
                    pipe_coord.append((childBeam.x, childBeam.y))
                    startBeams.append(childBeam)
    for beams in objects_delete:
        historySet = historySet.union(set(beams.history))
    startBeams = [beams for beams in startBeams if beams not in objects_delete]
print(f"result of part 1 -> {len(sorted(list(historySet)))-1}")
