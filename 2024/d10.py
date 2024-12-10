with open("2024/inputs/d10input.txt") as f:
    listTopographic: list[list[int]] = [
        list(map(int, line.strip())) for line in f.readlines()
    ]


def countTrailheadScore(
    topographicMap: list[list[int]],
    coord: tuple[int, int],
    value: int,
    past: list[tuple[int, int]],
) -> int:
    x, y = coord
    past += [(x, y)]
    if value == 9:
        return 1
    maxX = len(topographicMap[0])
    maxY = len(topographicMap)
    total = 0
    for new_x, new_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        total += (
            countTrailheadScore(topographicMap, (new_x, new_y), value + 1, past)
            if 0 <= new_x < maxX
            and 0 <= new_y < maxY
            and topographicMap[new_y][new_x] == value + 1
            and (new_x, new_y) not in past
            else 0
        )
    return total


total_Trailhead = sum(
    [
        countTrailheadScore(listTopographic, (x, y), 0, list())
        for y, line in enumerate(listTopographic)
        for x, value in enumerate(line)
        if value == 0
    ]
)

print(f"Exercise 1 -> {total_Trailhead}")
