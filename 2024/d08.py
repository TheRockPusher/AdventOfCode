from __future__ import annotations

from dataclasses import dataclass

with open("2024/inputs/d08input.txt") as f:
    listLines = [line.strip() for line in f.readlines()]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, C2: Coordinate) -> Coordinate:
        return Coordinate(self.x + C2.x, self.y + C2.y)

    def __sub__(self, C2: Coordinate) -> Coordinate:
        return Coordinate(self.x - C2.x, self.y - C2.y)

    def valid(self, MaxX: int, MaxY: int) -> bool:
        return (0 <= self.x < MaxX) and (0 <= self.y < MaxY)


def dictMaker(listLines) -> dict[str, set[Coordinate]]:
    dictLines: dict[str, set[Coordinate]] = {}
    for y, line in enumerate(listLines):
        for x, letter in enumerate(line):
            if letter != ".":
                dictLines[letter] = (
                    {Coordinate(x, y)}
                    if not dictLines.get(letter, False)
                    else dictLines[letter].union({Coordinate(x, y)})
                )
    return dictLines


def antiNode(C1: Coordinate, C2: Coordinate) -> set[Coordinate]:
    DistanceVector = C1 - C2
    return set(
        c
        for c in [C1 + DistanceVector, C2 - DistanceVector]
        if c.valid(len(listLines[0]), len(listLines))
    )


def antiNodeListCalc(CoordSet: set[Coordinate]) -> set[Coordinate]:
    CoordList = list(CoordSet)
    listSets = [
        antiNode(C1, C2)
        for i, C1 in enumerate(CoordList)
        for C2 in CoordList[i + 1 :]
        if i < len(CoordList)
    ]
    return {c for coordSet in listSets for c in coordSet}


dictLines = dictMaker(listLines)
totalSet = set()
for values in dictLines.values():
    totalSet.update(antiNodeListCalc(values))


print(f"Result Ex 1 -> {len(totalSet)}")
