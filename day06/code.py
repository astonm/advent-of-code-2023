from util import *
import aoc

submit = aoc.for_day(6)


@click.group()
def cli():
    pass


def process_line(line, space=" "):
    return ints(line.split(":")[1].replace(" ", space))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    times, dists = [process_line(l) for l in read_file(input)]
    records = zip(times, dists)

    return submit.part(1, prod(ways(time, dist) for (time, dist) in records))


def ways(time, dist):
    c = 0
    for hold in range(time + 1):
        v = hold
        t = time - hold
        d = v * t
        if d > dist:
            c += 1
    return c


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    times, dists = [process_line(l, space="") for l in read_file(input)]
    return submit.part(2, ways(times[0], dists[0]))


if __name__ == "__main__":
    cli()
