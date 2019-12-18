import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')

args = parser.parse_args()

repos_list = []

with open(args.input) as f:
    for line in tqdm(f.readlines()):
        if 'https' in line:
            repos_list.append(line)

with open(args.output, 'w') as f:
    f.write(''.join(set(repos_list)))
