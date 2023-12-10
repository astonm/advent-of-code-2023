from util import *
import aoc

submit = aoc.for_day(10)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    field = Grid.from_string(input.read())

    find_loops(field)
    start = convert_start(field)
    loop = get_loop_distances(field, start)

    return submit.part(1, max(loop.values()))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    field = Grid.from_string(input.read())

    find_loops(field)
    start = convert_start(field)
    loop = get_loop_distances(field, start)

    clear_non_loop_points(field, loop)
    fill_outside_points(field)

    pretty_print(field)
    return submit.part(2, sum(1 for v in field.walk_values() if v == "."))


N = (0, -1)
S = (0, +1)
E = (+1, 0)
W = (-1, 0)

PIPES = {
    "|": (N, S),
    "-": (E, W),
    "L": (N, E),
    "J": (N, W),
    "7": (S, W),
    "F": (S, E),
}

OPP = {
    N: S,
    S: N,
    E: W,
    W: E,
}


def find_loops(g):
    # find loops by eliminating all pieces missing a connection on some side
    while True:
        to_delete = []
        for p, v in g.walk():
            if v == "S":
                continue
            if v in PIPES:
                dirs = PIPES.get(v)
                for d in dirs:
                    q = p[0] + d[0], p[1] + d[1]
                    neighbor = g.get(q, None)
                    if neighbor == "S":
                        continue
                    if not neighbor:
                        to_delete.append(p)
                    elif neighbor not in PIPES:
                        to_delete.append(p)
                    elif OPP[d] not in PIPES[neighbor]:
                        to_delete.append(p)
        if to_delete:
            for p in to_delete:
                g.set(p, ".")
        else:
            break


def convert_start(g):
    # turn S into a regular pipe and return its position
    for p, v in g.walk():
        if v == "S":
            dirs = []
            for d in [N, S, E, W]:
                q = p[0] + d[0], p[1] + d[1]
                neighbor = g.get(q, None)
                if neighbor and neighbor in PIPES and OPP[d] in PIPES[neighbor]:
                    dirs.append(d)

            pipe = first(
                c
                for (c, pd) in PIPES.items()
                if pd == tuple(dirs) or pd == tuple(dirs[::-1])
            )

            g.set(p, pipe)
            return p


def get_loop_distances(g, s):
    dist = {s: 0}
    queue = [(s, 0)]
    while queue:
        p, l = queue.pop(0)
        pipe = g.get(p)
        for d in PIPES[pipe]:
            q = p[0] + d[0], p[1] + d[1]
            if q not in dist:
                dist[q] = l + 1
                queue.append((q, l + 1))
    return dist


def clear_non_loop_points(g, loop_points):
    for p in g.walk_coords():
        if p not in loop_points:
            g.set(p, ".")


def fill_outside_points(g):
    # flood fill from outside to label the obvious
    seen = set()
    w, h = g.width - 1, g.height - 1
    queue = [(0, 0), (w, 0), (0, h), (w, h)]
    while queue:
        p = queue.pop(0)
        g.set(p, "O")

        for d in [N, S, E, W]:
            q = p[0] + d[0], p[1] + d[1]
            if q not in seen and g.get(q, None) == ".":
                seen.add(q)
                queue.append(q)

    # even-odd walk each row to get the sneaky outsides
    # see https://en.wikipedia.org/wiki/Point_in_polygon#Ray_casting_algorithm
    for y, line in enumerate(g.lines):
        n = s = 0
        for x, v in enumerate(line):
            if v in PIPES:
                if N in PIPES[v]:
                    n += 1  # each north segment is the top half of a wall
                if S in PIPES[v]:
                    s += 1  # each south segment is the bottom half of a wall

            if v == ".":
                n_walls = min(n, s)  # completed walls require north and south parts
                outside = n_walls % 2 == 0  # even number of walls => outside
                if outside:
                    g.set((x, y), "O")


def pretty_print(g):
    g = g.copy()
    t = {
        "|": "║",
        "-": "═",
        "L": "╚",
        "J": "╝",
        "7": "╗",
        "F": "╔",
        "O": " ",
        ".": ".",
    }
    for p, v in g.walk():
        g.set(p, t.get(v, v))

    g.print()


if __name__ == "__main__":
    cli()
