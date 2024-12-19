with open("2024/inputs/d19input.txt") as f:
    allText = f.readlines()
    towelPatterns = [pattern.strip() for pattern in allText[0].split(",")]
    combinations = [comb.strip() for comb in allText[2:]]


def combinationFitter(combination: str, patterns: list[str]) -> bool:
    if not combination:
        return True
    for pattern in patterns:
        patternLen = len(pattern)
        if combination[:patternLen] == pattern:
            possible = combinationFitter(combination[patternLen:], patterns)
            if possible:
                return True
    return False


res = 0
for combination in combinations:
    res += combinationFitter(combination, towelPatterns)

print(f"Exercise 1 -> {res}")
