from util import *
import aoc

submit = aoc.for_day(19)


@click.group()
def cli():
    pass


Rule = fancytuple("expr dest")

NO_DEST = "NO_DEST"


def process_block(block):
    f = process_part if block.startswith("{") else process_workflow
    out = [f(l) for l in block.split("\n")]
    if f is process_workflow:
        out = dict(ChainMap(*out))
    return out


def process_workflow(line):
    name, rules = line.split("{")
    rules = (rules.rstrip("}") + ":" + NO_DEST).split(",")
    rules = [Rule(*r.split(":")) for r in rules]
    return {name: rules}


def process_part(line):
    assignments = [pair.split("=") for pair in line[1:-1].split(",")]
    return {k: int(v) for (k, v) in assignments}


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    workflows, parts = [process_block(b) for b in read_file(input, delim="\n\n")]

    def match(expr, part):
        if ">" in expr or "<" in expr:
            return eval(expr, part.copy())
        return True

    accepted = []
    for part in parts:
        state = "in"
        while state not in "AR":
            for rule in workflows[state]:
                if match(rule.expr, part, workflows):
                    if rule.dest == NO_DEST:
                        state = rule.expr
                    else:
                        state = rule.dest
                    break

        if state == "A":
            accepted.append(part)

    return submit.part(1, sum(sum(p.values()) for p in accepted))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    workflows, parts = [process_block(b) for b in read_file(input, delim="\n\n")]

    def ways(state, ranges):
        if state == "R":
            return 0

        if state == "A":
            # ranges are inclusive
            return prod(sum(r[1] - r[0] + 1 for r in rs) for rs in ranges.values())

        total = 0
        for rule in workflows[state]:
            if rule.dest == NO_DEST:
                total += ways(rule.expr, ranges)
                ranges = None
            else:
                match_ranges = {}
                other_ranges = {}
                for c in "xmas":
                    match_ranges[c], other_ranges[c] = split_range(
                        c, rule.expr, ranges[c]
                    )

                total += ways(rule.dest, match_ranges)
                ranges = other_ranges
        assert not ranges
        return total

    def split_range(c, expr, range):
        var, op, val = re.split(r"([><])", expr)

        val = int(val)
        f = {">": lambda x, y: x > y, "<": lambda x, y: x < y}[op]

        if c != var:
            return [range, range]

        match, other = [], []
        for r in range:
            if f(r[0], val) and f(r[1], val):
                match.append(r)
            elif not f(r[0], val) and not f(r[1], val):
                other.append(r)
            else:
                if op == "<":
                    match.append([r[0], val - 1])
                    other.append([val, r[1]])
                else:
                    match.append([val + 1, r[1]])
                    other.append([r[0], val])
        return match, other

    return submit.part(2, ways("in", {c: [[1, 4000]] for c in "xmas"}))


if __name__ == "__main__":
    cli()
