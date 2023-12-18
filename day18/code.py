from util import *
import aoc

submit = aoc.for_day(18)


@click.group()
def cli():
    pass


def process_line(line):
    return parse("{} {:d} (#{})", line)


DIRS = {
    "R": Vector([+1, 0]),
    "L": Vector([-1, 0]),
    "D": Vector([0, +1]),
    "U": Vector([0, -1]),
}


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    grid = GridN(default=" ")

    p = Vector([0, 0])
    grid.set(p, "#")
    for dir, dist, color in data:
        for _ in range(1, dist + 1):
            p += DIRS[dir]
            grid.set(p, "#")

    line_area = sum(1 for _, v in grid.walk() if v == "#")

    inside = Vector([1, 1])  # cheating a little
    flood_fill(grid, inside)

    grid.print(axis_order=(1, 0))

    return submit.part(1, sum(1 for _, v in grid.walk() if v == "#"))


def flood_fill(grid, start):
    q = [start]
    seen = set()
    while q:
        p = q.pop()
        if grid.get(p) in "#":
            continue

        grid.set(p, "#")
        for delta in DIRS.values():
            next_p = p + delta
            if tuple(next_p) not in seen:
                seen.add(tuple(next_p))
                q.append(next_p)


@dataclass
class Line:
    p0: Vector
    p1: Vector

    def __init__(self, start, end):
        self.p0 = start
        self.p1 = end

    def length(self):
        diff = self.p0 - self.p1
        return abs(diff[0]) + abs(diff[1])

    @property
    def horizontal(self):
        return self.p0[1] == self.p1[1]

    @property
    def vertical(self):
        return not self.horizontal

    def wall_intersecting_y(self, y):
        if self.horizontal and self.p0[1] == y:
            xs = sorted([self.p0[0], self.p1[0]])
            return tuple(xs)

        ys = sorted([self.p0[1], self.p1[1]])
        if ys[0] < y < ys[1]:
            x = self.p0[0]
            return (x, x)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    lines = []
    p = Vector([0, 0])
    min_y, max_y = (inf, -inf)
    for _, _, color in data:
        dir = {"0": "R", "1": "D", "2": "L", "3": "U"}[color[-1]]
        dist = int(color[:-1], 16)

        next_p = p + DIRS[dir] * dist
        lines.append(Line(p, next_p))

        min_y = min(min_y, next_p[1])
        max_y = max(max_y, next_p[1])

        p = next_p

    lines.sort(key=lambda l: l.p0)

    area = 0
    for line in lines:
        area += line.length()

    vline_other_by_endpoint = {}
    for line in lines:
        if line.vertical:
            vline_other_by_endpoint[tuple(line.p0)] = line.p1
            vline_other_by_endpoint[tuple(line.p1)] = line.p0

    for y in tqdm(range(min_y, max_y)):
        walls = []
        for line in lines:
            wall = line.wall_intersecting_y(y)
            if wall is not None:
                if line.horizontal:
                    left = vline_other_by_endpoint[tuple(line.p0)]
                    right = vline_other_by_endpoint[tuple(line.p1)]

                    left_up = left[1] > y
                    right_up = right[1] > y
                    switch = left_up != right_up

                if line.vertical:
                    switch = True

                walls.append((wall, switch))

        walls.sort()

        inside = False
        for wall1, wall2 in pairwise(walls):
            start, switch = wall1
            end, _ = wall2

            if switch:
                inside = not inside

            if inside:
                area += end[0] - start[1] - 1

    return submit.part(2, area)


if __name__ == "__main__":
    cli()
