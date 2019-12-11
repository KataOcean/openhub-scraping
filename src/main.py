import requests
import time
import argparse
import urllib.parse
import re
from bs4 import BeautifulSoup
from tqdm import tqdm


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


explicit_list = ['gamedev', 'emulator', 'framework']


def is_explicit(soup):
    tags = [x.get_text() for x in soup.select('a.tag')]
    for tag in tags:
        if tag in explicit_list:
            return True
    return False


repos_list = []
not_found_repos_list = []
index = 1
while index < 2:
    try:

        query = {'names': 'game', 'page': index}
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

                info_content = project.select_one('div.stats')

                pattern = '([\d\.]+).*'
                loc = re.match(pattern, info_content.select_one(
                    'a').get_text()).group(1)
                tqdm.write(loc)

                if is_explicit(project):
                    raise Exception

                if float(loc) <= 0:
                    raise Exception

                tqdm.write(title)

                repos_url = get_repos_url(url)

                tqdm.write(repos_url)
                repos_list.append(title + ',' + repos_url)
            except:
                not_found_repos_list.append(title)
                pass
    except:
        pass
    index += 1

with open('./repos_table.csv', mode='w') as f:
    f.write('\n'.join(repos_list))

with open('./not_found_repos_table.csv', mode='w') as f:
    f.write('\n'.join(not_found_repos_list))
