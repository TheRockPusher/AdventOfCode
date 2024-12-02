from dataclasses import dataclass

from sympy import Symbol, solve

with open("2023/inputs/d24input.txt") as f:
    lineFiles = f.readlines()


@dataclass(order=True)
class hail_particle:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int
    m: float = 0
    b: float = 0

    def __post_init__(self):
        self.m = self.vy / self.vx if self.vx != 0 else 0
        self.b = self.y - self.m * self.x


allHail = [
    hail_particle(
        x := int(lineSplit[0].split(",")[0]),
        y := int(lineSplit[0].split(",")[1]),
        int(lineSplit[0].split(",")[2]),
        vx := int(lineSplit[1].split(",")[0]),
        vy := int(lineSplit[1].split(",")[1]),
        int(lineSplit[1].split(",")[2]),
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


# we can design a set of 9 equations for 9 incognitos
# between the rock and the hail at 3 different times
def solve_system(hail1: hail_particle, hail2: hail_particle, hail3: hail_particle):
    Xr = Symbol("Xr")
    Yr = Symbol("Yr")
    Zr = Symbol("Zr")
    t1 = Symbol("t1")
    t2 = Symbol("t2")
    t3 = Symbol("t3")
    VXr = Symbol("VXr")
    VYr = Symbol("VYr")
    VZr = Symbol("VZr")

    result = solve(
        [
            Xr + VXr * t1 - hail1.x - hail1.vx * t1,
            Xr + VXr * t2 - hail2.x - hail2.vx * t2,
            Xr + VXr * t3 - hail3.x - hail3.vx * t3,
            Yr + VYr * t1 - hail1.y - hail1.vy * t1,
            Yr + VYr * t2 - hail2.y - hail2.vy * t2,
            Yr + VYr * t3 - hail3.y - hail3.vy * t3,
            Zr + VZr * t1 - hail1.z - hail1.vz * t1,
            Zr + VZr * t2 - hail2.z - hail2.vz * t2,
            Zr + VZr * t3 - hail3.z - hail3.vz * t3,
        ],
        dict=True,
    )

    return result, result[0][Xr] + result[0][Yr] + result[0][Zr]


equation_result, p2_res = solve_system(allHail[0], allHail[1], allHail[2])

print(f"Result of part 2 ->  {p2_res}\nfor incognito {equation_result}")
