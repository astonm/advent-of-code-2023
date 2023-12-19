from util import *
import aoc

submit = aoc.for_day(17)


@click.group()
def cli():
    pass


DIRS = {
    "R": (+1, 0),
    "D": (0, +1),
    "L": (-1, 0),
    "U": (0, -1),
}


OPP = {"U": "D", "D": "U", "L": "R", "R": "L"}


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    map = Grid.from_string(input.read())
    submit.part(1, find_path(map))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    map = Grid.from_string(input.read())
    submit.part(2, find_path(map, min_dist=4, max_dist=10))


def find_path(map, min_dist=1, max_dist=3):
    start = (0, 0)
    dest = (map.width - 1, map.height - 1)

    q = PriorityQueue()
    q.put((0, start, tuple()))

    seen = set()
    visited_links = set()
    with tqdm(total=map.width * map.height) as progress:
        while not q.empty():
            cost, p, path = q.get()

            if p not in seen:
                progress.update()
                seen.add(p)

            if p == dest:
                return cost

            for dir, d in DIRS.items():
                prev_dir = path[-1][0] if path else None

                if prev_dir == dir:
                    continue
                if prev_dir == OPP[dir]:
                    continue

                next_p = p
                next_cost = cost
                for dist in range(1, max_dist + 1):
                    next_p = next_p[0] + d[0], next_p[1] + d[1]
                    try:
                        next_cost += int(map.get(next_p))
                    except ValueError:
                        break

                    if dist < min_dist:
                        continue

                    next_path = path + (dir * dist,)
                    if (p, next_p) not in visited_links:
                        visited_links.add((p, next_p))

                        q.put(
                            (
                                next_cost,
                                next_p,
                                next_path,
                            )
                        )


if __name__ == "__main__":
    cli()
