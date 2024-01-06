from util import *
import aoc

submit = aoc.for_day(20)


@click.group()
def cli():
    pass


def process_line(line):
    module, args = line.split(" -> ")
    op = module[0] if module.startswith(tuple("&%")) else "broadcaster"
    name = module.lstrip("&%")
    return name, op, args.split(", ")


def get_modules(input):
    data = [process_line(l) for l in read_file(input)]
    return {name: (op, args) for (name, op, args) in data}


HI = 1
LO = 0

ON = True
OFF = False


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    modules = get_modules(input)

    c = Counter()
    for _, item in run_machine(modules, max_presses=1000):
        c[item[1]] += 1
    return submit.part(1, c[HI] * c[LO])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    modules = get_modules(input)
    flip_flops = set(m for m in modules if modules[m][0] == "%")
    nands = set(m for m in modules if modules[m][0] == "&")

    # each flip flop has a "value" based on which step number it triggers
    # it triggers HI on, and these values all appear to be powers of 2
    flip_flop_value = {}
    for press_number, (src, pulse, dest) in run_machine(modules, max_presses=None):
        if src in flip_flops and pulse == HI:
            if src not in flip_flop_value:
                flip_flop_value[src] = press_number

        if len(flip_flop_value) == len(flip_flops):
            break

    # it appears each nand is either the conjunction of all flip flops or all nands
    nand_inputs = defaultdict(list)
    for src, (_, args) in modules.items():
        for name in nands:
            if name in args:
                nand_inputs[name].append(src)

    flip_flop_nands = set()
    nand_nands = set()
    for k, v in nand_inputs.items():
        if all(x in flip_flops for x in v):
            flip_flop_nands.add(k)
        elif all(x in nands for x in v):
            nand_nands.add(k)

    # and of the nands that are conjuctions of flipflops, the gate triggers
    # on the button press number corresponding to the sum of the flip flop values that make up its inputs
    nand_sum = {}
    for nand in flip_flop_nands:
        nand_sum[nand] = sum(flip_flop_value[ff] for ff in nand_inputs[nand])

    # and there are two inverters (single-input nands) between rx and each flip flop nand (see graphviz)
    parents = defaultdict(list)
    for src, (_, args) in modules.items():
        for arg in args:
            parents[arg].append(src)

    rx_parents = parents["rx"]
    next_level = [p for x in rx_parents for p in parents[x]]
    last_level = [p for x in next_level for p in parents[x]]
    assert set(last_level) == set(flip_flop_nands)

    # which means the answer is just when all flip flop nands trigger
    # all together. and they are all prime numbers, so...
    return submit.part(2, prod(nand_sum.values()))


@cli.command()
@click.argument("input", type=click.File())
def graphviz(input):
    modules = get_modules(input)

    print("digraph G {")
    print("  splines=ortho")
    print("  {")
    for name in modules:
        shape = {"&": "invtriangle", "%": "oval"}.get(modules[name][0], "doublecircle")
        print(f"    {name} [shape={shape}]")
    print("  }")

    for name, (op, args) in modules.items():
        args = " ".join(args)
        print(f"  {name} -> {{{args}}}")

    print("}")


def run_machine(modules, max_presses):
    flip_flop = {}
    conjunction_names = set()
    for name, (op, args) in modules.items():
        if op == "%":
            flip_flop[name] = OFF

        if op == "&":
            conjunction_names.add(name)

    conjunction = defaultdict(dict)
    for src, (_, args) in modules.items():
        for name in conjunction_names:
            if name in args:
                conjunction[name][src] = LO

    bus = []
    button_presses = range(1, max_presses + 1) if max_presses else count(1)
    for press_number in button_presses:
        bus.append(("button", LO, "broadcaster"))
        while bus:
            item = bus.pop(0)
            yield press_number, item
            source, pulse, module_name = item

            if module_name not in modules:
                continue

            op, args = modules[module_name]

            if op == "broadcaster":
                for dest in args:
                    bus.append((module_name, pulse, dest))

            if op == "%":
                if pulse == LO:
                    flip_flop[module_name] = not flip_flop[module_name]
                    next_pulse = HI if flip_flop[module_name] == ON else LO
                    for dest in args:
                        bus.append((module_name, next_pulse, dest))

            if op == "&":
                conjunction[module_name][source] = pulse
                if all(x == HI for x in conjunction[module_name].values()):
                    next_pulse = LO
                else:
                    next_pulse = HI
                for dest in args:
                    bus.append((module_name, next_pulse, dest))


if __name__ == "__main__":
    cli()
