from util import *
import aoc

submit = aoc.for_day(14)


@click.group()
def cli():
    pass


def process_line(line):
    return line


TILTS = {
    "N": ((0, -1), 1),
    "S": ((0, +1), -1),
    "W": ((-1, 0), 1),
    "E": ((+1, 0), -1),
}


def tilt(grid, dir):
    delta, order = TILTS[dir]
    points = list(grid.walk())[::order]

    for p, v in points:
        if v == "O":
            q = p
            while grid.get((q[0] + delta[0], q[1] + delta[1]), "") == ".":
                q = q[0] + delta[0], q[1] + delta[1]
            grid.set(p, ".")
            grid.set(q, "O")


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid.from_string(input.read())
    tilt(grid, "N")
    return submit.part(1, sum(grid.height - p[1] for p, v in grid.walk() if v == "O"))


def to_s(grid):
    return "\n".join("".join(l) for l in grid.lines)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid.from_string(input.read())
    target = 1_000_000_000

    seen = {}
    loop_len = inf
    for cycle in count(1):
        for dir in "NWSE":
            tilt(grid, dir)

        s = to_s(grid)
        if s in seen:
            loop_len = cycle - seen[s]
        seen[s] = cycle

        if cycle > loop_len * 2:
            break

    target_ind = target % loop_len
    for s, v in seen.items():
        if v % loop_len == target_ind:
            found = Grid.from_string(s)

    return submit.part(2, sum(found.height - p[1] for p, v in found.walk() if v == "O"))


if __name__ == "__main__":
    cli()
