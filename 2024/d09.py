from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass


@dataclass
class memoryBlock:
    ID: int
    length: int


with open("2024/inputs/d09input.txt") as f:
    listLines: list[memoryBlock] = []
    free = False
    blockID = 0
    for letter in f.readlines()[0].strip():
        if free:
            listLines.append(memoryBlock(-1, int(letter)))
        else:
            listLines.append(memoryBlock(blockID, int(letter)))
            blockID += 1
        free = not free


def compaction(memoryListOriginal: list[memoryBlock]) -> list[memoryBlock]:
    memoryList: list[memoryBlock] = deepcopy(memoryListOriginal)
    i = 0
    while i < len(memoryList):
        block: memoryBlock = memoryList[i]
        if block.ID == -1:
            lastBlock: memoryBlock = memoryList[-1]
            if lastBlock.length == block.length:
                memoryList[i] = lastBlock
                memoryList = memoryList[:-1]
            elif lastBlock.length < block.length:
                memoryList[i : i + 1] = [
                    lastBlock,
                    memoryBlock(-1, block.length - lastBlock.length),
                ]
                memoryList = memoryList[:-1]
            else:
                memoryList[i] = memoryBlock(lastBlock.ID, block.length)
                memoryList[-1] = memoryBlock(
                    lastBlock.ID, lastBlock.length - block.length
                )
            if memoryList[-1].ID == -1:
                memoryList = memoryList[:-1]
        else:
            i += 1
    return memoryList


def checksumCalc(memoryList: list[memoryBlock]) -> int:
    i = 0
    res = 0
    for block in memoryList:
        res += sum([index * block.ID for index in range(i, i + block.length)])
        i += block.length
    return res


cleanedCompactedLines = [block for block in compaction(listLines) if block.length != 0]
print(f"Exercise 1 -> {checksumCalc(cleanedCompactedLines)}")
