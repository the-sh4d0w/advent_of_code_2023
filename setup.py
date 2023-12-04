"""Automatically set up file structure for a day of advent of code.
Also download necessaray examples and input.
"""

import argparse
import datetime
import os
import sys
import time
import typing

import requests
import bs4

DOMAIN = "adventofcode.com"
SESSION_PATH = "session.cookie"
TODAY = datetime.date.today()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "\
    "Gecko/20100101 Firefox/120.0"
CODE_PLACEHOLDER = '''"""{title} ({url})
Code for solving part {part_word}.
"""


def main(path: str) -> None:
    """Implement here.

    Arguments:
        - path: path to input.
    """
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()


if __name__ == "__main__":
    print("example:", main("{day:02}/example{day:02}_{part}.txt"))
    print("input:", main("{day:02}/input{day:02}.txt"))
'''

# setup arg parser
arg_parser = argparse.ArgumentParser(description="Automatically download files"
                                     " and set up folder and files for a day"
                                     " of advent of code.", epilog="Session"
                                     " cookie is expected to be in the file"
                                     f" '{SESSION_PATH}'.")
arg_parser.add_argument("-d", "--day", type=int, choices=range(1, 26),
                        metavar="DAY", default=TODAY.day,
                        help="Day of advent of code.")
arg_parser.add_argument("-y", "--year", type=int, default=TODAY.year,
                        choices=range(2015, TODAY.year+1), metavar="YEAR",
                        help="Year of advent of code.")
arg_parser.add_argument("-p", "--part", type=int, choices=range(1, 3),
                        default=1, metavar="PART", help="Part of the task.")
arg_parser.add_argument("-w", "--wait", action="store_true", default=False,
                        help="Wait until task is available.")
arg_parser.add_argument("-n", "--ntfy", default=False, help="Send "
                        "notification when finished (for use with wait).")


def main() -> None:
    """Do setup."""
    args = arg_parser.parse_args()

    # wait until release of task
    if args.wait and datetime.datetime(args.year, 12, args.day, 6) \
            > datetime.datetime.now():
        print(f"Waiting until task releases at {args.year}-12-{args.day}"
              "T06:00:00+01:00.")
        time.sleep((datetime.datetime(args.year, 12, args.day, 6)
                    - datetime.datetime.now()).total_seconds())
    url = f"https://{DOMAIN}/{args.year}/day/{args.day}"

    # exit if session cookie file doesn't exist
    if not os.path.exists(SESSION_PATH):
        sys.exit(f"The file '{SESSION_PATH}' does not exist.")

    # get session token
    with open(SESSION_PATH, "r", encoding="utf-8") as file:
        session = file.read().strip()

    # download example(s) and input
    with requests.Session() as sess:
        # set session token
        sess.cookies.set(name="session", value=session, domain=DOMAIN)
        response = sess.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        title = typing.cast(bs4.Tag, soup.find("h2")
                            ).text.replace("-", "").strip()
        examples = [typing.cast(bs4.Tag, code).text.strip()
                    for code in soup.find_all("code") if "\n" in code.text]
        input_text = sess.get(f"{url}/input").text.strip()

    # exit with error if part two not available
    if args.part == 2 and not "Part Two" in response.text:
        sys.exit("Part two is not yet available.")

    # setup folder and files
    format_values = {
        "title": title,
        "url": url + ("#part2" if args.part == 2 else ""),
        "part_word": "one" if args.part == 1 else "two",
        "day": args.day,
        "part": args.part
    }
    if not os.path.exists(f"{args.day:02}"):
        os.mkdir(f"{args.day:02}")
    with open(f"{args.day:02}/puzzle{args.day:02}_{args.part}.py", "w",
              encoding="utf-8") as file:
        file.write(CODE_PLACEHOLDER.format_map(format_values))
    with open(f"{args.day:02}/example{args.day:02}_{args.part}.txt", "w",
              encoding="utf-8") as file:
        file.write(examples[args.part - 1])
    with open(f"{args.day:02}/input{args.day:02}.txt", "w",
              encoding="utf-8") as file:
        file.write(input_text)

    # send notification
    if args.ntfy:
        requests.post(f"https://ntfy.sh/{args.ntfy}", timeout=10,
                      data=f"Part {args.part} of {args.year}-12-{args.day:02}"
                      " finished downloading.",
                      headers={"Title": "Advent of Code Setup",
                               "Priority": "urgent",
                               "Tags": "christmas_tree"})


if __name__ == "__main__":
    main()
