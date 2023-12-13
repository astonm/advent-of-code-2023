from util import *
import aoc

submit = aoc.for_day(12)


@click.group()
def cli():
    pass


def process_line(line):
    pattern, groupings = line.split()
    return pattern, ints(groupings)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(count_ways(p, g) for p, g in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    pass


def match(pat, seq):
    for p, s in zip(pat, seq):
        if p == "?":
            continue
        if p != s:
            return False
    return True


@lru_cache(maxsize=None)
def generate_filler(total_sum, divisions):
    if divisions == 1:
        return [[total_sum]]

    out = []
    for i in range(0, total_sum + 1):
        o = [i]
        for r in generate_filler(total_sum - i, divisions - 1):
            out.append(o + r)

    return out


def generate_shapes(groupings, length):
    for filler in generate_filler(length - sum(groupings), len(groupings) + 1):
        if 0 in filler[1:-1]:  # non-zero between
            continue

        out = [""] * (2 * len(groupings) + 1)
        out[::2] = ["." * f for f in filler]
        out[1::2] = [g * "#" for g in groupings]
        yield "".join(out)


def count_ways(pattern, groupings):
    c = 0
    for shape in generate_shapes(groupings, len(pattern)):
        if match(pattern, shape):
            c += 1
    return c


if __name__ == "__main__":
    cli()
