#! /usr/bin/env python3

import argparse
import os
import csv
import errno
import sys
sys.tracebacklimit=0
from datetime import datetime


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument("amount",
                        type=int,
                        help="USD amount to adjust to Purchasing Power Parity")
    parser.add_argument("country",
                        type=str,
                        help="country to use for adjustment")
    parser.add_argument("year",
			type=str,
			nargs="?",
			default=datetime.now().year,
			help="year of reference for a stipend amounts table")

    args = parser.parse_args()

    return args


def compute_ratio(country, data):
    """
    compute PPP ratio against a default source for given country
    """
    default_source = "Netherlands"
    source_amount = int(next(x[1] for x in data if x[0] == default_source))
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
    
    if not any(input.country == row[0] for row in data):
        countries = [row[0] for row in data[1:]]
        print(f"'{input.country}' not in list. List of available countries:")
        print(*countries, sep="\n")

        return
    
    ratio = compute_ratio(input.country, data)
    output = ratio * input.amount
    print(round(output))


if __name__ == "__main__":
    main()

