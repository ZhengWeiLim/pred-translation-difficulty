import argparse
from itertools import islice

parser = argparse.ArgumentParser()

parser.add_argument("--word_file", default=None, type=str, required=True,
                    help="score text file")
parser.add_argument("--prob_file", default=None, type=str,
                    help="file record of word,word_id,word occurrences indices")
parser.add_argument("--source_output_file", default=None, type=str, required=True,
                    help="source output text file")
parser.add_argument("--target_output_file", default=None, type=str, required=True,
                    help="target output text file")
parser.add_argument("--bsz", default=50000, type=int, help="Batch size")

args = parser.parse_args()

src_tgt_freq, tgt_src_freq = {}, {}
src_tgt_weight, tgt_src_weight = {}, {}

batchsz = args.bsz

wordf = open(args.word_file, "r")

############ ORIGINAL ALIGNMENT PROBABILITY ############
if args.prob_file is not None:
    probf = open(args.prob_file, "r")

    for n_lines in iter(lambda: tuple(zip(islice(wordf, batchsz), islice(probf, batchsz))), ()):
        word_alignments = [pair.lower().split('<sep>') for line in n_lines for pair in line[0].rstrip().split(' ')]
        word_probs = [float(prob) for line in n_lines for prob in line[1].rstrip().split(' ')]

        for wpairs, algprob in zip(word_alignments, word_probs):
            src, tgt = wpairs[0], wpairs[1]
            src_tgt_freq[src] = src_tgt_freq.get(src, {})
            src_tgt_freq[src][tgt] = src_tgt_freq[src].get(tgt, 0) + 1
            tgt_src_freq[tgt] = tgt_src_freq.get(tgt, {})
            tgt_src_freq[tgt][src] = tgt_src_freq[tgt].get(src, 0) + 1
            src_tgt_weight[src] = src_tgt_weight.get(src, {})
            src_tgt_weight[src][tgt] = src_tgt_weight[src].get(tgt, []) + [algprob]
            tgt_src_weight[tgt] = tgt_src_weight.get(tgt, {})
            tgt_src_weight[tgt][src] = tgt_src_weight[tgt].get(src, []) + [algprob]

    probf.close()

wordf.close()

src_tgt_freq_sum = {src: sum(tgtfq.values()) for src, tgtfq in src_tgt_freq.items()}
tgt_src_freq_sum = {tgt: sum(srcfq.values()) for tgt, srcfq in tgt_src_freq.items()}
src_tgt_freq_norm = {src: {tgt: fq/src_tgt_freq_sum[src] for tgt, fq in tgtfq.items()} for src, tgtfq in src_tgt_freq.items()}
tgt_src_freq_norm = {tgt: {src: fq/tgt_src_freq_sum[tgt] for src, fq in srcfq.items()} for tgt, srcfq in tgt_src_freq.items()}

src_tgt_weight_sum = {src: {tgt: sum(weights) for tgt, weights in tgtweight.items()} for src, tgtweight in src_tgt_weight.items()}
tgt_src_weight_sum = {tgt: {src: sum(weights) for src, weights in srcweight.items()} for tgt, srcweight in tgt_src_weight.items()}
src_weight_sum = {src: sum(list(tgtweight.values())) for src, tgtweight in src_tgt_weight_sum.items()}
tgt_weight_sum = {tgt: sum(list(srcweight.values())) for tgt, srcweight in tgt_src_weight_sum.items()}
src_tgt_weight_norm = {src: {tgt: weightsum/src_weight_sum[src] for tgt, weightsum in tgtweight.items()} for src, tgtweight in src_tgt_weight_sum.items()}
tgt_src_weight_norm = {tgt: {src: weightsum/tgt_weight_sum[tgt] for src, weightsum in srcweight.items()} for tgt, srcweight in tgt_src_weight_sum.items()}


with open(args.source_output_file, "w") as srcf:
    for srcw, tgtfq in src_tgt_freq.items():
        srcwfq = sum(list(tgtfq.values()))
        tgts = [f"{tgt} {fq} {src_tgt_freq_norm[srcw][tgt]} {src_tgt_weight_sum[srcw][tgt]} {src_tgt_weight_norm[srcw][tgt]}"
            for tgt, fq in tgtfq.items()]
        srcf.write(f"{srcw} {srcwfq} {' '.join(tgts)}\n")

with open(args.target_output_file, "w") as tgtf:
    for tgtw, srcfq in tgt_src_freq.items():
        tgtwfq = sum(list(srcfq.values()))
        srcs = [f"{src} {fq} {tgt_src_freq_norm[tgtw][src]} {tgt_src_weight_sum[tgtw][src]} {tgt_src_weight_norm[tgtw][src]}"
            for src, fq in srcfq.items()]
        tgtf.write(f"{tgtw} {tgtwfq} {' '.join(srcs)}\n")


