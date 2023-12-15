from util import *
import aoc

submit = aoc.for_day(15)


@click.group()
def cli():
    pass


def process_line(line):
    return re.match(r"(\w+)([=-])(\w*)", line).groups()


def do_hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = read_file(input, delim=",")
    return submit.part(1, sum(do_hash(d) for d in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input, delim=",")]
    boxes = defaultdict(dict)  # yay, ordered dicts!

    for label, op, val in data:
        if op == "=":
            boxes[do_hash(label)][label] = int(val)
        if op == "-":
            box = boxes[do_hash(label)]
            if label in box:
                del box[label]

    total = 0
    for box, lenses in boxes.items():
        for slot, focal_length in enumerate(lenses.values()):
            total += (box + 1) * (slot + 1) * focal_length

    return submit.part(2, total)


if __name__ == "__main__":
    cli()
