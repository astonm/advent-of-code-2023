from util import *
import aoc

submit = aoc.for_day(12)


@click.group()
def cli():
    pass


def process_line(line):
    pattern, groupings = line.split()
    return pattern, tuple(ints(groupings))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(count_ways(p, g) for p, g in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    total = 0
    for p, g in data:
        repeats = 5
        ps = "".join([p + "?" for i in range(repeats - 1)]) + p
        gs = g * repeats

        ways = count_ways(ps, gs)
        total += ways
    return submit.part(2, total)


@lru_cache(maxsize=None)
def count_ways(pattern, groupings, lvl=0):
    if not groupings:
        return 0 if "#" in pattern else 1

    first_hash = pattern.find("#")
    if first_hash == -1:
        first_hash = len(pattern) - 1

    total = 0
    grouping = first(groupings)
    for i in range(min(first_hash, len(pattern) - grouping) + 1):
        covered_pattern = pattern[i : i + grouping]
        if "." in covered_pattern:
            continue

        at_end = i + grouping == len(pattern)
        dot_ok = not at_end and pattern[i + grouping] != "#"

        if at_end and len(groupings) == 1:
            total += 1

        if dot_ok:
            total += count_ways(pattern[i + grouping + 1 :], groupings[1:])

    return total


if __name__ == "__main__":
    cli()
