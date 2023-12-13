with open("inputs/d13input.txt") as f:
    lineFiles = f.readlines()

patterns = [group.splitlines() for group in "".join(lineFiles).split("\n\n") if group]


def single_symmetry(
    pattern: list[str], firstCenters: list[int], distance: int, row: bool = True
) -> list[int]:
    if row:
        outOfRange = {
            center
            for center in firstCenters
            if (center - distance) < 0 or (center + distance + 1) >= len(pattern) 
        }
        possible = list(set(firstCenters) - outOfRange)
        possible = [
            center
            for center in possible
            if pattern[center - distance] == pattern[center + distance + 1]
        ]
    else:
        outOfRange = {
            center
            for center in firstCenters
            if (center - distance) < 0 or (center + distance + 1) >= len(pattern[0]) 
        }
        possible = list(set(firstCenters) - outOfRange)
        for rows in pattern:
            possible = [
                center
                for center in possible
                if rows[center - distance] == rows[center + distance + 1]
            ]
    if outOfRange:
        possible.extend(list(outOfRange))
    return possible

res = 0
for p, pattern in enumerate(patterns):
    rows = [i for i in range(len(pattern)-1)]
    col = [i for i in range(len(pattern[0])-1)]
    distance = 0
    while (len(rows) + len(col)) > 1 and distance < max(len(pattern), len(pattern[0])):
        rows = single_symmetry(pattern, rows, distance)
        col = single_symmetry(pattern, col, distance, False)
        distance += 1
    res += (rows[0]+1)*100 if rows else (col[0]+1)
    print(f"Pattern -> {p}, row/col -> {rows}/{col}")
print(res)
