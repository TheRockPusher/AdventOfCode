from __future__ import annotations

from dataclasses import dataclass

with open("2024/inputs/d12test.txt") as f:
    farmingPlot = [plotLine.strip() for plotLine in f.readlines()]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, coordinate2) -> Coordinate:
        return Coordinate(x=self.x + coordinate2.x, y=self.y + coordinate2.y)


@dataclass
class Region:
    area: int
    perimeter: int
    # tuple[Coordinate, bool] bool= true if horizontal
    perimeterCoordinates: set[tuple[Coordinate,bool]]

    def __add__(self, region2) -> Region:
        return Region(
            area=self.area + region2.area, perimeter=self.perimeter + region2.perimeter, perimeterCoordinates=self.perimeterCoordinates.union(region2.perimeterCoordinates)
        )
    
    def sides(self):
        currentSides:list[set[tuple[Coordinate,bool]]] = []
        directions = [Coordinate(1,0),Coordinate(-1,0), Coordinate(0,1), Coordinate(0,-1)]
        for coord, horizontal in self.perimeterCoordinates:
            intersectedSide:set[tuple[Coordinate,bool]] = {(coord,horizontal)}
            for direction in directions:
                for side in currentSides:
                    if (coord+direction,horizontal) in side:
                        intersectedSide=intersectedSide.union(side)
                        currentSides.remove(side)           
            currentSides.append(intersectedSide)
        for side in currentSides:
            print(side)
        return len(currentSides)



def regionCounter(
    plotList: list[str], plotCoordinate: Coordinate, seenPlots: set[Coordinate]
) -> tuple[Region, set[Coordinate]]:
    seenPlots.add(plotCoordinate)
    maxX = len(plotList[0])
    maxY = len(plotList)
    region = Region(1, 0,set())
    for direction in {
        Coordinate(-1, 0),
        Coordinate(1, 0),
        Coordinate(0, -1),
        Coordinate(0, 1),
    }:
        newCoordinate = direction + plotCoordinate
        if newCoordinate not in seenPlots:
            if (
                0 <= newCoordinate.x < maxX
                and 0 <= newCoordinate.y < maxY
                and plotList[plotCoordinate.y][plotCoordinate.x]
                == plotList[newCoordinate.y][newCoordinate.x]
            ):
                newRegion, setCoordinates = regionCounter(
                    plotList, newCoordinate, seenPlots
                )
                region += newRegion
            else:
                region.perimeter += 1
                region.perimeterCoordinates.add((newCoordinate,bool(direction.y)))

    return region, seenPlots


def regionAdder(plotList: list[str]):
    totalCost = 0
    seenPlots: set[Coordinate] = set()
    for y, line in enumerate(plotList):
        for x, letter in enumerate(line):
            if Coordinate(x, y) not in seenPlots:
                newRegion, newSeen = regionCounter(plotList, Coordinate(x, y), set())
                totalCost += newRegion.area * newRegion.perimeter
                seenPlots = seenPlots.union(newSeen)
                print(f"{plotList[y][x]} ->area{newRegion.area}   perimeter{newRegion.perimeter}  sides{newRegion.sides()}")
    return totalCost


totalCost = regionAdder(farmingPlot)
print(f"Exercise 1 -> {totalCost}")
