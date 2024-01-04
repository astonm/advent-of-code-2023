import sys

import click
import time
from collections import *
from collections.abc import *
from dataclasses import *
from typing import Type
from functools import *
from itertools import *
from more_itertools import *
from parse import *
from copy import *
from math import *
from random import *
from pprint import pprint, pformat
from sys import exit, maxsize as maxint
import re
from queue import *
import json
from tqdm import tqdm
from enum import Enum, IntEnum
from varname import varname


try:
    raw_input = __builtins__["input"]
except:
    raw_input = getattr(__builtins__, "input")

try:
    dist([0], [1])
except:
    dist = lambda p, q: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def p(*a, **k):
    return print(*a, **k)


def read_file(input, delim="\n"):
    return [l.strip() for l in input.read().strip().split(delim) if l.strip()]


def count_paths(start, end, graph):
    @lru_cache(maxsize=None)
    def ways_recursive(start, end):
        c = 0
        if start == end:
            return 1
        for next_node in graph[start]:
            c += ways_recursive(next_node, end)
        return c

    return ways_recursive(start, end)


def get_paths(start, end, graph):
    @lru_cache(maxsize=None)
    def ways_recursive(start, end):
        if start == end:
            return [[end]]

        out = []
        for next_node in graph[start]:
            for way in ways_recursive(next_node, end):
                out.append([start] + way)
        return out

    return ways_recursive(start, end)


class graph_from_func:
    def __init__(self, f):
        self.f = f

    def __getitem__(self, k):
        return self.f(k)


def tree_find(start, target, tree):
    node = tree[start]
    if node["val"] == target:
        return True

    for child in node.get("next") or []:
        if tree_find(child, target, tree):
            return True


def deltas(l):
    out = []
    for i in range(1, len(l)):
        out.append(l[i] - l[i - 1])
    return out


class Grid:
    Throw = object()

    UDLR = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    DIAGS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

    def __init__(self, lines):
        self.lines = lines
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get(self, p, default=Throw):
        if 0 <= p[0] < self.width:
            if 0 <= p[1] < self.height:
                return self.lines[p[1]][p[0]]
        if default is Grid.Throw:
            raise ValueError(f"Invalid position {p}")
        else:
            return default

    def get_multi(self, ps, default=Throw):
        return [self.get(p, default) for p in ps]

    def set(self, p, val):
        self.lines[p[1]][p[0]] = val

    def neighbors(self, p, diags=False):
        deltas = Grid.UDLR
        if diags:
            deltas = deltas + Grid.DIAGS

        out = []
        for (dx, dy) in deltas:
            if 0 <= p[0] + dx < self.width:
                if 0 <= p[1] + dy < self.height:
                    out.append((p[0] + dx, p[1] + dy))

        return out

    def walk(self):
        return zip(self.walk_coords(), self.walk_values())

    def walk_values(self):
        # top to bottom, left to right
        for line in self.lines:
            for val in line:
                yield val

    def walk_coords(self):
        # top to bottom, left to right
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)

    def print(self, sep="", vsep="\n"):
        out = []
        for row in range(self.height):
            out.append(sep.join(str(x) for x in self.lines[row]))
        print(vsep.join(out))
        print(vsep)

    def copy(self):
        return Grid(deepcopy(self.lines))

    def transpose(self):
        transposed = self.copy()
        transposed.width, transposed.height = self.height, self.width
        transposed.lines = list(zip(*self.lines))
        return transposed

    def fliplr(self):
        flipped = self.copy()
        flipped.lines = [l[::-1] for l in self.lines]
        return flipped

    def flipud(self):
        flipped = self.copy()
        flipped.lines = self.lines[::-1]
        return flipped

    def __eq__(self, other):
        return self.lines == other.lines

    @staticmethod
    def from_string(s):
        lines = s.rstrip().splitlines()
        width = max(len(l) for l in lines)
        return Grid([list(l.ljust(width)) for l in lines])


class GridN:
    Throw = object()

    def __init__(self, g=None, default=Throw):
        self.g = {} if g is None else g
        self.default = default
        self._dim = None

    @property
    def dim(self):
        if not self._dim:
            self._dim = len(first(self.g))
        return self._dim

    def bounds(self):
        # inclusive
        mins = [min(self.g, key=lambda d: d[i])[i] for i in range(self.dim)]
        maxs = [max(self.g, key=lambda d: d[i])[i] for i in range(self.dim)]
        return [range(mins[i], maxs[i] + 1) for i in range(self.dim)]

    def get(self, p):
        if isinstance(p, list):
            p = tuple(p)

        if p in self.g:
            return self.g[p]

        if self.default is GridN.Throw:
            raise ValueError(f"Invalid position {p}")
        else:
            return self.default

    def get_multi(self, ps):
        return [self.get(p) for p in ps]

    def set(self, p, val):
        if isinstance(p, list):
            p = tuple(p)
        self.g[p] = val

    def unset(self, p):
        if isinstance(p, list):
            p = tuple(p)
        del self.g[p]

    def neighbors(self, p, diags=False):
        pxs = []
        if not diags:
            for cx in [-1, 1]:
                for i in range(self.dim):
                    pxs.append(tuple([0] * i + [cx] + [0] * (self.dim - i - 1)))
        else:
            for prod in product([-1, 0, 1], repeat=self.dim):
                if not all(c == 0 for c in prod):
                    pxs.append(prod)
        out = []
        for px in pxs:
            np = tuple(d + dx for (d, dx) in zip(p, px))
            if np in self.g or self.default is not GridN.Throw:
                out.append((np, self.g.get(np, self.default)))
        return out

    def walk(self):
        yield from self.g.items()

    def walk_all(self, pad=0, axis_order=None):
        assert self.default is not GridN.Throw, "No default set. Did you mean .walk()?"
        padded_bounds = [range(r.start - pad, r.stop + pad) for r in self.bounds()]

        if axis_order is None:
            axis_order = list(range(self.dim))
        axis_inverse_order = [axis_order.index(i) for i in range(self.dim)]

        ordered_bounds = [padded_bounds[i] for i in axis_order]
        for p in product(*ordered_bounds):
            p = tuple(p[i] for i in axis_inverse_order)
            yield p, self.get(p)

    def print(self, sep="", vsep="\n", axis_order=None, putc=None):
        if putc is None:
            putc = lambda c: print(c, end="", sep="")
        if axis_order is None:
            axis_order = list(range(self.dim))
            if len(axis_order) == 2:
                axis_order.reverse()  # typical for 2d grids

        bounds_size = [len(b) for b in self.bounds()]
        ordered_bounds_size = [bounds_size[i] for i in reversed(axis_order)]
        dim_prods = [prod(ordered_bounds_size[:i]) for i in range(1, len(bounds_size))]

        for i, (p, v) in enumerate(self.walk_all(axis_order=axis_order)):
            putc(v)
            for dp in dim_prods:
                if (i + 1) % dp == 0:
                    putc("\n")

    def copy(self):
        out = GridN()
        out.g = deepcopy(self.g)
        out.default = self.default
        out._dim = self._dim
        return out

    def __eq__(self, other):
        return self.g == other.g


class Vector(list):
    def _broadcast(self, other):
        if isinstance(other, Iterable):
            return zip(self, other)
        else:
            return zip(self, [other] * len(self))

    def __add__(self, other):
        return Vector([x.__add__(y) for (x, y) in self._broadcast(other)])

    def __radd__(self, other):
        return Vector([x.__radd__(y) for (x, y) in self._broadcast(other)])

    def __sub__(self, other):
        return Vector([x.__sub__(y) for (x, y) in self._broadcast(other)])

    def __rsub__(self, other):
        return Vector([x.__rsub__(y) for (x, y) in self._broadcast(other)])

    def __mul__(self, other):
        return Vector([x.__mul__(y) for (x, y) in self._broadcast(other)])

    def __rmul__(self, other):
        return Vector([x.__rmul__(y) for (x, y) in self._broadcast(other)])

    def __truediv__(self, other):
        return Vector([x.__truediv__(y) for (x, y) in self._broadcast(other)])

    def __floordiv__(self, other):
        return Vector([x.__floordiv__(y) for (x, y) in self._broadcast(other)])

    def __pow__(self, other):
        return Vector([x.__pow__(y) for (x, y) in self._broadcast(other)])

    def __neg__(self):
        return Vector(x.__neg__() for x in self)

    def __pos__(self):
        return Vector(x.__pos__() for x in self)

    def __abs__(self):
        return Vector(x.__abs__() for x in self)

    # default list operator overrides

    def __iadd__(self, other):  # override list concatenation
        for i, (x, y) in enumerate(self._broadcast(other)):
            self[i] = x.__add__(y)
        return self

    def __imul__(self, other):  # override list multiplication
        for i, (x, y) in enumerate(self._broadcast(other)):
            self[i] = x.__mul__(y)
        return self


def softconv(val, converter, default=None):
    try:
        return converter(val)
    except ValueError:
        return default


def softint(s, default=None):
    return softconv(s, int, default)


def ints(s):
    return [int(n) for n in re.findall(r"-?\d+", s)]


def first(l, default=None):
    return next(iter(l), default)


def prod(l):
    return reduce(lambda x, y: x * y, l)


def sign(n):
    if not n:
        return 0
    return -1 if n < 0 else 1


def running_sum(l):
    if not l:
        return l
    out = [l[0]]
    for x in l[1:]:
        out.append(out[-1] + x)
    return out


def lget(l, k, default=None):
    if 0 <= k < len(l):
        return l[k]
    else:
        return default


def find_ind(l, f):
    for i, x in enumerate(l):
        if f(x):
            return i
    return -1


def fancytuple(*a, **kw):
    return namedtuple(varname(), *a, **kw)


def all_factors(n):
    return set(
        reduce(
            list.__add__,
            ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0),
        )
    )


def time_it(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        dt = time.time() - ts
        print(f"timing <{f.__name__}> took: {dt:2.4f} sec")
        return result

    return wrap


def profile_it():
    import cProfile
    import pstats
    import io
    import atexit

    print("Profiling...")
    pr = cProfile.Profile()
    pr.enable()

    def exit():
        pr.disable()
        print("Profiling completed")
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats()
        print(s.getvalue())

    atexit.register(exit)
