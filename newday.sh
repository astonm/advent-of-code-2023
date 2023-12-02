#!/bin/bash
DAY=`printf "day%02d" $1`

if [ ! -d "$DAY" ]; then
    mkdir "$DAY/"
fi

if [ ! -f "$DAY/code.py" ]; then
    cp code.py "$DAY/code.py"
    perl -pi -e "s/aoc.for_day\(\)/aoc.for_day\($1\)/" "$DAY/code.py"
fi

touch "$DAY/input.txt"
touch "$DAY/ex.txt"

echo "./run.sh $DAY part1 ex"
