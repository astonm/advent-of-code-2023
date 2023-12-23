from util import *
import aoc

submit = aoc.for_day(22)


@click.group()
def cli():
    pass


Point = fancytuple("x y z")


def process_line(line):
    parts = parse("{:d},{:d},{:d}~{:d},{:d},{:d}", line)
    p1, p2 = Point(*parts[:3]), Point(*parts[-3:])
    assert all(p2[i] >= p1[i] for i in [0, 1, 2])
    return p1, p2


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    data.sort(key=brick_height)
    settle_all(data)

    c = 0
    for i in tqdm(range(len(data))):
        test_bricks = data[:i] + data[i + 1 :]
        if not can_move(test_bricks):
            c += 1

    return submit.part(1, c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    data.sort(key=brick_height)
    settle_all(data)

    t = 0
    for i in tqdm(range(len(data))):
        test_bricks = data[:i] + data[i + 1 :]
        t += settle_all(test_bricks, show_progress=False)

    return submit.part(2, t)


def print_bricks(data):
    grid = GridN(default=".")
    for i, (c1, c2) in enumerate(data):
        letter = chr(ord("A") + i % 26)
        for x in range(c1[0], c2[0] + 1):
            for y in range(c1[1], c2[1] + 1):
                for z in range(c1[2], c2[2] + 1):
                    grid.set((x, y, z), letter)
    grid.print(axis_order=(1, 2, 0))


def collision(a, other):
    for b in other:
        if not (
            b[0].x > a[1].x
            or b[0].y > a[1].y
            or b[0].z > a[1].z
            or b[1].x < a[0].x
            or b[1].y < a[0].y
            or b[1].z < a[0].z
        ):
            return True


def drop_brick(bricks, i):
    brick = bricks[i]
    other_bricks = bricks[:i] + bricks[i + 1 :]

    assert not collision(brick, other_bricks)

    okay_brick = brick
    for dist in count(1):
        lower_brick = (
            Point(
                brick[0].x,
                brick[0].y,
                brick[0].z - dist,
            ),
            Point(
                brick[1].x,
                brick[1].y,
                brick[1].z - dist,
            ),
        )

        at_floor = 0 in (lower_brick[0].z, lower_brick[1].z)

        if not at_floor and not collision(lower_brick, other_bricks):
            okay_brick = lower_brick
        else:
            break

    bricks[i] = okay_brick
    return dist - 1


def settle_all(bricks, show_progress=True):
    num_moved = 0

    progress = tqdm if show_progress else lambda x: x

    while True:
        just_moved = False
        for i in progress(range(len(bricks))):
            dist = drop_brick(bricks, i)
            if dist > 0:
                just_moved = True
                num_moved += 1
        if not just_moved:
            break

    return num_moved


def can_move(bricks):
    for i in range(len(bricks)):
        brick = bricks[i]
        other_bricks = bricks[:i] + bricks[i + 1 :]
        lower_brick = (
            Point(
                brick[0].x,
                brick[0].y,
                brick[0].z - 1,
            ),
            Point(
                brick[1].x,
                brick[1].y,
                brick[1].z - 1,
            ),
        )

        at_floor = 0 in (lower_brick[0].z, lower_brick[1].z)
        if not at_floor and not collision(lower_brick, other_bricks):
            return True
    return False


def brick_height(b):
    return min(b[0].z, b[1].z)


if __name__ == "__main__":
    cli()
