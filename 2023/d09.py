with open("inputs/d09input.txt") as f:
    lineFiles = f.readlines()


def get_down_sequence(nums: list[int]) -> list[int]:
    res = []
    for i in range(len(nums) - 1):
        res.append(nums[i + 1] - nums[i])
    return res


def get_up_sequence(downList: list[list[int]], Left: bool = False) -> list[list[int]]:
    downList[-1].append(0)
    lastNum = 0
    l_downList = len((downList))
    for i, nums in enumerate(reversed(downList[:-1])):
        if Left:
            lastNum = nums[0] - lastNum
            downList[l_downList - i - 2].insert(0, lastNum)
        else:
            lastNum = lastNum + nums[-1]
            downList[l_downList - i - 2].append(lastNum)
    return downList


def get_total_down_sequence(line: list[int]) -> list[list[int]]:
    res = [line]
    for i in range(len(line)):
        newLine = get_down_sequence(res[-1])
        res.append(newLine)
        if not any(newLine):
            break

    return res


r_p1 = 0
r_p2 = 0
for line in lineFiles:
    downRes = get_total_down_sequence([int(i) for i in line.split()])
    upRes = get_up_sequence(downRes)
    upResLeft = get_up_sequence(downRes, True)
    r_p1 += upRes[0][-1]
    r_p2 += upResLeft[0][0]

print(f"Result of part 1 -> {r_p1}")
print(f"Result of part 2 -> {r_p2}")
