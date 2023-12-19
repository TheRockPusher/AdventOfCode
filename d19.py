from typing import NamedTuple

with open("inputs/d19input.txt") as f:
    lineFile = f.readlines()

part = NamedTuple("part", [("x", int), ("m", int), ("a", int), ("s", int)])

raw_map = lineFile[: lineFile.index("\n")]
ratings_list = lineFile[lineFile.index("\n") + 1 :]
parts_list: list[part] = []
for rating in ratings_list:
    individualRating = {
        rat.split("=")[0]: int(rat.split("=")[1])
        for rat in rating.replace("{", "").replace("}", "").split(",")
    }
    parts_list.append(
        part(
            individualRating["x"],
            individualRating["m"],
            individualRating["a"],
            individualRating["s"],
        )
    )

mapping_dict: dict[str, list[tuple[str, str | None]]] = {}
for mapping in raw_map:
    k = mapping.split("{")[0]
    val_untreated = mapping.split("{")[1].replace("}", "").replace("\n", "")
    val = [
        (process, None)
        if not any(substring in process for substring in ["<", ">", "="])
        else (process.split(":")[0], process.split(":")[1])
        for process in val_untreated.split(",")
    ]
    mapping_dict[k] = val


def process_rating_once(
    mapping_dict: dict[str, list[tuple[str, str | None]]],
    part_i: part,
    starting_node: str = "in",
) -> str:
    mapping = mapping_dict[starting_node]
    for m in mapping:
        if m[1]:
            match m[0][1]:
                case "<":
                    if part_i.__getattribute__(m[0].split("<")[0]) < int(
                        m[0].split("<")[1]
                    ):
                        return m[1]
                case ">":
                    if part_i.__getattribute__(m[0].split(">")[0]) > int(
                        m[0].split(">")[1]
                    ):
                        return m[1]
                case "=":
                    if part_i.__getattribute__(m[0].split("=")[0]) == int(
                        m[0].split("=")[1]
                    ):
                        return m[1]
        else:
            return m[0]
    return mapping[-1][0]


accepted_parts: list[part] = []
for part_i in parts_list:
    node = "in"
    while node not in ["A", "R"]:
        node = process_rating_once(mapping_dict, part_i, node)
    if node == "A":
        accepted_parts.append(part_i)

print(f"Result of part 1 -> {sum([sum([p.x, p.m, p.a, p.s]) for p in accepted_parts])}")
