from operator import add, mul
from typing import Callable

with open("2024/inputs/d07input.txt") as f:
    lineFile = [
        (int(line.split(":")[0]), list(map(int, line.split(":")[1].strip().split(" "))))
        for line in f.readlines()
    ]


def multiAdd(
    value: int, operands: list[int], operators: list[Callable[[int, int], int]]
) -> bool:
    if len(operands) == 2:
        return any(
            [value == operator(operands[0], operands[1]) for operator in operators]
        )
    if len(operands) == 1:
        return value == operands[0]
    if operands[0] >= value:
        return False
    return any(
        [
            multiAdd(
                value, [operator(operands[0], operands[1])] + operands[2:], operators
            )
            for operator in operators
        ]
    )


print(
    f"Exercise 1 -> {sum([line[0] for line in lineFile if multiAdd(line[0], line[1],[add,mul])])}"
)


def concatNumbers(n1: int, n2: int) -> int:
    return int(str(n1) + str(n2))


print(
    f"Exercise 2 -> {sum([line[0] for line in lineFile if multiAdd(line[0], line[1],[add,mul,concatNumbers])])}"
)
