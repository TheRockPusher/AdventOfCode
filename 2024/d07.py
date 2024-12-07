with open("2024/inputs/d07input.txt") as f:
    lineFile = [
        (int(line.split(":")[0]), list(map(int, line.split(":")[1].strip().split(" "))))
        for line in f.readlines()
    ]


def multiAdd(value: int, operands: list[int]) -> bool:
    if len(operands) == 2:
        return (value == operands[0] + operands[1]) or (
            value == operands[0] * operands[1]
        )
    if len(operands) == 1:
        return value == operands[0]
    if operands[0] >= value:
        return False
    return multiAdd(value, [operands[0] + operands[1]] + operands[2:]) or multiAdd(
        value, [operands[0] * operands[1]] + operands[2:]
    )


print(sum([k for k, v in lineFile if multiAdd(k, v)]))
