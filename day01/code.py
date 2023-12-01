from util import *
import aoc

submit = aoc.for_day(1)


@click.group()
def cli():
    pass


def process_line(line):
    return [c for c in line if c in "0123456789"]


def process_line_part2(line):
    fwd = r"0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine"
    rev = fwd[::-1]

    first = re.search(fwd, line).group(0)
    last = re.search(rev, line[::-1]).group(0)[::-1]

    n = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    return [n.get(first, first), n.get(last, last)]


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum([int(c[0] + c[-1]) for c in data]))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line_part2(l) for l in read_file(input)]
    return submit.part(2, sum([int(c[0] + c[-1]) for c in data]))


if __name__ == "__main__":
    cli()
