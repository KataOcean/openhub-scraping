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
    if r.status_code == 404:
        return None
    return BeautifulSoup(r.content, 'html.parser')


explicit_list = ['game-engine', 'gamedev', 'emulator', 'library']


def is_explicit(soup):
    if not soup:
        return True
    if not explicit_list:
        return False
    tags = [x.get_text().strip() for x in soup.select('a.topic-tag')]
    print(tags)
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
    f.write(''.join(set(repos_list)))
