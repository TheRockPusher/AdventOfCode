with open("inputs/d11input.txt") as f:
    lineFiles = f.readlines()


# find all ocurences of galaxies
def find_galaxy(file: list[str]) -> list[tuple[int, int]]:
    res = []
    for i, line in enumerate(file):
        res.extend([(pos, i) for pos, char in enumerate(line) if char == "#"])

    return res


def sum_distances(
    galaxies: list[tuple[int, int]],
    empty_lines: set[int],
    empty_rows: set[int],
    empty_distance: int = 2,
) -> int:
    s = 0
    for i, galaxy in enumerate(galaxies[:-1]):
        for j, galaxy2 in enumerate(galaxies[i + 1 :]):
            distance = abs(galaxy2[0] - galaxy[0]) + abs(galaxy2[1] - galaxy[1])
            emptyColCount = (
                empty_lines
                - {e for e in range(galaxy[1])}
                - {e2 for e2 in range(galaxy2[1], len(lineFiles))}
            )
            x = [galaxy[0], galaxy2[0]]
            emptyRowCount = (
                empty_rows
                - {r for r in range(min(x))}
                - {r2 for r2 in range(max(x), len(lineFiles[0]))}
            )
            s += distance + (empty_distance - 1) * (
                len(emptyRowCount) + len(emptyColCount)
            )
    return s


galaxies = find_galaxy(lineFiles)
all_lines = {i for i in range(len(lineFiles))}
used_lines = {pos[1] for pos in galaxies}
empty_lines = all_lines - used_lines
all_rows = {i for i in range(len(lineFiles[0]))}
used_rows = {pos[0] for pos in galaxies}
empty_rows = all_rows - used_rows
print(f"Result of part 1 ->  {sum_distances(galaxies, empty_lines, empty_rows)}")
print(
    f"Result of part 2 ->  {sum_distances(galaxies, empty_lines, empty_rows, 1000000)}"
)
