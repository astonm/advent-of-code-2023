from util import *
import aoc

submit = aoc.for_day(16)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@dataclass
class Beam:
    p: tuple
    d: tuple


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid.from_string(input.read())
    return submit.part(1, num_activated_tiles(grid, Beam((0, 0), (1, 0))))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid.from_string(input.read())

    edge_beams = []
    for y in [0, grid.height - 1]:
        for x in range(0, grid.width):
            edge_beams.append(
                Beam(
                    p=(x, y),
                    d=(0, 1) if y == 0 else (0, -1),
                ),
            )
    for x in [0, grid.width - 1]:
        for y in range(0, grid.height):
            edge_beams.append(
                Beam(
                    p=(x, y),
                    d=(1, 0) if x == 0 else (-1, 0),
                ),
            )

    return submit.part(2, max(num_activated_tiles(grid, b) for b in edge_beams))


def num_activated_tiles(grid, start_beam):
    beams = [start_beam]
    activated = set()
    seen = set()

    while beams:
        beam = beams.pop(0)
        if (beam.p, beam.d) in seen:
            continue
        seen.add((beam.p, beam.d))

        try:
            c = grid.get(beam.p)
            activated.add(beam.p)
        except ValueError:
            continue

        if c == "|" and beam.d[0]:
            u = Beam((beam.p[0], beam.p[1] - 1), (0, -1))
            d = Beam((beam.p[0], beam.p[1] + 1), (0, 1))
            beams.extend([u, d])
            continue

        if c == "-" and beam.d[1]:
            l = Beam((beam.p[0] - 1, beam.p[1]), (-1, 0))
            r = Beam((beam.p[0] + 1, beam.p[1]), (1, 0))
            beams.extend([l, r])
            continue

        if c == "/":
            beam.d = -beam.d[1], -beam.d[0]
        if c == "\\":
            beam.d = beam.d[1], beam.d[0]

        beam.p = beam.p[0] + beam.d[0], beam.p[1] + beam.d[1]
        beams.append(beam)

    return len(activated)


if __name__ == "__main__":
    cli()
