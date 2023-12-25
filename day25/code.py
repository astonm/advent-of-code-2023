from util import *
import aoc

import networkx as nx

submit = aoc.for_day(25)


@click.group()
def cli():
    pass


def process_line(line):
    component, connections = line.split(": ")
    return (component, connections.split())


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    wire_desc = [process_line(l) for l in read_file(input)]

    graph = nx.Graph()
    for node1, others in wire_desc:
        for node2 in others:
            graph.add_edge(node1, node2)

    cut_value, groups = nx.stoer_wagner(graph)
    assert cut_value == 3
    assert len(groups) == 2

    return submit.part(1, len(groups[0]) * len(groups[1]))


if __name__ == "__main__":
    cli()
