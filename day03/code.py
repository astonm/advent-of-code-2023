from util import *
import aoc

submit = aoc.for_day(3)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    g = Grid(data)

    number_coords = []
    for y, line in enumerate(data):
        for match in re.finditer(r"\d+", line):
            number = match.group(0)
            coords = [(x, y) for x in range(match.start(), match.end())]
            number_coords.append((number, coords))

    part_nums = []
    for number, coords in number_coords:
        if list(adjacent_symbols(g, coords)):
            part_nums.append(int(number))

    return submit.part(1, sum(part_nums))


def adjacent_symbols(g, coords):
    for coord in coords:
        for neighbor in g.neighbors(coord, diags=True):
            symbol = g.get(neighbor, ".")
            if symbol != "." and not symbol.isdigit():
                yield symbol, neighbor


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    g = Grid(data)

    number_coords = []
    for y, line in enumerate(data):
        for match in re.finditer(r"\d+", line):
            number = match.group(0)
            coords = [(x, y) for x in range(match.start(), match.end())]
            number_coords.append((number, coords))

    numbers = {}  # by first coord
    numbers_near_gear = defaultdict(set)  # gear coord -> first coord of number
    for number, coords in number_coords:
        numbers[first(coords)] = int(number)
        gears = [p for c, p in adjacent_symbols(g, coords) if c == "*"]
        for gear in gears:
            numbers_near_gear[gear].add(first(coords))

    gear_ratios = []
    for first_coords in numbers_near_gear.values():
        if len(first_coords) == 2:
            gear_ratios.append(prod(numbers[x] for x in first_coords))

    return submit.part(2, sum(gear_ratios))


if __name__ == "__main__":
    cli()
