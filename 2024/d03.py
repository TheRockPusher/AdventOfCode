import re

with open("2024/inputs/d03input.txt") as f:
    file = f.read()

# exercise 1
print(sum([int(n1)*int(n2) for n1,n2 in re.findall(r"mul\((\d*),(\d*)\)",file)]))

