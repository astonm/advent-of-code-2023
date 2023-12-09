from util import *
import aoc

submit = aoc.for_day(9)


@click.group()
def cli():
    pass


def process_line(line):
    return ints(line)


def extend(seq):
    if all(s == 0 for s in seq):
        return seq + [0]

    d = extend(deltas(seq))
    out = seq + [seq[-1] + d[-1]]

    return out


def extend_left(seq):
    if all(s == 0 for s in seq):
        return [0] + seq

    d = extend_left(deltas(seq))
    out = [seq[0] - d[0]] + seq
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(extend(seq)[-1] for seq in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(2, sum(extend_left(seq)[0] for seq in data))


if __name__ == "__main__":
    cli()
