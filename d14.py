with open("inputs/d14input.txt") as f:
    lineFiles = f.readlines()


def up_pull(text: list[str]) -> list[str]:
    for i, line in enumerate(text):
        for row in range(i)[::-1]:
            new_string = "".join(
                "O" if r0 == "." and r1 == "O" else r0
                for r0, r1 in zip(text[row], text[row + 1])
            )
            new_string_plus = "".join(
                "." if r0 == "." and r1 == "O" else r1
                for r0, r1 in zip(text[row], text[row + 1])
            )
            text[row] = new_string
            text[row + 1] = new_string_plus

    return text


def count_weight(text: list[str]) -> int:
    r = 0
    for i, line in enumerate(text):
        r += (len(text) - i) * line.count("O")
    return r


moved = up_pull(lineFiles)
print(f"Result of part 1 -> {count_weight(moved)}")
