from math import log10

with open("2024/inputs/d11input.txt") as f:
    inicialArrangement=[int(strNumber) for strNumber in f.readlines()[0].strip().split()]

def blink(arrangement: list[int])->list[int]:
    newArrangement:list[int] = []
    for stone in arrangement:
        match stone:
            case 0:
                newArrangement.append(1)
            case n if (int(log10(n))+1)%2==0:
                splitPoint = (int(log10(n))+1)//2
                newArrangement.extend([int(str(stone)[:splitPoint]),int(str(stone)[splitPoint:])])
            case _:
                newArrangement.append(stone*2024)
    return newArrangement

finalArrangement = inicialArrangement
for i in range(25):
    finalArrangement = blink(finalArrangement)
print(f"Exercise 1 -> {len(finalArrangement)}")

            
