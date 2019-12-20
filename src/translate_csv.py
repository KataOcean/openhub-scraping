import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')

args = parser.parse_args()

repos_list = []

with open(args.input) as f:
    reader = csv.reader(f)
    cols = [row for row in reader]

    for col in cols:
        if not 'github' in col[1]:
            continue
        repos_list.append(col[1].replace(
            'git://github', 'https://github'))

with open(args.output, 'w') as f:
    f.write('\n'.join(set(repos_list)))
