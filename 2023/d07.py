with open("inputs/d07input.txt") as f:
    lineFiles = f.readlines()


def sortCards(cards: str, joker: bool = False) -> tuple[float, str]:
    five = 0
    four = 0
    three = 0
    pair = 0
    jokers = cards.count("J")
    rank: float
    newCards = cards
    if joker:
        newCards = cards.replace("J", "")
    for card in set(newCards):
        repeat = newCards.count(card)
        match repeat:
            case 5:
                five += 1
            case 4:
                four += 1
            case 3:
                three += 1
            case 2:
                pair += 1
    if five:
        rank = 4
    elif four:
        rank = 3
    elif three and pair:
        rank = 2.5
    elif three:
        rank = 2
    elif pair == 2:
        rank = 1.5
    elif pair:
        rank = 1
    else:
        rank = 0
    rankKicker = ""
    kickerDict = {"T": "a", "J": "b", "Q": "c", "K": "d", "A": "e"}
    if joker:
        kickerDict["J"] = "1"
        if jokers == 5:
            rank = 4
        else:
            rank += jokers
    for card2 in cards:
        if card2.isdigit():
            rankKicker += card2
        else:
            rankKicker += kickerDict[card2]
    return (rank, rankKicker)


cardsBet = {line.split()[0]: int(line.split()[1]) for line in lineFiles}
cardsList = list(cardsBet.keys())
cardsListJoker = sorted(cardsList, key=lambda sort: sortCards(sort, True))
cardsList.sort(key=sortCards)
part1 = 0
part2 = 0
for i, card in enumerate(cardsList):
    part1 += cardsBet[card] * (i + 1)
for j, card in enumerate(cardsListJoker):
    part2 += cardsBet[card] * (j + 1)
print(f"Result of part1 -> {part1}")
print(f"Result of part2 -> {part2}")
