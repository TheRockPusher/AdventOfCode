from typing import NamedTuple

with open("inputs/d18input.txt") as f:
    lineFile = f.readlines()

dig_step = NamedTuple("dig_step", [("direction", str), ("stepsN", int), ("color", str)])

dig_step_list = [
    dig_step(
        step.split()[0],
        int(step.split()[1]),
        step.split()[2].replace("\n", "").replace("(", "").replace(")", ""),
    )
    for step in lineFile
]


# Calculate total area following the shoelace formula
# https://en.wikipedia.org/wiki/Shoelace_formula
def polygon_areas(steps_list: list[dig_step]) -> tuple[int, int]:
    current_y = 0
    area = 0
    circumference = 0
    for step in steps_list:
        match step.direction:
            case "R":
                area += step.stepsN * current_y
            case "L":
                area -= step.stepsN * current_y
            case "U":
                current_y += step.stepsN
            case "D":
                current_y -= step.stepsN
        circumference += step.stepsN

    return area, circumference


# Maybe picks?
area, circumference = polygon_areas(dig_step_list)
print(f"Result of part 1 -> {area+circumference/2+1}")


def get_dir(n: int) -> str:
    match n:
        case 0:
            return "R"
        case 1:
            return "D"
        case 2:
            return "L"
        case 3:
            return "U"
    return ""


dig_step_trans = [
    dig_step(get_dir(int(step.color[-1])), int(step.color[1:-1], 16), step.color)
    for step in dig_step_list
]

areaP2, circumferenceP2 = polygon_areas(dig_step_trans)
print(f"Result of part 2 -> {areaP2+circumferenceP2/2+1}")
