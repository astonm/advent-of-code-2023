from util import *
import aoc

submit = aoc.for_day(2)


@click.group()
def cli():
    pass


def process_line(line):
    game_id, draws = parse("Game {}: {}", line)
    draws = draws.split("; ")
    draws = [d.split(", ") for d in draws]
    draws = [[c.split() for c in d] for d in draws]
    return int(game_id), [Counter({x[1]: int(x[0]) for x in d}) for d in draws]


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    target = Counter(red=12, green=13, blue=14)
    good_games = []
    for game_id, draws in data:
        for draw in draws:
            left = Counter(target)  # copy
            left.subtract(draw)  # mutate

            if any(v < 0 for v in left.values()):
                break
        else:
            good_games.append(game_id)

    return submit.part(1, sum(good_games))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    powers = []
    for game_id, draws in data:
        min_count = defaultdict(int)
        for draw in draws:
            for color, count in draw.items():
                min_count[color] = max(min_count[color], count)

        powers.append(prod(min_count.values()))

    return submit.part(2, sum(powers))


if __name__ == "__main__":
    cli()
