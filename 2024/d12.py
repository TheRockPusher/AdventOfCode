from __future__ import annotations

from dataclasses import dataclass

with open("2024/inputs/d12input.txt") as f:
    farmingPlot=[plotLine.strip() for plotLine in f.readlines()]

@dataclass(frozen=True)
class Coordinate:
    x:int
    y:int
    
    def __add__(self,coordinate2)->Coordinate:
        return Coordinate(
            x=self.x+coordinate2.x,
            y=self.y+coordinate2.y
        )

@dataclass
class Region:
    area: int
    perimeter: int
    
    def __add__(self,region2)->Region:
        return Region(
            area=self.area+region2.area,
            perimeter=self.perimeter+region2.perimeter
        )


def regionCounter(plotList:list[str], plotCoordinate:Coordinate,seenPlots: set[Coordinate] = set())->tuple[Region,set[Coordinate]]:
    seenPlots.add(plotCoordinate)
    maxX = len(plotList[0])
    maxY = len(plotList)
    region = Region(1,0)
    for direction in {Coordinate(-1,0), Coordinate(1,0), Coordinate(0,-1), Coordinate(0,1)}:
        newCoordinate = direction+plotCoordinate
        if newCoordinate not in seenPlots:
            if 0<=newCoordinate.x<maxX and 0<=newCoordinate.y<maxY and plotList[plotCoordinate.y][plotCoordinate.x]==plotList[newCoordinate.y][newCoordinate.x]:
                newRegion,setCoordinates =regionCounter(plotList,newCoordinate,seenPlots)
                region+=newRegion
            else:
                region.perimeter+=1    
    
    return region,seenPlots

def regionAdder(plotList:list[str]):
    totalRegion = Region(0,0)
    seenPlots: set[Coordinate] = set()
    for y,line in enumerate(plotList):
        for x,letter in enumerate(line):
            if Coordinate(x,y) not in seenPlots:
                newRegion,newSeen = regionCounter(plotList,Coordinate(x,y),seenPlots)
                totalRegion+=newRegion
                seenPlots.union(newSeen)
    return totalRegion

totalRegion = regionAdder(farmingPlot)
print(f"Exercise 1 -> {totalRegion} Cost={totalRegion.area*totalRegion.perimeter}")
