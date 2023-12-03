with open("inputs/d3input.txt") as f:
    lineFiles = f.readlines()


def get_symbol_coordinates(text: list[str]) -> list[tuple[int, int]]:
    res = []
    for y_pos, line in enumerate(lineFiles):
        res.extend(
            [
                (pos, y_pos)
                for pos, char in enumerate(line)
                if not char.isdigit() and char != "."
            ][:-1]
        )
    return res


def get_num_coord(coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # get coords to check
    coord_possible: list[tuple[int, int]] = []
    for coord in coords:
        for i in range(3):
            for j in range(3):
                if (i, j) != (1, 1):
                    coord_possible.append((coord[0] + i - 1, coord[1] + j - 1))
    return coord_possible


def get_num(num_coord: list[tuple[int, int]], text: list[str]) -> list[int]:
    res: list[int] = []
    maxLen = len(text)
    checked_coords: list[tuple[int, int]] = []
    for coord in num_coord:
        if (
            text[coord[1]][coord[0]].isdigit()
            and (coord[0], coord[1]) not in checked_coords
        ):
            n = text[coord[1]][coord[0]]
            # check back
            for i in range(coord[0] - 1, -1, -1):
                if text[coord[1]][i].isdigit() and (i, coord[1]) not in checked_coords:
                    n = text[coord[1]][i] + n
                    checked_coords.append((i, coord[1]))
                else:
                    break
            # check forwards
            for i in range(coord[0] + 1, maxLen, 1):
                if text[coord[1]][i].isdigit() and (i, coord[1]) not in checked_coords:
                    n = n + text[coord[1]][i]
                    checked_coords.append((i, coord[1]))
                else:
                    break
            res.append(int(n))
    return res


s_coord = get_symbol_coordinates(lineFiles)
num_coord = get_num_coord(s_coord)
nums = get_num(num_coord, lineFiles)
print(f"Result of part 1 -> {sum(nums)}")
