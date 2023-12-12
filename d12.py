import time

with open("inputs/d12input.txt") as f:
    lineFiles = f.readlines()


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

    # print(f"{arrange_count(text[1:], grp)}")
    # print(f"{arrange_count(text[: grp[0]], grp[:1])}")
    # print(f"{arrange_count(text[grp[0] + 1:], grp[1:])}")

    return arrange_count(text[1:], grp) + arrange_count(
        text[: grp[0]], grp[:1]
    ) * arrange_count(text[grp[0] + 1 :], grp[1:])


res = 0
start_time = total_time = time.time()
lineFiles = sorted(lineFiles, key=lambda x: len(x))
# lineFiles = ["???  1,2"]
# lineFiles = ["?#?.#????#?.???.?#  3,3,2,1,1,2"]
# lineFiles = ["#?.?#???. 4"]
for l_index, line in enumerate(lineFiles):
    lineList = line.split()
    print(
        f"text->{lineList[0]}  group -> {tuple(int(i) for i in lineList[1].split(','))}"
    )
    pr = res
    res += arrange_count(lineList[0], tuple(int(i) for i in lineList[1].split(",")))
    print(f"line {l_index} res -> {res-pr}")

print(f"Result of part1 -> {res}\n time -> {time.time()-start_time}s")
