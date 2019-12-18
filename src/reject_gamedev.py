import requests
import time
import argparse
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')

args = parser.parse_args()


def get_soup(url):
    time.sleep(5)
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


explicit_list = ['game-engine', 'gamedev', 'emulator', 'library']


def is_explicit(soup):
    if not explicit_list:
        return False
    tags = [x.get_text() for x in soup.select('a.topic-tag')]
    for tag in tags:
        if tag in explicit_list:
            return True
    return False


repos_list = []

with open(args.input) as f:
    for line in tqdm(f.readlines()):
        try:
            soup = get_soup(line)
            if is_explicit(soup):
                continue
            repos_list.append(line)
        except:
            pass

with open(args.output, 'w') as f:
    f.write('\n'.join(repos_list))
