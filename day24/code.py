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
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    # p1 + v1 * t1 = rock_pos + t1 * rock_vel
    # p0 + v0 * t0 = rock_pos + t0 * rock_vel
    # in the case where v0 == v1 == v
    # (p1 - p0) = (rock_vel - v) * (t1 - t0), thus
    # the velocity difference and the time difference are factors of the point distance

    # to start, group by velocity and dimenstion (vx, vy, vz)
    by_vel = defaultdict(lambda: defaultdict(list))
    for p, v in data:
        for dim in range(3):
            by_vel[dim][v[dim]].append(p[dim])

    for dim in range(3):
        for k, v in by_vel[dim].copy().items():
            if len(v) < 2:
                del by_vel[dim][k]

    # then intersect all possible options for velocity together to winnow
    vel_options = {}
    for dim in range(3):
        for vel, hailstones in by_vel[dim].items():
            for p0, p1 in combinations(hailstones, 2):
                factors = all_factors(abs(p1 - p0))

                # from above, rock_vel = some_factor + v
                # negative and positive factors are valid
                options = {f + vel for f in factors} | {-f + vel for f in factors}
                options -= {0}  # zero isn't

                if dim not in vel_options:
                    vel_options[dim] = options
                else:
                    vel_options[dim] &= options
            if len(vel_options[dim]) == 1:
                break

    # there may be more than one possibility, still, though in my input i just had one
    for rock_vel in product(vel_options[0], vel_options[1], vel_options[2]):
        rock_vel = Vector(rock_vel)

        # insert razzle dazzle linear algebra...
        # i worked this out from a similar equation as above, but not assuming v1 == v0
        # t0 * (rock_vel - v0) + t1 * (v1 - rock_vel) == (p0 - p1)
        # and then i generalized to solve for all of the t's at the same time
        # i could have probably done all of the dimensions together using vectors
        # but instead i did them separately because it was easier for me to figure out
        pdiffs = []
        vcoeffs = []
        for (i, h0), (j, h1) in pairwise(enumerate(data)):
            for dim in range(3):
                pdiffs.append([h0[0][dim] - h1[0][dim]])

                vc = [0] * len(data)
                vc[i] = rock_vel[dim] - h0[1][dim]
                vc[j] = h1[1][dim] - rock_vel[dim]
                vcoeffs.append(vc)

        res = numpy.linalg.lstsq(vcoeffs, pdiffs, rcond=None)

        # the least squares solution isn't exact, but is close
        def round_int(n):
            if abs(n - int(round(n))) < 0.02:
                return int(round(n))
            else:
                return n

        ts = [round_int(val[0]) for val in res[0]]
        if all(type(x) is int for x in ts):
            p0, v0 = data[0]
            intersect0 = p0 + ts[0] * v0
            rock_pos = intersect0 - ts[0] * rock_vel
            print(rock_vel, rock_pos)
            return submit.part(2, sum(rock_pos))


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


if __name__ == "__main__":
    cli()
