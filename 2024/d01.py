with open("2024/inputs/d01input.txt") as f:
    lineFile = f.readlines()

# exercise 1
listA: list[int] = []
listB: list[int] = []


for line in lineFile:
    splitN = line.split()
    listA.append(int(splitN[0]))
    listB.append(int(splitN[1]))


print(sum([abs(n1 - n2) for n1, n2 in zip(sorted(listA), sorted(listB))]))


# exercise 1
# turn list into dicts(n,n_occurrence)
def occurrenceDict(l: list[int]) -> dict[int, int]:
    occurrences = dict()
    for n in l:
        nOccurrences = occurrences.get(n, 0)
        occurrences[n] = nOccurrences + 1

    return occurrences


occurrencesA = occurrenceDict(listA)
occurrencesB = occurrenceDict(listB)

print(sum([k * v * occurrencesB.get(k, 0) for k, v in occurrencesA.items()]))
