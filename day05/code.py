from util import *
import aoc

submit = aoc.for_day(5)


@click.group()
def cli():
    pass


def process_line(line):
    return process_group(line)


Mapping = fancytuple("start end delta")


def fill_gaps(mappings):
    out = []

    mappings.sort()

    start = 0
    for mapping in mappings:
        if mapping.start > start:
            out.append(Mapping(start=start, end=mapping.start, delta=0))
            start = mapping.start

        if mapping.start == start:
            out.append(mapping)
            start = mapping.end
        else:
            assert 0, f"unexpected state {start=}, {mapping=}"
    return out


def process_group(group):
    def to_mapping(vals):
        return Mapping(start=vals[1], end=vals[1] + vals[2], delta=vals[0] - vals[1])

    name, data = group.split(":")
    if name == "seeds":
        return ints(data)
    else:
        data = data.strip()
        key = tuple(name.replace(" map", "").split("-to-"))
        mappings = [to_mapping(ints(l)) for l in data.split("\n")]
        return {key: fill_gaps(mappings)}


SEED_TO_LOCATION_PATH = [
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location",
]


def seed_to_location(seed, mappings):
    val = seed
    for start, end in pairwise(SEED_TO_LOCATION_PATH):
        for mapping in mappings[start, end]:
            if mapping.start <= val < mapping.end:
                val += mapping.delta
                break
    return val


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input, delim="\n\n")]
    seeds = data.pop(0)

    mappings = {}
    for mapping in data:
        mappings.update(mapping)

    return submit.part(1, min(seed_to_location(seed, mappings) for seed in seeds))


def seed_to_location_mappings(seed_ranges, mappings):
    current_seed_ranges = seed_ranges

    for start, end in pairwise(SEED_TO_LOCATION_PATH):
        next_seed_ranges = []
        seed_range_q = current_seed_ranges[:]

        while seed_range_q:
            seed_range = seed_range_q.pop(0)

            for mapping in mappings[(start, end)]:  #  n^2, but could be linear
                if mapping.start <= seed_range.start + seed_range.delta < mapping.end:
                    if seed_range.end + seed_range.delta <= mapping.end:
                        # seed range totally contained in mapping
                        working_range = seed_range
                    else:
                        # left part of seed contained
                        working_range = Mapping(
                            seed_range.start,
                            mapping.end - seed_range.delta,
                            seed_range.delta,
                        )

                        # ...then requeue remainder on the right
                        remainder = Mapping(
                            mapping.end - seed_range.delta,
                            seed_range.end,
                            seed_range.delta,
                        )
                        seed_range_q.insert(0, remainder)

                    next_delta = working_range.delta + mapping.delta
                    next_seed_ranges.append(working_range._replace(delta=next_delta))
                    break
            else:
                # seed_range outside of all mappings, so leave unchanged
                next_seed_ranges.append(seed_range)

        current_seed_ranges = next_seed_ranges

    return current_seed_ranges


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input, delim="\n\n")]
    seeds = data.pop(0)

    seed_ranges = [
        Mapping(start=pair[0], end=pair[0] + pair[1], delta=0)
        for pair in grouper(seeds, 2)
    ]

    mappings = {}
    for mapping in data:
        mappings.update(mapping)

    res = seed_to_location_mappings(seed_ranges, mappings)
    smallest = min(res, key=lambda m: m.start + m.delta)

    return submit.part(2, smallest.start + smallest.delta)


if __name__ == "__main__":
    cli()
