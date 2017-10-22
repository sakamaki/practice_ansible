#!/usr/bin/env python

import re
import os

import requests
from bs4 import BeautifulSoup

URL = "http://www.boxofficemojo.com/yearly/chart/?yr=2017&p=.htm"
DEST_PATH = "/usr/share/nginx/html/"
FILE_NAME = "2017_us_boxoffice.tsv"


def main():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    with open(os.path.join(DEST_PATH, FILE_NAME), "w") as f:
        f.write("rank\ttitle\ttotal gross\n")
        for r in soup.find_all('tr', bgcolor=re.compile('#fffff|#f4f4ff'))[:-1]:
            f.write("{0[0]}\t{0[1]}\t{0[3]}\n".format(
                [r.text for r in r.find_all('font')])
            )


if __name__ == "__main__":
    main()
