from dataclasses import dataclass

with open("inputs/d24input.txt") as f:
    lineFiles = f.readlines()


@dataclass(order=True)
class hail_particle:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int
    m: float
    b: float


allHail = [
    hail_particle(
        x := int(lineSplit[0].split(",")[0]),
        y := int(lineSplit[0].split(",")[1]),
        int(lineSplit[0].split(",")[2]),
        vx := int(lineSplit[1].split(",")[0]),
        vy := int(lineSplit[1].split(",")[1]),
        int(lineSplit[1].split(",")[2]),
        m := vy / vx,
        b := y - m * x,
    )
    for line in lineFiles
    if (lineSplit := line.replace("\n", "").replace(" ", "").split("@"))
]


def intersection_calculator(hail: list[hail_particle]) -> int:
    # linear -> 1 intersection
    # x = (b2-b1)/(m1-m2)
    # y = mx+b
    res = 0
    minimumVal = 200000000000000
    maximumVal = 400000000000000

    for i, hail1 in enumerate(hail[:-1]):
        for j in range(i + 1, len(hail)):
            if hail1.m == hail[j].m:
                if hail1.b == hail[j].b:
                    res += 1
            else:
                x_int = (hail[j].b - hail1.b) / (hail1.m - hail[j].m)
                y_int = hail1.m * x_int + hail1.b
                if (
                    x_int >= minimumVal
                    and x_int <= maximumVal
                    and y_int >= minimumVal
                    and y_int <= maximumVal
                    and (x_int - hail1.x) / hail1.vx > 0
                    and (y_int - hail1.y) / hail1.vy > 0
                    and (x_int - hail[j].x) / hail[j].vx > 0
                    and (y_int - hail[j].y) / hail[j].vy > 0
                ):
                    res += 1
    return res


print(f"Result of part 1 -> {intersection_calculator(allHail)}")
