import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')

args = parser.parse_args()

repos_list = []

with open(args.input) as f:
    reader = csv.reader(f)
    cols = [row[1] for row in reader]

    for col in cols:
        if not 'github' in col:
            continue
        repos_list.append(col.replace('git://github', 'https://github'))

with open(args.output, 'w') as f:
    f.write('\n'.join(repos_list))
