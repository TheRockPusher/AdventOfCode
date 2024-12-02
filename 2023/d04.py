with open("2023/inputs/d04input.txt") as f:
    lineFiles = f.readlines()


def get_games_split(text: list[str]) -> tuple[int, dict[int, int]]:
    res_p2_dict: dict = {}
    res_p1 = 0
    for line in lineFiles:
        # p1 calc
        game = int(line.split(":")[0].split(" ")[-1])
        nums = line.split(":")[1].split("|")
        winningSet = set([int(i) for i in nums[0].split(" ") if i.isdigit()])
        chosenSet = set(
            [int(i) for i in nums[1].replace("\n", "").split(" ") if i.isdigit()]
        )
        numberHits = len(winningSet & chosenSet)
        print(numberHits)
        if numberHits > 0:
            res_p1 += 2 ** (numberHits - 1)
        # p2 calc
        res_p2_dict[game] = res_p2_dict.get(game, 0) + 1
        for i in range(game + 1, game + numberHits + 1):
            res_p2_dict[i] = res_p2_dict.get(i, 0) + res_p2_dict[game]

    return res_p1, res_p2_dict


results = get_games_split(lineFiles)
results_p1 = results[0]
print(f"Result of part 1 -> {results_p1}")
print(f"Result of part 2 -> {sum(results[1].values())}")
