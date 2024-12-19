from functools import lru_cache

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


ex1 = 0
for combination in combinations:
    ex1 += combinationFitter(combination, towelPatterns)

print(f"Exercise 1 -> {ex1}")


@lru_cache
def combinationAdder(combination: str, patterns: frozenset[str]) -> int:
    res = 0
    if not combination:
        return 1
    for pattern in patterns:
        patternLen = len(pattern)
        if combination[:patternLen] == pattern:
            res += combinationAdder(combination[patternLen:], patterns)
    return res


ex2 = 0
for combination in combinations:
    ex2 += combinationAdder(combination, frozenset(towelPatterns))

print(f"Exercise 2 -> {ex2}")
