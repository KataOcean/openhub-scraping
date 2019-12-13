import requests
import time
import argparse
import urllib.parse
import re
import os
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--tag', default='gui')
parser.add_argument('-e', '--explicit_tags', nargs='*')

args = parser.parse_args()


def get_repos_url(relative_url):
    soup = get_soup(urllib.parse.urljoin(
        'https://www.openhub.net', relative_url + '/enlistments'))
    repos_url = soup.select_one(
        'tr.enlistment td'
    ).get_text().split()[0]
    return repos_url


def get_soup(url):
    time.sleep(5)
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def write_csv(path, list):
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    with open(path, mode='w') as f:
        f.write('\n'.join(list))


explicit_list = args.explicit_tags


def is_explicit(soup):
    if not explicit_list:
        return False
    tags = [x.get_text() for x in soup.select('a.tag')]
    for tag in tags:
        if tag in explicit_list:
            return True
    return False


print('start')

repos_list = []
not_found_repos_list = []
index = 1
while True:
    try:

        query = {'names': args.tag, 'page': index}
        encoded_query = urllib.parse.urlencode(query)
        soup = get_soup(
            'https://www.openhub.net/tags?' + encoded_query)

        list_root = soup.select_one('div#projects_index_list')

        if not list_root:
            break

        for project in tqdm(list_root.select('div.well'), leave=False):
            try:
                title_content = project.select_one('h2.title a')
                url = title_content.get('href')
                title = title_content.get_text()
                tqdm.write(title)

                info_content = project.select_one('div.stats')

                pattern = r'([\d\.]+).*'
                loc = re.match(pattern, info_content.select_one(
                    'a').get_text()).group(1)
                tqdm.write(loc)

                if is_explicit(project):
                    raise Exception

                if float(loc) <= 0:
                    raise Exception

                repos_url = get_repos_url(url)

                tqdm.write(repos_url)
                repos_list.append(title + ',' + repos_url)
            except:
                not_found_repos_list.append(title)
                pass
    except:
        pass
    index += 1

write_csv(str(os.path.join(args.tag + '/', 'repos_table.csv')), repos_list)
write_csv(str(os.path.join(args.tag + '/',
                           'not_found_repos_table.csv')), not_found_repos_list)
