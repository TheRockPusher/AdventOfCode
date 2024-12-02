import re

with open("2023/inputs/d02input.txt") as f:
    lineFiles = f.readlines()


possibleGames: list[int] = []
MaxColor = {"red": 12, "blue": 14, "green": 13}
s = 0

for line in lineFiles:
    line = line.replace("\n", "")
    gameSplit = line.split(":")
    game = int(gameSplit[0].split(" ")[1])
    colorDict: dict[str, int] = {}
    # get list of max value per color
    for col in re.split(";|,", gameSplit[1]):
        colorPair = col.split(" ")
        colorDict[colorPair[2]] = max(
            int(colorDict.get(colorPair[2], 0)), int(colorPair[1])
        )
    # get possible games for part 1
    possible = True
    for colour in ["red", "blue", "green"]:
        if MaxColor[colour] < colorDict[colour]:
            possible = False
    if possible:
        possibleGames.append(game)

    # sum the  multiplication for part 2
    s += colorDict["red"] * colorDict["blue"] * colorDict["green"]
print(f"Possible games list -> {possibleGames}")
print(f"Result of part1 -> {sum(possibleGames)}")
print(f"Result of part2 -> {s}")
