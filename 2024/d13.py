with open("2024/inputs/d13input.txt") as f:
    cleanedInput = [i.strip() for i in f.readlines()]
    endList: list[list[float]] = [[]]
    for i, line in enumerate(cleanedInput):
        match i % 4:
            case 0:
                endList[i // 4].extend(
                    [int(splitLine.split("+")[1]) for splitLine in line.split(",")]
                )
            case 1:
                endList[i // 4].extend(
                    [int(splitLine.split("+")[1]) for splitLine in line.split(",")]
                )
            case 2:
                endList[i // 4].extend(
                    [int(splitLine.split("=")[1]) for splitLine in line.split(",")]
                )
            case _:
                endList.append([])


## System of two equations can be resolved by using a Matrix
## PressesA*xA+PressesB*xB=xTotal
## PressesB*yB+PressesB*yB= yTotal

# If determinant is not 0 function has 1 solution
# If it isn't, function can have either 0 or infinite solutions


def determinant(xA: float, xB: float, yA: float, yB: float) -> float:
    return xA * yB - xB * yA


# If det(M)=0 matrix needs to be consistent to have solutions
def consistent(xA: float, xB: float, xTotal: float, yTotal: float) -> bool:
    return xA / xB == xTotal / yTotal


# Solution given when resolving matrix
def matrixSolution(
    xA: float,
    xB: float,
    yA: float,
    yB: float,
    xTotal: float,
    yTotal: float,
    determinant: float,
) -> tuple[float, float]:
    n = (yB * xTotal - xB * yTotal) / determinant
    m = (-yA * xTotal + xA * yTotal) / determinant
    return n, m


# If we have multiple solutions we parametrize m in order of n and resolve looking for integers
def parametrizedSolution(xA: float, xB: float, xTotal: float) -> float:
    xTotalMod = xTotal % xB
    xAMod = xA % xB
    return xTotalMod / xAMod


def calculate(xA: float, xB: float, yA: float, yB: float, xTotal: float, yTotal: float):
    tokenA = 3
    det = determinant(xA, xB, yA, yB)
    if det:
        pressesA, pressesB = matrixSolution(xA, xB, yA, yB, xTotal, yTotal, det)
        if pressesA.is_integer() and pressesB.is_integer():
            return int(pressesA * tokenA + pressesB)
        else:
            return 0
    else:
        if consistent(xA, xB, xTotal, yTotal):
            pressesA = parametrizedSolution(xA, xB, xTotal)
            pressesB = (xTotal - pressesA * xA) / xB
            if pressesA.is_integer() and pressesB.is_integer():
                return int(pressesA * tokenA + pressesB)
            else:
                return 0
        else:
            return 0


result: list[int] = [
    calculate(line[0], line[2], line[1], line[3], line[4], line[5]) for line in endList
]
print(f"Exercise 1 -> {sum(result)}")
adder = 10000000000000
resultBig: list[int] = [
    calculate(line[0], line[2], line[1], line[3], line[4] + adder, line[5] + adder)
    for line in endList
]
print(f"Exercise 2 -> {sum(resultBig)}")
