import fnmatch
from math import lcm

with open("2023/inputs/d08input.txt") as f:
    lineFiles = f.readlines()

directions = lineFiles[0].replace("\n", "")
map2 = {
    mapVal.split()[0]: (mapVal.split()[2][1:4], mapVal.split()[3][:3])
    for mapVal in lineFiles[2:]
}


def find_min_steps(startLoc, endLoc, mp, directions):
    foundEnd = False
    currentLocation = startLoc
    step = 0
    while not foundEnd:
        for LR in directions:
            if LR == "L":
                currentLocation = map2[currentLocation][0]
            else:
                currentLocation = map2[currentLocation][1]
            step += 1
            if fnmatch.fnmatch(currentLocation, endLoc):
                foundEnd = True
                break
    return step


print(f"Result of part1 -> {find_min_steps('AAA', 'ZZZ', map2, directions)}")

# P2
# Every A path only had one Z ending possible,
# calculate all possibles and then the least common multiple between the steps
currentLocationP2 = [Loc for Loc in map2.keys() if Loc[2] == "A"]
res = [find_min_steps(i, "*Z", map2, directions) for i in currentLocationP2]
print(f"Result of part2 -> {lcm(*res)}")
