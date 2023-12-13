from util import *
import aoc

submit = aoc.for_day(13)


@click.group()
def cli():
    pass


def process_line(line):
    return Grid.from_string(line)


def find_reflection_row(g):
    for i, line in enumerate(g.lines):
        if line == lget(g.lines, i + 1):
            if all(x == y for (x, y) in zip(g.lines[i::-1], g.lines[i + 1 :])):
                return i + 1


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grids = [process_line(l) for l in read_file(input, delim="\n\n")]

    total = 0
    for g in grids:
        if h := find_reflection_row(g):
            total += 100 * h
        if v := find_reflection_row(g.transpose()):
            total += v

    return submit.part(1, total)


def get_reflection_distances(g):
    for i, line in enumerate(g.lines):
        mismatches = 0
        for x, y in zip(g.lines[i::-1], g.lines[i + 1 :]):
            mismatches += sum(int(a != b) for a, b in zip(x, y))
        yield i + 1, mismatches


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grids = [process_line(l) for l in read_file(input, delim="\n\n")]

    total = 0
    for g in grids:
        if h := first(i for (i, d) in get_reflection_distances(g) if d == 1):
            total += 100 * h

        gt = g.transpose()
        if v := first(i for (i, d) in get_reflection_distances(gt) if d == 1):
            total += v
    return submit.part(2, total)


if __name__ == "__main__":
    cli()
