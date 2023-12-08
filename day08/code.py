from util import *
import aoc

submit = aoc.for_day(8)


@click.group()
def cli():
    pass


def process_line(line):
    if "=" not in line:
        return cycle(line.strip())
    else:
        return dict(process_node(s) for s in line.split("\n"))


def process_node(node):
    n, left, right = parse("{} = ({}, {})", node)
    return (n, (left, right))


def get_dist(start, end, dirs, network):
    for dir, steps in zip(dirs, count(1)):
        dest = network[start][0 if dir == "L" else 1]
        if dest.endswith(end):
            return steps
        start = dest


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    dirs, network = [process_line(l) for l in read_file(input, delim="\n\n")]

    return submit.part(1, get_dist("AAA", "ZZZ", dirs, network))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    dirs, network = [process_line(l) for l in read_file(input, delim="\n\n")]

    starts = [s for s in network if s.endswith("A")]
    dists = [get_dist(s, "Z", dirs, network) for s in starts]
    return submit.part(2, lcm(*dists))


if __name__ == "__main__":
    cli()
