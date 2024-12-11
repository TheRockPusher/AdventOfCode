from functools import lru_cache
from math import log10

with open("2024/inputs/d11input.txt") as f:
    inicialArrangement = [
        int(strNumber) for strNumber in f.readlines()[0].strip().split()
    ]


def blink(arrangement: list[int]) -> list[int]:
    newArrangement: list[int] = []
    for stone in arrangement:
        match stone:
            case 0:
                newArrangement.append(1)
            case n if (int(log10(n)) + 1) % 2 == 0:
                splitPoint = (int(log10(n)) + 1) // 2
                newArrangement.extend(
                    [int(str(stone)[:splitPoint]), int(str(stone)[splitPoint:])]
                )
            case _:
                newArrangement.append(stone * 2024)
    return newArrangement


@lru_cache(maxsize=100000)
def blinker(stone: int, cycleCount: int) -> int:
    count = 0
    if cycleCount == 0:
        return 1
    new_stones = blink([stone])
    for stoneN in new_stones:
        count += blinker(stoneN, cycleCount - 1)
    return count


def blinker_caller(arrangement, cycles):
    count = 0
    for i in range(cycles + 1):
        count = 0
        for stone in inicialArrangement:
            count += blinker(stone, i)
    return count


print(f"Exercise 1 -> {blinker_caller(inicialArrangement,25)}")
print(f"Exercise 2 -> {blinker_caller(inicialArrangement,75)}")
