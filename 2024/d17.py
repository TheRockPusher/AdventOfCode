import random
from copy import deepcopy
from dataclasses import dataclass

with open("2024/inputs/d17input.txt") as f:
    entrada = [t.strip().split(":")[1][1:] for t in f.readlines() if t != "\n"]


@dataclass
class machine:
    A: int
    B: int
    C: int
    operands: list[int]
    instructions: list[int]
    stdout: str = ""
    verification = ""

    def combo(self, operand) -> int:
        match operand:
            case x if x <= 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise ValueError

    def adv(self, operand):
        numerator = self.A
        denominator = 2 ** self.combo(operand)
        self.A = int(numerator / denominator)

    def bxl(self, operand):
        self.B = self.B ^ operand

    def bst(self, operand):
        self.B = self.combo(operand) % 8

    def jnz(self, operand) -> int:
        if self.A != 0:
            return operand // 2 + 1 if operand != 0 else 0
        return -1

    def bxc(self, operand):
        self.B = self.B ^ self.C

    def out(self, operand):
        self.stdout += f"{self.combo(operand)%8},"

    def bdv(self, operand):
        numerator = self.A
        denominator = 2 ** self.combo(operand)
        self.B = int(numerator / denominator)

    def cdv(self, operand):
        numerator = self.A
        denominator = 2 ** self.combo(operand)
        self.C = int(numerator / denominator)

    def run(self):
        i = 0
        while i < len(self.operands):
            adder = 1
            operand, instruction = (self.operands[i], self.instructions[i])
            # print(instruction)
            # print(operand)
            match instruction:
                case 0:
                    self.adv(operand)
                case 1:
                    self.bxl(operand)
                case 2:
                    self.bst(operand)
                case 3:
                    j = self.jnz(operand)
                    if j != -1:
                        i = j
                        adder = 0
                case 4:
                    self.bxc(operand)
                case 5:
                    self.out(operand)
                case 6:
                    self.bdv(operand)
                case 7:
                    self.cdv(operand)
                case _:
                    raise ValueError
            i += adder
            if self.verification:
                if self.verification == self.stdout:
                    return True
                if self.verification[: len(self.stdout)] != self.stdout:
                    return False
        return False


robotOriginal = machine(
    int(entrada[0]),
    int(entrada[1]),
    int(entrada[2]),
    [int(t) for i, t in enumerate(entrada[3].split(",")) if i % 2 != 0],
    [int(t) for i, t in enumerate(entrada[3].split(",")) if i % 2 == 0],
)

robot = deepcopy(robotOriginal)
robot.run()
print(f"Exercise 1 -> {robot.stdout[:-1]}")

a = 0
similar = 1
EXPECTED_OUTPUT = entrada[3].split(",")
while True:
    for i in range(8):
        robot = deepcopy(robotOriginal)
        robot.A = a
        robot.run()
        if robot.stdout[:-1].split(",")[-similar:] == EXPECTED_OUTPUT[-similar:]:
            similar += 1
            print(f"{a} , {robot.stdout[:-1]}")
            a *= 8
            break
        a += 1
    if robot.stdout[:-1].split(",") == EXPECTED_OUTPUT:
        print(f"\nExercise 2 final result {a/8} , {robot.stdout[:-1]}")
        break
