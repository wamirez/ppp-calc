#! /usr/bin/env python3

import argparse
import csv
import requests
import sys
from bs4 import BeautifulSoup


def scrape_table(URL):
    """ 
    take URL containing a Google Stipend table
    and return table contents as nested list of strings
    """

    try:
        r = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    r = r.text
    soup = BeautifulSoup(r, "html.parser")
    
    # selecting the right table
    table = soup.select_one("h2:-soup-contains('Total Stipend Amount') + p + table")
        
    rows = table.find_all("tr")
    result = [[el.text for el in rows[0].find_all("th")]]
    for row in rows[1:]:
        result.append([el.text.replace("$", "") for el in row.find_all("td")])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser() 

    parser.add_argument("URL",
			type=str,
			help="URL to Google Summer of Code contributor stipend table")

    args = parser.parse_args()

    wr = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    wr.writerows(scrape_table(args.URL))

