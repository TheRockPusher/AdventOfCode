with open("2024/inputs/d04input.txt") as f:
    lineFile = f.readlines()


# Exercise 1
def search(lineFile,coord:tuple[int,int],direction:tuple[int,int],check_letter:int, word:str)->bool:
    nextCoord=(coord[0]+direction[0],coord[1]+direction[1])
    if (not 0<=nextCoord[0]<len(lineFile[0])) or (not 0<=nextCoord[1]<len(lineFile)):
        return False
    if word[check_letter] !=lineFile[nextCoord[1]][nextCoord[0]]:
        return False
    if check_letter==len(word)-1:
        return True
    else:
        return search(lineFile,nextCoord,direction,check_letter+1,word)

def searchAllDirections(lineFile,coord:tuple[int,int],check_letter:int, word:str):
    horizontal_search=search(lineFile,coord,(1,0),check_letter,word)
    horizontal_opp_search=search(lineFile,coord,(-1,0),check_letter,word)
    vertical_search=search(lineFile,coord,(0,1),check_letter,word)
    vertical_opp_search=search(lineFile,coord,(0,-1),check_letter,word)
    diagonal_search=search(lineFile,coord,(1,1),check_letter,word)
    diagonal_opp_search=search(lineFile,coord,(-1,-1),check_letter,word)
    diagonal_back_search=search(lineFile,coord,(1,-1),check_letter,word)
    diagonal_back_opp_search=search(lineFile,coord,(-1,1),check_letter,word)
    return sum([horizontal_search,horizontal_opp_search,vertical_search,vertical_opp_search,diagonal_search,diagonal_opp_search,diagonal_back_search,diagonal_back_opp_search])

total =0
for y,line in enumerate(lineFile):
    for x,letter in enumerate(line):
        if letter=='X':
            total+=searchAllDirections(lineFile,(x,y),1,'XMAS')
print(total)
