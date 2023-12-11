from util import *
import aoc

submit = aoc.for_day(11)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    universe = Grid.from_string(input.read())
    galaxies = list(expand(universe))
    all_dists = pairwise_dists(galaxies)
    return submit.part(1, sum(all_dists.values()))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    universe = Grid.from_string(input.read())
    galaxies = list(expand(universe, factor=1000000))
    all_dists = pairwise_dists(galaxies)
    return submit.part(2, sum(all_dists.values()))


def expand(universe, factor=2):
    expand_rows = []
    for i, row in enumerate(universe.lines):
        if all(c == "." for c in row):
            expand_rows.append(i)

    expand_cols = []
    for i, col in enumerate(zip(*universe.lines)):
        if all(c == "." for c in col):
            expand_cols.append(i)

    for (x, y), v in universe.walk():
        if v == "#":
            x += sum(factor - 1 for n in expand_cols if n < x)
            y += sum(factor - 1 for n in expand_rows if n < y)
            yield (x, y)


def pairwise_dists(pts):
    out = {}
    for i, start in enumerate(pts):
        for end in pts[i + 1 :]:
            out[(start, end)] = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return out


if __name__ == "__main__":
    cli()
