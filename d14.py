import time
import copy

with open("inputs/d14input.txt") as f:
    lineFiles = f.readlines()


def vertical_pull(text_to_move: list[str], inverted: bool = False) -> list[str]:
    text = copy.deepcopy(text_to_move)
    if inverted:
        text.reverse()
    for i, line in enumerate(text):
        for row in range(i)[::-1]:
            new_string = "".join(
                "O" if r0 == "." and r1 == "O" else r0
                for r0, r1 in zip(text[row], text[row + 1])
            )
            new_string_plus = "".join(
                "." if r0 == "." and r1 == "O" else r1
                for r0, r1 in zip(text[row], text[row + 1])
            )
            text[row] = new_string
            text[row + 1] = new_string_plus
    if inverted:
        text.reverse()
    return text


def horizontal_pull(text_to_move: list[str], inverted: bool = False) -> list[str]:
    text = copy.deepcopy(text_to_move)
    for i, row in enumerate(text):
        text[i] = "".join(
            "".join(sorted(s, reverse=inverted)) + "#"
            for s in row.replace("\n", "").split("#")
        )[:-1]
    return text


def full_cycle(text: list[str]) -> list[str]:
    return horizontal_pull(
        vertical_pull(
            horizontal_pull(vertical_pull(text), inverted=True), inverted=True
        )
    )


def count_weight(text: list[str]) -> int:
    r = 0
    for i, line in enumerate(text):
        r += (len(text) - i) * line.count("O")
    return r


def find_cycle(text: list[str]) -> tuple[int, int]:
    i = 0
    text = [i.replace("\n", "") for i in text]
    res = text
    d_hash: dict[int, int] = {}
    while True:
        i += 1
        res = full_cycle(res)
        hashTup = hash(tuple(res))
        if d_hash.get(hashTup, 0) == 0:
            d_hash[hashTup] = i
        elif i:
            break

    return d_hash[hashTup], i


start_time = time.time()
moved = vertical_pull(lineFiles)
print(f"Result of part 1 -> {count_weight(moved)}")

n = 1000000000
cycleStart, cycleEnd = find_cycle(lineFiles)
resP2 = lineFiles
for i in range((n - cycleStart) % (cycleEnd - cycleStart) + cycleStart):
    resP2 = full_cycle(resP2)
print(f"Result of part 2 -> {count_weight(resP2)}")
