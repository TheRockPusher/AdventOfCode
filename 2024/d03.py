import re

with open("2024/inputs/d03input.txt") as f:
    file = f.read()

# exercise 1
print(f"Exercise 1 -> {sum([int(n1) * int(n2) for n1, n2 in re.findall(r"mul\((\d*),(\d*)\)", file)])}")

# exercise 2
listWithDo = re.findall(r"mul\((\d*),(\d*)\)|(do\(\))|(don't\(\))", file)

do = True
res = 0
for tup in listWithDo:
    match tup:
        case ("", "", "", "don't()"):
            do = False
        case ("", "", "do()", ""):
            do = True
        case _:
            if do:
                res += int(tup[0]) * int(tup[1])
print(f"Exercise 2 -> {res}")
