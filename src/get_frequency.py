import argparse
from itertools import islice
from collections import Counter

parser = argparse.ArgumentParser()

parser.add_argument("--tokenized_word_file", default=None, type=str, required=True,
                    help="score ||| target tokenized text file")
parser.add_argument("--source_output_file", default=None, type=str, required=True,
                    help="source output text file")
parser.add_argument("--target_output_file", default=None, type=str, required=True,
                    help="target output text file")

args = parser.parse_args()

source_word_freq = Counter()
target_word_freq = Counter()

batch_size = 1000000

with open(args.tokenized_word_file, "r") as inputf:
    for n_lines in iter(lambda: tuple(islice(inputf, batch_size)), ()):
        data = [line.lower().split(" ||| ") for line in n_lines]
        source_tokens = Counter([tok for line in data for tok in line[0].rstrip().split(' ')])
        target_tokens = Counter([tok for line in data for tok in line[1].rstrip().split(' ') if len(line) > 1])
        source_word_freq += source_tokens
        target_word_freq += target_tokens


with open(args.source_output_file, "w") as src_outf:
    for word, count in source_word_freq.items():
        src_outf.write(f"{word} {count}\n")

with open(args.target_output_file, "w") as tgt_outf:
    for word, count in target_word_freq.items():
        tgt_outf.write(f"{word} {count}\n")