with open("inputs/d15input.txt") as f:
    lineFile = f.readlines()


def hashStep(step: str) -> int:
    res = 0
    for letter in step:
        res = (res + ord(letter)) * 17 % 256
    return res


print(f'Result part 1 -> {sum([hashStep(step) for step in lineFile[0].split(",")])}')
