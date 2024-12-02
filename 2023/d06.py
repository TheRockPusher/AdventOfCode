with open("2023/inputs/d06input.txt") as f:
    lineFiles = f.readlines()

td_tuple = [
    (int(time), int(distance))
    for time, distance in zip(
        lineFiles[0].split(":")[1].split(), lineFiles[1].split(":")[1].split()
    )
]

t_p2 = ""
d_p2 = ""
for tup in td_tuple:
    t_p2 += str(tup[0])
    d_p2 += str(tup[1])
td_tuple.append((int(t_p2), int(d_p2)))
# Total distance can be calculated through (Total_time*Charge_time - Charge time**2)
# possibilities = Total_time-2*Min_Charge_time+1
r = []
for td in td_tuple:
    t = 1
    D = 0
    while not D:
        d = td[0] * t - t**2
        if d > td[1]:
            D = d
        else:
            t += 1
    r.append(td[0] - 2 * t + 1)
part1 = 1
for i in r[:-1]:
    part1 *= i
print(f"Result of part 1 -> {part1}")
print(f"Result of part 2 -> {r[-1]}")
