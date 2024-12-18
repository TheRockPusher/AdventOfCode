from __future__ import annotations
from dataclasses import dataclass
from queue import PriorityQueue

@dataclass(frozen= True, order=True)
class Coordinate:
    x: int
    y: int

    def __add__(self,other: Coordinate)->Coordinate:
        return Coordinate(self.x +other.x,self.y+other.y)
    
    def inside(self,size:int) -> bool:
        if 0<=self.x<=size and 0<=self.y<=size:
            return True
        return False

with open("2024/inputs/d18input.txt") as f:
    falling_blocks = [Coordinate(*map(int,line.strip().split(","))) for line in f.readlines()]

def dijkstra(start: Coordinate,end: Coordinate,size: int,blocked:list[Coordinate]):
    visited: dict[Coordinate,int] = {start:0}
    q:PriorityQueue[tuple[int,Coordinate]] = PriorityQueue()
    q.put((0,start))
    while not q.empty():
        currentScore,currentCoord = q.get()
        currentScore+=1
        for coord in [(Coordinate(1,0)),(Coordinate(-1,0)),(Coordinate(0,1)),(Coordinate(0,-1))]:
            neighbour = currentCoord+coord
            if neighbour.inside(size) and neighbour not in blocked:
                if currentScore<visited.get(neighbour,9999999999):
                    visited[neighbour]= currentScore
                    q.put((currentScore,neighbour))

    return visited

size=70
start = Coordinate(0,0)
end = Coordinate(size,size)
res = dijkstra(start,end,size,falling_blocks[:1024])
                
print(f"Exercise 1 -> {res}")

# def calculateFinalBlock():


# # map = [["."]*size]*size
# # for c,score in res.items():
# #     map[c.y][c.x]=str(score)
# # for c in falling_blocks[:1024]:
# #     map[c.y][c.x] = "#"

# # for line in map:
# #     print(line)