import click
import os
import re
import requests


aoc_session = open(os.path.expanduser("~/.aoc.session")).read().strip()


YEAR = 2018
SUBMIT_URL = "https://adventofcode.com/{year}/day/{day}/answer"
HEADERS = {
    "User-Agent": "aston's AoC submitter https://github.com/astonm",
    "Cookie": f"session={aoc_session}",
}


class for_day:
    def __init__(self, day):
        self.day = day

    def part(self, level, answer):
        if answer is None:
            return
        answer = f"{answer}"

        print(f"day {self.day}, level {level}. submit answer {answer}? [Y/n]", end=" ")
        reply = input().lower() or "y"

        if reply != "y":
            return

        url = SUBMIT_URL.format(year=YEAR, day=self.day)
        res = requests.post(url, {"level": level, "answer": answer}, headers=HEADERS)
        for line in res.text.split("\n"):
            if "answer" in line or "level" in line:
                print(re.sub("<[^<]+?>", "", line))
