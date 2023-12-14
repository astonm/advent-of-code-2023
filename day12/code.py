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
        print(p, g, ways)
        total += ways

    return submit.part(2, total)


def count_ways(pattern, groupings):
    pattern = re.sub(r"\.+", ".", pattern)  # multiple dots are as good as one
    sub_patterns = pattern.split(".")
    return do_it(sub_patterns, groupings)


def do_it(sub_patterns, groupings, lvl=0):
    if not sub_patterns:
        return 1 if not groupings else 0

    count = 0
    sub_pattern = first(sub_patterns)
    for j in range(0, len(groupings) + 1):
        if len(sub_pattern) < sum(groupings[:j]):
            break

        curr_ways = inner_count_ways(sub_pattern, groupings[:j])
        if curr_ways:
            next_ways = do_it(sub_patterns[1:], groupings[j:], lvl=lvl + 1)

            if next_ways:
                count += curr_ways * next_ways
    return count


@lru_cache(maxsize=None)
def inner_count_ways(pattern, groupings, lvl=0):
    if sum(groupings) + len(groupings) - 1 > len(pattern):
        return 0
    if not groupings:
        if "#" in pattern:
            return 0
        else:
            return 1
    if len(groupings) == 1 and "#" not in pattern:
        return max(0, len(pattern) - groupings[0] + 1)

    if pattern.count("#") > sum(groupings):
        return 0

    first_hash = pattern.find("#")
    if first_hash == -1:
        first_hash = len(pattern) - 1

    total = 0
    grouping = first(groupings)
    for i in range(min(first_hash, len(pattern) - grouping) + 1):
        at_end = i + grouping == len(pattern)
        dot_ok = not at_end and pattern[i + grouping] != "#"

        if at_end and len(groupings) == 1:
            total += 1

        if dot_ok:
            res = inner_count_ways(pattern[i + grouping + 1 :], groupings[1:])
            total += res
    return total


if __name__ == "__main__":
    cli()
