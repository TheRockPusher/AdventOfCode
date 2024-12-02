from collections import Counter, defaultdict
from queue import Queue
from random import choices

with open("2023/inputs/d25input.txt") as f:
    lineFiles = f.readlines()


graph: dict = defaultdict(list)
for line in lineFiles:
    key = line.split(":")[0]
    listVal = line.replace("\n", "").split(":")[1].split()
    graph[key] = graph[key] + listVal
    for val in listVal:
        graph[val] = graph[val] + [key]


def random_walk(graph, rand_count):
    past_walk = Counter()
    for i in range(rand_count):
        beginning, end = choices(list(graph.keys()), k=2)
        frontier = Queue()
        frontier.put((beginning, [beginning]))
        past_nodes = set()
        while not frontier.empty():
            next, full_path = frontier.get()
            if next == end:
                for j in range(len(full_path) - 1):
                    past_walk[tuple(sorted([full_path[j], full_path[j + 1]]))] += 1
                break
            for next_possibility in graph[next]:
                if next_possibility not in past_nodes:
                    past_nodes.add(next_possibility)
                    frontier.put((next_possibility, full_path + [next_possibility]))

    return past_walk


def delete_and_count(extraneous_lines: list[tuple], graph: dict[str, list[str]]):
    for line in extraneous_lines:
        graph[line[0]].remove(line[1])
        graph[line[1]].remove(line[0])
    frontier: Queue = Queue()
    frontier.put((extraneous_lines[0][0], [extraneous_lines[0][0]]))
    past_nodes = set()
    while not frontier.empty():
        next, full_path = frontier.get()
        for next_possibility in graph[next]:
            if next_possibility not in past_nodes:
                past_nodes.add(next_possibility)
                frontier.put((next_possibility, full_path + [next_possibility]))
    return len(past_nodes)


most_common_graph_lines = [line[0] for line in random_walk(graph, 1000).most_common(3)]

circle_size = delete_and_count(most_common_graph_lines, graph)

print(
    f"Result of part 1   ->  {circle_size} * \
{len(graph)-circle_size} = {circle_size*(len(graph)-circle_size)}"
)
