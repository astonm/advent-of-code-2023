#!/bin/bash
DAY="$1"
PART="$2"
INPUT=${3:-input}
OTHER=${@:4}
export PYTHONPATH="."
export PIPENV_VERBOSITY=-1
pypy3 "$DAY/code.py" "$PART" "$DAY/$INPUT.txt" $OTHER
