from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class block:
    x: range
    y: range
    z: range


with open("2023/inputs/d22input.txt") as f:
    lineFiles = f.readlines()


def load_blocks(text: list[str]) -> dict[int, set[block]]:
    block_height: dict[int, set[block]] = defaultdict(set)
    for line in text:
        blockText = [(coord.split(",")) for coord in line.replace("\n", "").split("~")]
        block_height[int(blockText[1][2])].add(
            block(
                range(int(blockText[0][0]), int(blockText[1][0]) + 1),
                range(int(blockText[0][1]), int(blockText[1][1]) + 1),
                range(int(blockText[0][2]), int(blockText[1][2]) + 1),
            )
        )

    return block_height


def range_intercepts(block1: block, block2: block) -> bool:
    return (
        False
        if block1.x[-1] < block2.x[0]
        or block1.x[0] > block2.x[-1]
        or block1.y[-1] < block2.y[0]
        or block1.y[0] > block2.y[-1]
        else True
    )


def drop_blocks(block_dict: dict[int, set[block]]) -> tuple[dict[int, set[block]], int]:
    dropped_block_dict: dict[int, set[block]] = defaultdict(set)
    counter_drops: int = 0
    for i in range(1, max(block_dict.keys()) + 1):
        for block_i in block_dict[i]:
            descent = 0
            drop = False
            while descent < (block_i.z[0] - 1) and (
                dropped_block_dict.get(block_i.z[0] - 1 - descent, 0) == 0
                or not any(
                    [
                        range_intercepts(block_i, block_check)
                        for block_check in dropped_block_dict[
                            block_i.z[0] - descent - 1
                        ]
                    ]
                )
            ):
                descent += 1
                drop = True
            new_z_start = block_i.z[0] - descent
            new_z_end = block_i.z[-1] - descent
            dropped_block_dict[new_z_end].add(
                block(block_i.x, block_i.y, range(new_z_start, new_z_end + 1))
            )
            if drop:
                counter_drops += 1

    return dropped_block_dict, counter_drops


def count_who_single_holds(block_dict: dict[int, set[block]]) -> set[block]:
    set_who_single_holds: set[block] = set()
    for i, block_set in block_dict.items():
        if i > 1:
            for block_i in block_set:
                list_of_who_holds = [
                    block_check
                    for block_check in block_dict.get(block_i.z[0] - 1, set())
                    if range_intercepts(block_i, block_check)
                ]
                if len(list_of_who_holds) == 1:
                    set_who_single_holds.add(list_of_who_holds[0])
    return set_who_single_holds


def count_who_drops(set_who_single_holds, block_dict) -> list[int]:
    list_drops: list[int] = []
    for block_i in set_who_single_holds:
        new_block_dict = deepcopy(block_dict)
        new_block_dict[block_i.z[-1]] = new_block_dict[block_i.z[-1]] - {block_i}
        _, drops = drop_blocks(new_block_dict)
        list_drops.append(drops)

    return list_drops


dropped_blocks, _ = drop_blocks(load_blocks(lineFiles))
set_of_who_holds = count_who_single_holds(dropped_blocks)

print(f"Result of part 1 -> {len(lineFiles)- len(set_of_who_holds)}")
print(f"Result of part 2 -> {sum(count_who_drops(set_of_who_holds, dropped_blocks))}")
