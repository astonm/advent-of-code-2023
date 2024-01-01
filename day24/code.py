from util import *
import aoc
import numpy

submit = aoc.for_day(24)


@click.group()
def cli():
    pass


def process_line(line):
    pos, vel = line.split(" @ ")
    pos = Vector([int(x) for x in pos.split(", ")])
    vel = Vector([int(x) for x in vel.split(", ")])
    return pos, vel


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    window = (200000000000000, 400000000000000) if "input" in input.name else (7, 27)

    c = 0
    for i, x in enumerate(data):
        for y in data[i + 1 :]:
            if p := intersection_xy(x, y):
                in_window = all(window[0] <= p[i] <= window[1] for i in range(2))
                tx = (p[0] - x[0][0]) / x[1][0]
                ty = (p[0] - y[0][0]) / y[1][0]

                if in_window and tx > 0 and ty > 0:
                    c += 1

    return submit.part(1, c)


@cli.command()
@click.argument("input", type=click.File())
def part2_example(input):
    assert "ex" in input.name, "only works for the example input"
    data = [process_line(l) for l in read_file(input)]

    special, other = find_special_lines(
        data, test=lines_parallel if "ex" in input.name else lines_intersect
    )

    plane = plane_from_lines(special[0], special[1])
    p0 = intersect_plane_and_line(plane, other[0])
    p1 = intersect_plane_and_line(plane, other[1])
    rock_vel = p1 - p0

    t = get_time_to(other[0], special[0], rock_vel)
    collide_point = other[0][0] + t * other[0][1]
    rock_pos = collide_point - t * rock_vel

    print(sum(rock_pos))


def xgcd(a, b):
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
    return a, prevx, prevy


def round_int(n):
    if abs(n - int(round(n))) < 1e-8:
        return int(round(n))
    return n


def vector_mag(v):
    return abs(v[0]) + abs(v[1]) + abs(v[2])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    vmax = 5
    for rock_vel in tqdm(
        sorted(product(range(-vmax, vmax + 1), repeat=3), key=vector_mag)
    ):
        if rock_vel == (0, 0, 0):
            continue

        pdiffs = []
        vcoeffs = []
        for (i, h0), (j, h1) in pairwise(enumerate(data)):
            for dim in range(3):
                pdiffs.append([h0[0][dim] - h1[0][dim]])

                vc = [0] * 5
                vc[i] = rock_vel[dim] - h0[1][dim]
                vc[j] = h1[1][dim] - rock_vel[dim]
                vcoeffs.append(vc)

        res = numpy.linalg.lstsq(vcoeffs, pdiffs, rcond=None)[0]
        ts = [round_int(val[0]) for val in res]

        if all(type(x) is int for x in ts) and any(x > 0 for x in ts):
            print(rock_vel, ts)


def intersection_xy(hail1, hail2):
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    x1, y1, _ = hail1[0]
    x2, y2, _ = hail1[0] + hail1[1]
    x3, y3, _ = hail2[0]
    x4, y4, _ = hail2[0] + hail2[1]

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if not denom:
        return None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return px, py


def dotp(a, b):
    return sum(a * b)


def crossp(a, b):
    # https://en.wikipedia.org/wiki/Cross_product#Computing
    return Vector(
        [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]
    )


def find_special_lines(lines, test):
    special_inds = set()
    for i, l1 in enumerate(lines):
        for j, l2 in enumerate(lines):
            if i != j:
                if test(l1, l2):
                    special_inds.add(i)

    special = [l for i, l in enumerate(lines) if i in special_inds]
    other = [l for i, l in enumerate(lines) if i not in special_inds]

    return special, other


def zero(v):
    return all(x == 0 for x in v)


def lines_parallel(l1, l2):
    return zero(crossp(l1[1], l2[1]))


def lines_intersect(l1, l2):
    # https://math.stackexchange.com/a/697278
    return dotp(l1[0] - l2[0], crossp(l1[1], l2[1])) == 0


def plane_from_parallel_lines(l1, l2):
    p1, p2 = l1[0], l1[0] + l1[1]
    p3 = l2[0]

    normal = crossp((p2 - p1), (p3 - p1))
    return p1, normal


def plane_from_intersecting_lines(l1, l2):
    return l[1][0], crossp(l1[1], l2[1])


def plane_from_lines(l1, l2):
    if lines_parallel(l1, l2):
        return plane_from_parallel_lines(l1, l2)
    if lines_intersect(l1, l2):
        return plane_from_intersecting_lines(l1, l2)
    return None


def intersect_plane_and_line(plane, line):
    # https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection#Algebraic_form
    denom = dotp(line[1], plane[1])
    if not denom:
        return None
    t = int(dotp(plane[0] - line[0], plane[1]) / denom)
    return line[0] + t * line[1]


def get_time_to(target, comparison, u):
    # derivation was a real pain...
    x1, v1 = target
    x2, v2 = comparison
    t = (x2[0] - x1[0]) + (x1[1] - x2[1]) * (v2[0] - u[0]) / (v2[1] - u[1]) / (
        (v1[0] - u[0]) - (v1[1] - u[1]) * (v2[0] - u[0]) / (v2[1] - u[1])
    )
    assert t == int(t)
    return int(t)


if __name__ == "__main__":
    cli()
