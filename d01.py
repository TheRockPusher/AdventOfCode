import re

# read input file
with open("inputs/d01input.txt") as f:
    lineFile = f.readlines()

# part one
s = 0
for line in lineFile:
    dig_list = [x for x in line if x.isdigit()]
    if dig_list:
        s += int(dig_list[0] + dig_list[-1])
print(f"Result of part 1 -> {s}")


# part two
regexStart = "^.*?(one|two|three|four|five|six|seven|eight|nine|[1-9]).*"
regexEnd = "^.*(one|two|three|four|five|six|seven|eight|nine|[1-9]).*?"
dict_numb = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
s2 = 0


def to_num(n: str) -> str:
    if n.isdigit():
        return n
    return dict_numb[n]


for line in lineFile:
    firstRegex = re.search(regexStart, line)
    lastRegex = re.search(regexEnd, line)
    if firstRegex and lastRegex:
        firstDigit = firstRegex.group(1)
        lastDigit = lastRegex.group(1)
        s2 += int(f"{to_num(firstDigit)}{to_num(lastDigit)}")
print(f"result of part 2 -> {s2}")
