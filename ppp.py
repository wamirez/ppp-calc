#! /usr/bin/env python3

import argparse
import os
import csv
import errno
import sys
sys.tracebacklimit=0
from datetime import datetime
from tabulate import tabulate


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "amount",
        type=int,
        help="amount to adjust to Purchasing Power Parity",
    )
    parser.add_argument(
        "country",
        type=str,
        nargs="?",
        help="country to use for adjustment",
    )
    parser.add_argument(
        "year",
        type=str,
        nargs="?",
        default=datetime.now().year,
        help="year of reference for a stipend amounts table",
    )
    parser.add_argument(
        "--reference", "-r",
        type=str,
        nargs="?",
        help="country to use as reference",
        default="Netherlands",
    )
    parser.add_argument(
        "--ignore", "-i",
        type=str,
        help="do not adjust the amount if the country is listed in this file"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
    )

    args = parser.parse_args()

    return args


def compute_ratio(reference, country, data):
    """
    compute PPP ratio against a default source for given country
    """
    source_amount = int(next(x[1] for x in data if x[0] == reference))
    target_amount = int(next(x[1] for x in data if x[0] == country))

    return target_amount/source_amount


def main():
    input = args()

    base = os.getcwd()
    file = f"{base}/{input.year}.csv"
    if not os.path.isfile(file):
       raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"'{input.year}.csv'. Please download a .csv file containing the stipend table amounts. Run `update.py` or see `README.md` for further instructions")
    with open(file, "r") as table:
        my_csv = csv.reader(table)
        data = [row for row in my_csv]

    if input.ignore:
        with open(input.ignore, 'r') as file:
            ignored = file.read().splitlines()

        if input.country in ignored:
            print(input.amount)
            return

    if input.all:
        eu_countries = set()
        eu_file = os.path.join(base, "european-union.txt")
        if os.path.isfile(eu_file):
            with open(eu_file, 'r') as f:
                eu_countries = set(line.strip() for line in f if line.strip())

        def calculate_amounts(country, ratio):
            if country in eu_countries:
                return round(input.amount), round(5/3 * input.amount)
            return round(input.amount * ratio), round(5/3 * input.amount * ratio)

        rows = [
            [row[0], *calculate_amounts(row[0], compute_ratio(input.reference, row[0], data))]
            for row in data[1:]
        ]
    
        print(tabulate(rows, headers=["Country", "Participant [EUR]", "Mentor [EUR]"], tablefmt="github"))
        return

    countries = [row[0] for row in data[1:]]
    if (not input.country in countries) or (not input.reference in countries):
        print(f"'{input.country}' not in list. List of available countries:")
        print(*countries, sep="\n")

        return

    ratio = compute_ratio(input.reference, input.country, data)

    output = ratio * input.amount
    print(round(output))


if __name__ == "__main__":
    main()
