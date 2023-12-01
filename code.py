from util import *
import aoc

submit = aoc.for_day()


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    pprint(locals())
    return submit.part(1, None)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    pprint(locals())
    return submit.part(2, None)


if __name__ == "__main__":
    cli()
