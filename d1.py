import re

# read input file
with open("Python/AdventOfCode/d1input.txt") as f:
    linefile = f.readlines()

# part one
s = 0
for line in linefile:
    dig_list = [x for x in line if x.isdigit()]
    if dig_list:
        s += int(dig_list[0] + dig_list[-1])
print(s)


# part two
regexstart = "^.*?(one|two|three|four|five|six|seven|eight|nine|[1-9]).*"
regexend = "^.*(one|two|three|four|five|six|seven|eight|nine|[1-9]).*?"
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


for line in linefile:
    firstRegex = re.search(regexstart, line)
    lastRegex = re.search(regexend, line)
    if firstRegex and lastRegex:
        firstDigit = firstRegex.group(1)
        lastDigit = lastRegex.group(1)
        s2 += int(f"{to_num(firstDigit)}{to_num(lastDigit)}")
print(s2)
