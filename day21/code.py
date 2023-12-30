from util import *
import aoc

submit = aoc.for_day(21)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid.from_string(input.read())
    n = 64 if "input" in input.name else 6

    start = first(p for (p, v) in grid.walk() if v == "S")
    grid.set(start, ".")

    return submit.part(1, len(bfs(grid, start, n)))


@cli.command()
@click.argument("input", type=click.File())
def part2_example(input):
    grid = Grid.from_string(input.read())

    start = first(p for (p, v) in grid.walk() if v == "S")
    grid.set(start, ".")

    for n in [6, 10, 50, 100, 500, 1000, 5000]:
        print(n, num_reachable(grid, start, n), len(bfs(RepeatingGrid(grid), start, n)))


def bfs(grid, start, n_steps):
    q = {start}
    for _ in range(n_steps):
        next_q = set()
        for p in q:
            for d in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                next_p = p[0] + d[0], p[1] + d[1]
                if grid.get(next_p, "#") == ".":
                    next_q.add(next_p)
        q = next_q
    return q


class RepeatingGrid:
    def __init__(self, grid):
        self.grid = grid

    def get(self, p, *a, **k):
        return self.grid.get(self.core_point(p), *a, **k)

    def core_point(self, p):
        return (p[0] % self.grid.width, p[1] % self.grid.height)


def steps_to_saturate(grid, starts, grid_loc):
    global GRID
    GRID = grid

    step_offset = min(s[1] for s in starts)
    grid_offset = grid_loc[0] * grid.width, grid_loc[1] * grid.height

    inner_starts = []
    for p, step in starts:
        p = p[0] - grid_offset[0], p[1] - grid_offset[1]
        step = step - step_offset
        inner_starts.append((p, step))

    sat_steps, res, outside_points = steps_to_saturate_inner(tuple(inner_starts))

    sat_steps += step_offset
    res = {k + step_offset: v for (k, v) in res.items()}
    outside_points = [
        ((p[0] + grid_offset[0], p[1] + grid_offset[1]), s + step_offset)
        for (p, s) in outside_points
    ]

    return sat_steps, res, outside_points


@lru_cache(maxsize=None)
def steps_to_saturate_inner(starts, DEBUG=False):
    to_start = defaultdict(list)
    for point, step in starts:
        to_start[step].append(point)
    min_start = min(to_start)

    if DEBUG:
        print(grid_loc, to_start)

    q = []
    seen = set()
    counts = {}
    answers = {}
    outside = set()

    for step in count(min_start):
        if DEBUG:
            print(f"{step=} {q=}")
            print(f"{seen=}")

        next_q = []
        for p in q:
            for d in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                next_p = p[0] + d[0], p[1] + d[1]
                try:
                    if GRID.get(next_p) == "." and next_p not in seen:
                        next_q.append(next_p)
                        seen.add(next_p)
                except ValueError:
                    outside.add((next_p, step))

        for injected_p in to_start.pop(step, []):
            if GRID.get(injected_p, ".") and injected_p not in seen:
                if DEBUG:
                    print("step", step, ", injecting", injected_p)
                next_q.append(injected_p)
                seen.add(injected_p)

        q = next_q
        counts[step] = len(seen)
        answers[step] = counts[step] - answers.get(step - 1, 0)

        recent = [answers[s] for s in range(step - 3, step + 1) if s in answers]

        if seen and len(recent) == 4 and recent[0:2] == recent[2:4]:
            return (step - 3, answers, outside)


def num_reachable(grid, start, n_steps):
    unexplored = [(start, 0)]
    complete_grids = set()
    total = 0

    while unexplored:
        by_grid = defaultdict(list)
        for p, step in unexplored:
            grid_loc = p[0] // grid.width, p[1] // grid.height
            by_grid[grid_loc].append((p, step))

        next_unexplored = []

        for grid_loc, starts in by_grid.items():
            if grid_loc in complete_grids:
                continue
            complete_grids.add(grid_loc)
            sat_steps, res, outside_points = steps_to_saturate(grid, starts, grid_loc)
            next_unexplored.extend((p, s) for (p, s) in outside_points if s <= n_steps)

            if n_steps > sat_steps:
                diff = n_steps - sat_steps
                amount = res[sat_steps] if diff % 2 == 0 else res[sat_steps + 1]
            elif n_steps in res:
                amount = res[n_steps]
            else:
                assert 0, "should never need this"

            total += amount

        unexplored = next_unexplored

    return total


##### below functions are from exploration of my input.txt specifics


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid.from_string(input.read())
    assert "input" in input.name, "only works with puzzle input"

    start = first(p for (p, v) in grid.walk() if v == "S")
    grid.set(start, ".")

    N = 26501365
    total = 0
    max_on_axis_coord = int(ceil((N - 66) / 131) + 1)

    # center
    total += calc_count(grid, (0, 0), N)

    # inner saturated
    m = max(0, max_on_axis_coord - 2) // 2
    n_inner_even = 4 * m * (m + 1)
    n_inner_odd = 4 * m * m
    odd_mult, even_mult = calc_count(grid, (0, 0), N + 1), calc_count(grid, (0, 0), N)
    total += n_inner_even * even_mult
    total += n_inner_odd * odd_mult

    # outer diamond
    for dist in range(2 * m + 1, max_on_axis_coord + 2):
        for x in range(dist + 1):
            y = dist - x
            for grid_loc in {(x, y), (-x, y), (x, -y), (-x, -y)}:
                total += calc_count(grid, grid_loc, N)

    return submit.part(2, total)


def calc_min_steps(grid_loc):
    s = abs(grid_loc[0]) + abs(grid_loc[1])

    if not s:
        return 0
    elif 0 in grid_loc:
        return 66 + 131 * (s - 1)
    else:
        return 1 + 131 * (s - 1)


def calc_sat_vals(grid_loc):
    return (7282, 7331)


def calc_sat_length(grid_loc):
    if grid_loc == (0, 0):
        return 129
    elif 0 in grid_loc:
        return 194
    else:
        return 259


def calc_sat_steps(grid_loc):
    return calc_sat_length(grid_loc) + calc_min_steps(grid_loc)


def is_touched(grid_loc, n_steps):
    return n_steps >= calc_min_steps(grid_loc)


def is_saturated(grid_loc, n_steps):
    return n_steps > calc_min_steps(grid_loc) + calc_sat_length(grid_loc)


def calc_grid_start_point(grid, grid_loc):
    s = sign(grid_loc[0]), sign(grid_loc[1])
    base = {
        (0, 0): (65, 65),
        (0, 1): (65, 0),
        (0, -1): (65, 130),
        (1, 0): (0, 65),
        (-1, 0): (130, 65),
        (1, 1): (0, 0),
        (1, -1): (0, 130),
        (-1, 1): (130, 0),
        (-1, -1): (130, 130),
    }[s]

    return (
        base[0] + grid_loc[0] * grid.width,
        base[1] + grid_loc[1] * grid.height,
    )


def calc_partial_count(grid, grid_loc, n_steps):
    sat_steps, res, outside_points = steps_to_saturate(
        grid, [(calc_grid_start_point(grid, grid_loc), 0)], grid_loc
    )
    ind = n_steps - calc_min_steps(grid_loc)
    assert ind in res
    return res[ind]


def calc_count(grid, grid_loc, n_steps):
    if not is_touched(grid_loc, n_steps):
        return 0
    elif is_saturated(grid_loc, n_steps):
        diff = n_steps - calc_sat_steps(grid_loc)
        sat_vals = calc_sat_vals(grid_loc)
        r = sat_vals[0] if diff % 2 == 0 else sat_vals[1]
        return r
    else:
        r = calc_partial_count(grid, grid_loc, n_steps)
        return r


if __name__ == "__main__":
    cli()
