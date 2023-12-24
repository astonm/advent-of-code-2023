from util import *
import aoc

submit = aoc.for_day(23)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    map = Grid.from_string(input.read())

    start = (1, 0)
    end = (map.width - 2, map.height - 1)

    return submit.part(1, longest_path(start, end, map))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    map = Grid.from_string(input.read())

    start = (1, 0)
    end = (map.width - 2, map.height - 1)

    graph = grid_to_graph(start, end, map, use_arrows=False)
    longest = 0
    for path in all_paths(graph, start, end):
        dist = sum(graph[x][y] for (x, y) in pairwise(path))
        longest = max(longest, dist)

    return submit.part(2, longest)


CDIR = {
    "v": (0, +1),
    "^": (0, -1),
    "<": (-1, 0),
    ">": (+1, 0),
}


def longest_path(start, end, map, steep=True):
    longest = 0
    q = [(start, 0, set())]

    while q:
        p, steps, seen = q.pop(0)
        if p == end:
            longest = max(longest, steps)
            continue

        c = map.get(p)
        if c in CDIR and steep:
            possible_dirs = [CDIR[c]]
        else:
            possible_dirs = CDIR.values()

        for d in possible_dirs:
            next_p = p[0] + d[0], p[1] + d[1]
            next_steps = steps + 1
            next_seen = seen.copy()
            if next_p not in next_seen and map.get(next_p, "#") != "#":
                next_seen.add(next_p)
                q.append((next_p, next_steps, next_seen))
    return longest


def grid_points_with_options(grid, use_arrows):
    points = []
    for p, c in grid.walk():
        if c == "#":
            continue
        if c in CDIR and use_arrows:
            possible_dirs = [CDIR[c]]
        else:
            possible_dirs = CDIR.values()

        next_ps = []
        for d in CDIR.values():
            next_p = p[0] + d[0], p[1] + d[1]
            if grid.get(next_p, "#") != "#":
                next_ps.append(next_p)

        if len(next_ps) > 2:
            points.append(p)

    return points


def grid_to_graph(start, end, grid, use_arrows):
    graph_nodes = [start, end]
    graph_nodes.extend(grid_points_with_options(grid, use_arrows=use_arrows))
    graph_nodes.sort(key=lambda x: (x[1], x[0]))

    def shortest_direct_path(start, end):
        seen = set()
        q = [(start, 0)]

        while q:
            p, steps = q.pop(0)
            if p not in (start, end) and p in graph_nodes:
                continue

            if p == end:
                return steps

            c = grid.get(p)
            if c in CDIR and use_arrows:
                possible_dirs = [CDIR[c]]
            else:
                possible_dirs = CDIR.values()

            for d in possible_dirs:
                next_p = p[0] + d[0], p[1] + d[1]
                next_steps = steps + 1
                if next_p not in seen and grid.get(next_p, "#") != "#":
                    seen.add(next_p)
                    q.append((next_p, next_steps))

    graph = defaultdict(dict)
    for i, node1 in enumerate(graph_nodes):
        for node2 in graph_nodes[i + 1 :]:
            if dist := shortest_direct_path(node1, node2):
                graph[node1][node2] = dist
                graph[node2][node1] = dist

    return dict(graph)


def all_paths(graph, start, end, path=tuple()):
    path = path + (start,)

    if start == end:
        yield path
        return

    for p in graph[start]:
        if p not in path:
            for sub_path in all_paths(graph, p, end, path):
                yield sub_path


if __name__ == "__main__":
    cli()
