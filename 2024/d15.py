from copy import deepcopy
with open("2024/inputs/d15input.txt") as f:
    text: list[str] = f.readlines()
    originalGraph: list[str]= [t.strip() for t in text[:50]]
    movement: str = "".join([t.strip() for t in text[51:]])


def translationCoord(letter:str)->tuple[int,int]:
    match letter:
        case "v":
            return (0,1)
        case ">":
            return (1,0)
        case "^":
            return (0,-1)
        case "<":
            return (-1,0)
        case _ :
            print(letter)
            raise(ValueError)
        
i=True
def push(graph:list[str],coordToPush:tuple[int,int], movement:str, bigBox:bool = False)->bool: 
    # global i
    # if i:
    #     for r in graph:
    #         print(r)
    #         i=False
    #     print(movement)
    movementCoordinates=translationCoord(movement)    
    nextCoord=(coordToPush[0]+movementCoordinates[0], coordToPush[1]+movementCoordinates[1])
    match graph[nextCoord[1]][nextCoord[0]]:
        case "#":
            return False
        case ".":
            if not bigBox:
                graph[nextCoord[1]] = graph[nextCoord[1]][:nextCoord[0]]+graph[coordToPush[1]][coordToPush[0]]+graph[nextCoord[1]][nextCoord[0]+1:]
                graph[coordToPush[1]] = graph[coordToPush[1]][:coordToPush[0]]+ "."+graph[coordToPush[1]][coordToPush[0]+1:]
            return True
        case "O":
            if push(graph,nextCoord, movement):
                graph[nextCoord[1]] = graph[nextCoord[1]][:nextCoord[0]]+graph[coordToPush[1]][coordToPush[0]]+graph[nextCoord[1]][nextCoord[0]+1:]
                graph[coordToPush[1]] = graph[coordToPush[1]][:coordToPush[0]]+ "."+graph[coordToPush[1]][coordToPush[0]+1:]
                return True
            else:
                return False
        case "[":
            otherCoord=(nextCoord[0]+1,nextCoord[1])
            if push(graph,nextCoord, movement,True) and push(graph,otherCoord, movement,True):
                pass
            else:
                return False
        case "]":
            otherCoord=(nextCoord[0]-1,nextCoord[1])
            if push(graph,nextCoord, movement,True) and push(graph,otherCoord, movement,True):
                pass
            else:
                return False     
        case _:
            print(graph[nextCoord[1]][nextCoord[0]])
            raise (TypeError)

mapGraph = deepcopy(originalGraph)
x,y = (-1,-1)      
for y,line in enumerate(mapGraph):
    try:
        x=line.index("@")
        break
    except ValueError:
        pass
# print(movement)
for singleMovement in movement:
    i=True
    moved=push(mapGraph,(x,y),singleMovement)
    if moved:
        movementX, movementY= translationCoord(singleMovement)
        x=x+movementX
        y=y+movementY
print(f"Exercise 1 -> {sum([100*y+x for y,row in enumerate(mapGraph) for x,char in enumerate(row) if char =='O'])}")

mapGraphEx2:list[str]= []
for row in originalGraph:
    stringToAppend = ""
    for char in row:
        match char:
            case "#":
                stringToAppend=stringToAppend+"##"
            case ".":
                stringToAppend=stringToAppend+".."
            case "O":
                stringToAppend=stringToAppend+"[]"
            case "@":
                stringToAppend=stringToAppend+"@."
            case _:
                raise ValueError
    mapGraphEx2.append(stringToAppend)


for row in mapGraphEx2:
    print(row)

x,y = (-1,-1)      
for y,line in enumerate(mapGraphEx2):
    try:
        x=line.index("@")
        break
    except ValueError:
        pass
for singleMovement in movement:
    i=True
    moved=push(mapGraphEx2,(x,y),singleMovement)
    if moved:
        movementX, movementY= translationCoord(singleMovement)
        x=x+movementX
        y=y+movementY
print(f"Exercise 1 -> {sum([100*y+x for y,row in enumerate(mapGraphEx2) for x,char in enumerate(row) if char =='['])}")
