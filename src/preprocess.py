import argparse
import transformers
from unidecode import unidecode
from util import clean_str, isascii, isdecodable
import spacy
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from aksara.aksara import BaseTokenizer as AksaraBaseTokenizer

parser = argparse.ArgumentParser()

parser.add_argument("--source_file", default=None, type=str, required=True,
                    help="Source text file (sentence-aligned, newline-delimited)")
parser.add_argument("--target_file", default=None, type=str, required=True,
                    help="Target text file (sentence-aligned, newline-delimited)")
parser.add_argument("--output_file", default=None, type=str, required=True,
                    help="non-tokenized output text file (combining source and target sentences)")
parser.add_argument("--tokenized_file", default=None, type=str, required=True,
                    help="tokenized output text file (combining source and target sentences)")
parser.add_argument("--source_spacy_model", default=None, type=str,
                    help="downloaded spacy model to load as source text tokenizer")
parser.add_argument("--target_spacy_model", default=None, type=str,
                    help="downloaded spacy model to load as target text tokenizer")
parser.add_argument("--target_aksara_model", action='store_true',
                    help="use aksara (indo/malay) tokenizer")
parser.add_argument("--source_bert_tokenizer", action='store_true',
                    help="use bert tokenizer for source file")
parser.add_argument("--target_bert_tokenizer", action='store_true',
                    help="use bert tokenizer for target file")
parser.add_argument("--source_ignore_non_ascii", action='store_true',
                    help="for source language ignore and drop tokens containing non ascii characters")
parser.add_argument("--target_ignore_non_ascii", action='store_true',
                    help="for target language ignore and drop tokens containing non ascii characters")
parser.add_argument("--source_unidecode", action='store_true',
                    help="strip off accents from character and remove corrupted unicode")
parser.add_argument("--target_unidecode", action='store_true',
                    help="strip off accents from character and remove corrupted unicode")
parser.add_argument("--source_ignore_nondecodable", action='store_true',
                    help="filter tokens that contain corrupted unicode")
parser.add_argument("--target_ignore_nondecodable", action='store_true',
                    help="filter tokens that contain corrupted unicode")

args = parser.parse_args()

source_lines = open(args.source_file).read().rstrip().split("\n")
target_lines = open(args.target_file).read().rstrip().split("\n")

print(len(source_lines))
print(len(target_lines))

max_line_no = min(len(source_lines), len(target_lines))
source_lines = [clean_str(line) for line in source_lines[:max_line_no]]
target_lines = [clean_str(line) for line in target_lines[:max_line_no]]

if args.source_unidecode:
    source_lines = [unidecode(line) for line in source_lines]

if args.target_unidecode:
    target_lines = [unidecode(line) for line in target_lines]

def filter_data(source_lines, target_lines, filter_source, filter_target, function):
    if filter_source and filter_target:
        source_target = [(src, tar) for src, tar in zip(source_lines, target_lines) if
                         function(src) and function(tar)]
    elif filter_source:
        source_target = [(src, tar) for src, tar in zip(source_lines, target_lines) if
                         function(src)]
    elif filter_target:
        source_target = [(src, tar) for src, tar in zip(source_lines, target_lines) if
                         function(tar)]
    else:
        source_target = list(zip(source_lines, target_lines))

    new_source_lines = [srctar[0] for srctar in source_target]
    new_target_lines = [srctar[1] for srctar in source_target]

    return new_source_lines, new_target_lines

source_lines, target_lines = filter_data(source_lines, target_lines, filter_source=args.source_ignore_non_ascii,
                                         filter_target=args.target_ignore_non_ascii, function=isascii)
source_lines, target_lines = filter_data(source_lines, target_lines, filter_source=args.source_ignore_nondecodable,
                                         filter_target=args.target_ignore_nondecodable, function=isdecodable)

source_nlp = spacy.load(args.source_spacy_model) if args.source_spacy_model else None
target_nlp = spacy.load(args.target_spacy_model) if args.target_spacy_model else None

disable_pipes = ["transformer", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner", "tok2vec", "morphologizer"]

for pipe in disable_pipes:
    if source_nlp and pipe in source_nlp.pipe_names:
        source_nlp.disable_pipes(pipe)
    if target_nlp and pipe in target_nlp.pipe_names:
        target_nlp.disable_pipes(pipe)


if args.source_bert_tokenizer or args.target_bert_tokenizer:
    bert_tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-multilingual-cased')
else:
    bert_tokenizer = None

if args.target_aksara_model:
    aksara_tokenizer = AksaraBaseTokenizer()

def src_tokenize(line):
    if args.source_bert_tokenizer:
        return bert_tokenizer.tokenize(line)
    elif args.source_spacy_model:
        return [token.text for token in source_nlp(line)]
    else:
        return word_tokenize(line)

def tar_tokenize(line):
    if args.target_bert_tokenizer:
        return bert_tokenizer.tokenize(line)
    elif args.target_spacy_model:
        return [token.text for token in target_nlp(line)]
    elif args.target_aksara_model:
        return aksara_tokenizer.tokenize(line)[0]
    else:
        return word_tokenize(line)


batch_size = 128

outputf = open(args.output_file, "w")
tokenizedf = open(args.tokenized_file, "w")

read_len = 0
print(read_len)

for i in range(read_len, max_line_no, batch_size):

    src_tar, tokenized_src_tar = [], []
    tokenized_source_lines = [src_tokenize(src) for src in source_lines[i:i+batch_size]]
    tokenized_target_lines = [tar_tokenize(tar) for tar in target_lines[i:i+batch_size]]

    for j, (tokenized_src, tokenized_tar, src, tar) in enumerate(zip(tokenized_source_lines, tokenized_target_lines,
                                                           source_lines[i:i+batch_size], target_lines[i:i+batch_size])):

        if tokenized_src and tokenized_tar:
            out = " ".join(tokenized_src) + " ||| " + " ".join(tokenized_tar)
            tokenized_src_tar.append(out)

            out = src + " ||| " + tar
            src_tar.append(out)
        else:
            print(i + j)
            print(tokenized_src)
            print(tokenized_tar)

    if src_tar and tokenized_src_tar:
        if i > 0:
            tokenizedf.write("\n")
            outputf.write("\n")
        tokenizedf.write("\n".join(tokenized_src_tar))
        outputf.write("\n".join(src_tar))
tokenizedf.close()