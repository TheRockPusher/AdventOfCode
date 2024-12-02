with open("2024/inputs/d02input.txt") as f:
    lineFile = [list(map(int, line.split())) for line in f.readlines()]


def condition(n1, n2, positive=False, positive_check=False) -> bool:
    return abs(n1 - n2) > 3 or n1 == n2 or (positive != positive_check)


def safeChecker(list_to_check: list[int], dampener: int = 0) -> bool:
    positive = list_to_check[1] > list_to_check[0]
    for i in range(len(list_to_check) - 1):
        positive_check = list_to_check[i + 1] > list_to_check[i]
        if condition(list_to_check[i], list_to_check[i + 1], positive, positive_check):
            if dampener <= 0:
                return False
            dampener -= 1
            for j in range(i - 1, i + 2):
                if safeChecker(list_to_check[:j] + list_to_check[j + 1 :]):
                    return True
            return False
    return True


# Part 1
print(len([line for line in lineFile if safeChecker(line)]))

# Part 2
print(len([line for line in lineFile if safeChecker(line, dampener=1)]))
