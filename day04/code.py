from util import *
import aoc

submit = aoc.for_day(4)


@click.group()
def cli():
    pass


def process_line(line):
    card_num, winners, have = parse("Card {}: {} | {}", line)
    card_num = ints(card_num)[0]
    winners = set(ints(winners))
    have = set(ints(have))
    return card_num, winners, have


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    points = []
    for card_num, winners, have in data:
        matching = have & winners
        if matching:
            points.append(2 ** (len(matching) - 1))

    return submit.part(1, sum(points))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    prizes = {}
    for card_num, winners, have in data:
        matching = have & winners
        if matching:
            prizes[card_num] = [card_num + i + 1 for i in range(len(matching))]

    return submit.part(2, total_prizes(prizes) + len(data))


def total_prizes(prizes):
    @cache
    def sum_prizes(start_card):
        out = 0
        won = prizes.get(start_card, [])

        for card in won:
            out += sum_prizes(card)

        out += len(won)
        return out

    total = 0
    for card in prizes:
        total += sum_prizes(card)

    return total


if __name__ == "__main__":
    cli()
