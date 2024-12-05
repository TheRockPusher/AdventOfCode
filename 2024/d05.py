with open("2024/inputs/d05input.txt") as f:
    lineFile = f.readlines()

def dictMaker(lines):
    dictToCheck:dict[int,list[int]] = {}
    for line in lines:
        if "|" in line:
            key = int(line.strip().split("|")[0])
            val = int(line.strip().split("|")[1])
            dictToCheck[key] = dictToCheck.get(key,list())+[val]
    return dictToCheck


def orderVerification(dictTest: dict[int,list[int]], pageList: list[list[int]]) -> int:
    s=0
    for page in pageList:
        valid=True
        for i,number in enumerate(page):
            if bool(set(dictTest.get(number,[])) & set(page[:i])):
                valid=False
                break
        if valid:
            s+=page[len(page)//2]
    return s

pageList = [list(map(int,page.strip().split(","))) for page in lineFile if "," in page]
print(f"Result of exercise 1 -> {orderVerification(dictMaker(lineFile), pageList)}")
