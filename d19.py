from typing import NamedTuple

with open("inputs/test.txt") as f:
    lineFile = f.readlines()

part = NamedTuple("part", [("x", int), ("m", int), ("a", int), ("s", int)])
ranger = NamedTuple(
    "ranger", [("x", range), ("m", range), ("a", range), ("s", range), ("mapping", str)]
)

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


def range_returner(rng: ranger, fun: tuple[str, str]) -> tuple[ranger, ranger]:
    mapping = fun[1]
    match fun[0][1]:
        case "<":
            match fun[0][0]:
                case "x":
                    main_ranger = ranger(
                        rng.x[: int(fun[0].split("<")[1]) - rng.x[0]],
                        rng.m,
                        rng.a,
                        rng.s,
                        mapping,
                    )
                    compliment_ranger = ranger(
                        rng.x[int(fun[0].split("<")[1]) - rng.x[0] :],
                        rng.m,
                        rng.a,
                        rng.s,
                        mapping,
                    )
                case "m":
                    main_ranger = ranger(
                        rng.x,
                        rng.m[: int(fun[0].split("<")[1]) - rng.m[0]],
                        rng.a,
                        rng.s,
                        mapping,
                    )
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m[int(fun[0].split("<")[1]) - rng.m[0] :],
                        rng.a,
                        rng.s,
                        mapping,
                    )
                case "a":
                    main_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a[: int(fun[0].split("<")[1]) - rng.a[0]],
                        rng.s,
                        mapping,
                    )
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a[int(fun[0].split("<")[1]) - rng.a[0] :],
                        rng.s,
                        mapping,
                    )
                case "s":
                    main_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a,
                        rng.s[: int(fun[0].split("<")[1]) - rng.s[0]],
                        mapping,
                    )
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a,
                        rng.s[int(fun[0].split("<")[1]) - rng.s[0] :],
                        mapping,
                    )

        case ">":
            match fun[0][0]:
                case "x":
                    compliment_ranger = ranger(
                        rng.x[: int(fun[0].split(">")[1]) - rng.x[0]],
                        rng.m,
                        rng.a,
                        rng.s,
                        mapping,
                    )
                    main_ranger = ranger(
                        rng.x[int(fun[0].split(">")[1]) - rng.x[0] :],
                        rng.m,
                        rng.a,
                        rng.s,
                        mapping,
                    )
                case "m":
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m[: int(fun[0].split(">")[1]) - rng.m[0]],
                        rng.a,
                        rng.s,
                        mapping,
                    )
                    main_ranger = ranger(
                        rng.x,
                        rng.m[int(fun[0].split(">")[1]) - rng.m[0] :],
                        rng.a,
                        rng.s,
                        mapping,
                    )
                case "a":
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a[: int(fun[0].split(">")[1]) - rng.a[0]],
                        rng.s,
                        mapping,
                    )
                    main_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a[int(fun[0].split(">")[1]) - rng.a[0] :],
                        rng.s,
                        mapping,
                    )
                case "s":
                    compliment_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a,
                        rng.s[: int(fun[0].split(">")[1]) - rng.s[0]],
                        mapping,
                    )
                    main_ranger = ranger(
                        rng.x,
                        rng.m,
                        rng.a,
                        rng.s[int(fun[0].split(">")[1]) - rng.s[0] :],
                        mapping,
                    )

    return main_ranger, compliment_ranger


def range_splitter(
    mapping_dict: dict[str, list[tuple[str, str | None]]], ranges: list[ranger]
) -> list[ranger]:
    res: list[ranger] = []
    for ranger_i in ranges:
        main_ranger = ranger_i
        compliment_ranger = ranger_i
        for m in mapping_dict[ranger_i.mapping]:
            if m[1]:
                main_ranger, compliment_ranger = range_returner(compliment_ranger, m)
            else:
                main_ranger = ranger(
                    compliment_ranger.x,
                    compliment_ranger.m,
                    compliment_ranger.a,
                    compliment_ranger.s,
                    m[0],
                )

            res.append(main_ranger)
    return res


accepted_parts: list[part] = []
for part_i in parts_list:
    node = "in"
    while node not in ["A", "R"]:
        node = process_rating_once(mapping_dict, part_i, node)
    if node == "A":
        accepted_parts.append(part_i)

print(f"Result of part 1 -> {sum([sum([p.x, p.m, p.a, p.s]) for p in accepted_parts])}")


start_range = ranger(
    range(0, 5000), range(0, 5000), range(0, 5000), range(0, 5000), "in"
)
ranger_list = [start_range]
accepted_list: list[ranger] = []
while ranger_list:
    ranger_list = range_splitter(mapping_dict, ranger_list)
    accepted_list.extend([r for r in ranger_list if r.mapping == "A"])
    ranger_list = [r for r in ranger_list if r.mapping not in ["A", "R"]]
print(f"{sum([len(r.x)*len(r.s)*len(r.a)*len(r.m) for r in accepted_list])}")
print("167409079868000")

# 299176363191761  too high
