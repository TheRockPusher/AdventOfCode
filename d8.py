with open("inputs/d8input.txt") as f:
    lineFiles = f.readlines()

directions = lineFiles[0].replace("\n", "")
map2 = {
    mapVal.split()[0]: (mapVal.split()[2][1:4], mapVal.split()[3][:3])
    for mapVal in lineFiles[2:]
}

foundEnd = False
currentLocation = "AAA"
step = 0
while not foundEnd:
    for LR in directions:
        if LR == "L":
            currentLocation = map2[currentLocation][0]
        else:
            currentLocation = map2[currentLocation][1]
        step += 1
        if currentLocation == "ZZZ":
            foundEnd = True
            break

print(f"Result of part1 -> {step}")
