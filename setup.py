"""Automatically set up file structure for a day of advent of code.
Also download necessaray exmples and input.
"""

import argparse
import datetime
import os
import typing

import requests
import bs4

DOMAIN = "adventofcode.com"
SESSION_PATH = "session.cookie"
DESCRIPTION = "Automatically download files and set up folder and files for" \
    " a day of advent of code"
TODAY = datetime.date.today()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "\
    "Gecko/20100101 Firefox/120.0"
CODE = '"""{title} ({url})\nCode for solving part {part_word}."""\n\n\ndef ' \
    'main(path: str) -> None:\n    """Implement here.\n    """\n\n\n'\
    'if __name__  == "__main__":\n    print("example:", main("{day:02}'\
    '/example{day:02}_{part}.txt"))\n    print("input:", main("{day:02}'\
    '/input{day:02}.txt"))\n'

# setup arg parser
arg_parser = argparse.ArgumentParser(description="Automatically dowsetup ")
arg_parser.add_argument("-d", "--day", choices=range(1, 26),
                        default=TODAY.day, type=int)
arg_parser.add_argument("-y", "--year", choices=range(2015, TODAY.year+1),
                        default=TODAY.year, type=int)
arg_parser.add_argument("-p", "--part", choices=range(1, 3), default=1)


def main() -> None:
    """Do setup."""
    args = arg_parser.parse_args()
    url = f"https://{DOMAIN}/{args.year}/day/{args.day}"
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
    # setup folder and files
    format_values = {
        "title": title,
        "url": url + ("#part2" if args.part == 2 else ""),
        "part_word": "one" if args.part == 1 else "two",
        "day": args.day,
        "part": args.part
    }
    os.mkdir(f"{args.day:02}")
    with open(f"{args.day:02}/puzzle{args.day:02}_{args.part}.py", "w",
              encoding="utf-8") as file:
        file.write(CODE.format_map(format_values))
    with open(f"{args.day:02}/example{args.day:02}_{args.part}.txt", "w",
              encoding="utf-8") as file:
        file.write(examples[args.part - 1])
    with open(f"{args.day:02}/input{args.day:02}.txt", "w",
              encoding="utf-8") as file:
        file.write(input_text)


if __name__ == "__main__":
    main()
