from util import *
import aoc

submit = aoc.for_day(7)


RANKS = dict(list(zip("A, K, Q, J, T".split(", "), [14, 13, 12, 11, 10])))


@click.group()
def cli():
    pass


def process_line(line):
    hand, bid = parse("{} {:d}", line)
    hand = [int(RANKS.get(c, c)) for c in hand]
    return hand, bid


def hand_score(hand, j_for_joker=False):
    non_jokers = hand if not j_for_joker else [c for c in hand if c != RANKS["J"]]
    counts = sorted(Counter(non_jokers).values(), reverse=True)
    jokers = 5 - len(non_jokers)

    if jokers == 5:
        return 7, hand
    else:
        counts[0] += jokers

    if counts[0] == 5:
        return 7, hand
    if counts[0] == 4:
        return 6, hand
    if counts == [3, 2]:
        return 5, hand
    if counts[0] == 3:
        return 4, hand
    if counts[:2] == [2, 2]:
        return 3, hand
    if counts[0] == 2:
        return 2, hand
    if counts[0] == 1:
        return 1, hand

    assert 0, f"bad {counts=}"


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    data.sort(key=lambda d: hand_score(d[0]))

    return submit.part(1, sum(n * d[1] for (n, d) in zip(count(1), data)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    RANKS["J"] = 1
    data = [process_line(l) for l in read_file(input)]
    data.sort(key=lambda d: hand_score(d[0], j_for_joker=True))

    return submit.part(2, sum(n * d[1] for (n, d) in zip(count(1), data)))


if __name__ == "__main__":
    cli()
