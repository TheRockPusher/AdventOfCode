from typing import Optional

with open("inputs/d13input.txt") as f:
    lineFiles = f.readlines()

patterns = [group.splitlines() for group in "".join(lineFiles).split("\n\n") if group]


def diff_count(l1: str, l2: str):
    a = 0
    for i, j in zip(l1, l2):
        if i != j:
            a += 1
    return a


def single_symmetry(
    pattern: list[str],
    firstCenters: list[int],
    distance: int,
    row: bool = True,
    smudge: bool = False,
    smudgers: Optional[dict[int, int]] = None,
):
    if not smudgers and smudge:
        smudgers = {}
    if row:
        outOfRange = {
            center
            for center in firstCenters
            if (center - distance) < 0 or (center + distance + 1) >= len(pattern)
        }
        possible = list(set(firstCenters) - outOfRange)
        if smudge:
            smudgersNew = [
                center
                for center in possible
                if diff_count(
                    pattern[center - distance], pattern[center + distance + 1]
                )
                == 1
            ]
            superSmudger = [
                center
                for center in possible
                if diff_count(
                    pattern[center - distance], pattern[center + distance + 1]
                )
                > 1
            ]
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
        smudgersNewTemp2: dict = {}
        for rows in pattern:
            if smudge:
                smudgersNewTemp = [
                    center
                    for center in list(set(firstCenters) - outOfRange)
                    if rows[center - distance] != rows[center + distance + 1]
                ]

                smudgersNewTemp2.update(
                    {i: smudgersNewTemp2.get(i, 0) + 1 for i in smudgersNewTemp}
                )
            possible = [
                center
                for center in possible
                if rows[center - distance] == rows[center + distance + 1]
            ]
        if smudge:
            smudgersNew = [i for i, j in smudgersNewTemp2.items() if j == 1]
            superSmudger = [i for i, j in smudgersNewTemp2.items() if j > 1]

    if outOfRange:
        possible.extend(list(outOfRange))
    if smudge and smudgers is not None:
        for smgd in smudgersNew:
            if smudgers.get(smgd, 0) == 0:
                possible.append(smgd)
            smudgers[smgd] = smudgers.get(smgd, 0) + 1
        for ss in superSmudger:
            if smudgers.get(ss, 0) != 0:
                del smudgers[ss]
        return possible, smudgers
    return possible


res = 0
for p, pattern in enumerate(patterns):
    rows = [i for i in range(len(pattern) - 1)]
    col = [i for i in range(len(pattern[0]) - 1)]
    distance = 0
    while (len(rows) + len(col)) > 1 and distance < max(len(pattern), len(pattern[0])):
        rows = single_symmetry(pattern, rows, distance)
        col = single_symmetry(pattern, col, distance, False)
        distance += 1
    res += (rows[0] + 1) * 100 if rows else (col[0] + 1)
    # print(f"Pattern -> {p}, row/col -> {rows}/{col}")
print(f"Result of part 1 -> {res}")

res = 0
for p, pattern in enumerate(patterns):
    rows = [i for i in range(len(pattern) - 1)]
    col = [i for i in range(len(pattern[0]) - 1)]
    distance = 0
    smudgersRows: dict[int, int] = {}
    smudgersCol: dict[int, int] = {}
    while (len(rows) + len(col)) > 0 and distance < max(len(pattern), len(pattern[0])):
        rows, smudgersRows = single_symmetry(
            pattern, rows, distance, smudge=True, smudgers=smudgersRows
        )
        col, smudgersCol = single_symmetry(
            pattern, col, distance, False, smudge=True, smudgers=smudgersCol
        )
        distance += 1

    res += (
        (list(smudgersRows.keys())[0] + 1) * 100
        if smudgersRows
        else (list(smudgersCol.keys())[0] + 1)
    )
    # print(f"Pattern -> {p}, row/col -> {rows}/{col}")
    # print(f"Pattern -> {p}, smudger -> \
    # {smudgersRows}/{smudgersCol} distance{distance}")
print(f"Result of part 2 -> {res}")
