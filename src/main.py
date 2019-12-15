import requests
import time
import argparse
import urllib.parse
import re
import os
import sys
from bs4 import BeautifulSoup

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


def write_csv(path, text):
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    with open(path, mode='a') as f:
        f.write(text + '\n')


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

index = 1
repos_table_path = os.path.join(args.tag + '/', 'repos_table.csv')
not_found_repos_table_path = os.path.join(
    args.tag + '/', 'not_found_repos_table.csv')
while True:
    try:
        print('page : ' + str(index))
        query = {'names': args.tag, 'page': str(index)}
        encoded_query = urllib.parse.urlencode(query)
        soup = get_soup(
            'https://www.openhub.net/tags?' + encoded_query)

        list_root = soup.select_one('div#projects_index_list')

        if not list_root:
            break

        for project in list_root.select('div.well'):
            try:
                title_content = project.select_one('h2.title a')
                url = title_content.get('href')
                title = title_content.get_text()
                print(title)

                info_content = project.select_one('div.stats')

                pattern = r'([\d\.]+).*'
                loc = re.match(pattern, info_content.select_one(
                    'a').get_text()).group(1)
                print(loc)

                if is_explicit(project):
                    raise Exception

                if float(loc) <= 0:
                    raise Exception

                repos_url = get_repos_url(url)

                print(repos_url)
                write_csv(repos_table_path, title + ',' + repos_url)
            except:
                write_csv(not_found_repos_table_path, title)
                pass
    except:
        print('error occured page :' + str(index))
        break
    index += 1
