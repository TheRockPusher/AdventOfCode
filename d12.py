import time
from functools import cache

with open("inputs/d12input.txt") as f:
    lineFiles = f.readlines()

@cache
def arrange_count(text: str, grp: tuple[int, ...]) -> int:
    if len(text) < (sum(grp) + len(grp) - 1) or sum(grp) < text.count("#"):
        return 0
    if len(text) == sum(grp) and len(grp) == 1:
        return 0 if "." in text else 1
    if len(grp) == 0:
        return 1
    if text[grp[0]] == "#" and text[0] == "#":
        return 0
    if text[grp[0]] == "#":
        return arrange_count(text[1:], grp)
    if text[0] == "#":
        return arrange_count(text[: grp[0]], grp[:1]) * arrange_count(
            text[grp[0] + 1 :], grp[1:]
        )
    return arrange_count(text[1:], grp) + arrange_count(
        text[: grp[0]], grp[:1]
    ) * arrange_count(text[grp[0] + 1 :], grp[1:])


def main_result(lineFiles, multiplier = 1 ,prints = False):
    res = 0    
    lineFiles = sorted(lineFiles, key=lambda x: len(x))
    for l_index, line in enumerate(lineFiles):
        lineList = line.split()
        group = tuple(int(i) for i in lineList[1].split(','))*multiplier
        textList = ((lineList[0]+"?")*multiplier)[:-1]
        if prints:
            print(
                f"text->{textList}  group -> {group}"
            )
        pr = res
        res += arrange_count(textList, group)
        if prints:
            print(f"line {l_index} res -> {res-pr}")
    return res

start_time = total_time = time.time()
print(f"Result of part1 -> {main_result(lineFiles)} time -> {time.time()-start_time}s")
print(f"Result of part2 -> {main_result(lineFiles, multiplier=5)} time -> {time.time()-start_time}s")
