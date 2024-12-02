from collections import OrderedDict

with open("2023/inputs/d15input.txt") as f:
    lineFile = f.readlines()


def hashStep(step: str) -> int:
    res = 0
    for letter in step:
        res = (res + ord(letter)) * 17 % 256
    return res


def lensManipulator(
    fullStep: str, boxes: dict[int, OrderedDict[str, int]]
) -> dict[int, OrderedDict[str, int]]:
    if "=" in fullStep:
        boxLens = fullStep.split("=")
        box = hashStep(boxLens[0])
        if boxes.get(box, 0) == 0:
            boxes[box] = OrderedDict()
        boxes[box][boxLens[0]] = int(boxLens[1])
    if "-" in fullStep:
        boxHash = fullStep[:-1]
        box = hashStep(boxHash)
        if boxes.get(box, 0) != 0 and boxHash in boxes[box]:
            del boxes[box][boxHash]

    return boxes


print(f'Result part 1 -> {sum([hashStep(step) for step in lineFile[0].split(",")])}')


allBoxes: dict[int, OrderedDict[str, int]] = {}

for i in lineFile[0].split(","):
    lensManipulator(i, allBoxes)

resP2 = sum(
    [
        ((boxName + 1) * (slot + 1) * lens)
        for boxName, box in allBoxes.items()
        for slot, lens in enumerate(box.values())
    ]
)
print(f"Result of part2 -> {resP2}")
