with open("inputs/d4input.txt") as f:
    lineFiles = f.readlines()


result = 0
for line in lineFiles:
    nums = line.split(":")[1].split("|")
    winningSet = set([int(i) for i in nums[0].split(" ") if i.isdigit()])
    chosenSet = set(
        [int(i) for i in nums[1].replace("\n", "").split(" ") if i.isdigit()]
    )
    numberHits = len(winningSet & chosenSet)
    print(len(winningSet))
    print(len(chosenSet))
    print(numberHits)
    if numberHits > 0:
        result += 2 ** (numberHits - 1)
print(f"Result of part 1 -> {result}")
