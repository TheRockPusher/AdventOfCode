import time
with open("inputs/d5input.txt") as f:
    lineFiles = f.readlines()


seeds = [int(seed) for seed in lineFiles[0].replace("\n", "").split(" ")[1:]]
maps = lineFiles[2:]
sts: list[list[int]] = []
stf: list[list[int]] = []
ftw: list[list[int]] = []
wtl: list[list[int]] = []
ltt: list[list[int]] = []
tth: list[list[int]] = []
htl: list[list[int]] = []
currentMap: list[list[int]] = []
for i in maps:
    j = i.replace("\n", "")
    match j:
        case "seed-to-soil map:":
            currentMap = sts
        case "soil-to-fertilizer map:":
            currentMap = stf
        case "fertilizer-to-water map:":
            currentMap = ftw
        case "water-to-light map:":
            currentMap = wtl
        case "light-to-temperature map:":
            currentMap = ltt
        case "temperature-to-humidity map:":
            currentMap = tth
        case "humidity-to-location map:":
            currentMap = htl
        case "":
            pass
        case _:
            numberMap = [int(num) for num in j.split(" ")]
            numberMap.append(numberMap[0] - numberMap[1])
            currentMap.append(numberMap)


# M = list[destination, source, range, added]
def mapped(seed: int, M: list[list[int]]):
    for m in M:
        if seed >= m[1] and seed < (m[1] + m[2]):
            return seed + m[3]
    return seed


def get_seedLocation(seeds: list[int]) -> list[int]:
    seedLocation: list[int] = []
    mapList = [sts, stf, ftw, wtl, ltt, tth, htl]
    for seed in seeds:
        curr = seed
        for m in mapList:
            curr = mapped(curr, m)
        seedLocation.append(curr)
    return seedLocation


print(f"Result of part1 -> {min(get_seedLocation(seeds))}")