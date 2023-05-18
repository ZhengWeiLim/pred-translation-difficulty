# Predicting Human Translation Difficulty Using Automatic Word Alignment

1.  Translation surprisal and entropy are calculated in `predicting-translation-difficulty.ipynb`. 
Results are shown and can be reproduced on the notebook.

2. Alignment scores are aggregated by `src/word_alignment_distribution.py`,
based on [awesome-align](https://github.com/neulab/awesome-align) word files and
output scores of [open subtitles](https://opus.nlpl.eu/OpenSubtitles-v2018.php). For example, 

    `python3 src/word_alignment_distribution.py --word_file <word_file> --prob_file <output_prob_file> 
--source_output_file en_fr.txt --target_output_file fr_en.txt --bsz 50000`

    will compute English-to-French and French-to-English alignment scores based on the initial parallel corpora.

    Let `sword` and `tword` be source and target word alignment, each line of the output file is space separated with:

    `<sword> <sword frequency> <tword> <tword frequency> <tword normalized frequency> <tword alignment score sum> <tword alignment score normalized>`

3. Semantic alignments based on [Thompson et al. (2020)](https://par.nsf.gov/servlets/purl/10213620)  can be found in `evaluation/semantic-alignments-thompson/compute-alignment/eval-alignments`.
Original code is available [here](https://osf.io/tngba/).  

## Evaluation
### 1. Tranlsation process  
CRITT TPR-DB translation process data and feature descriptions can be found [here](https://sites.google.com/site/centretranslationinnovation/tpr-db/public-studies).

### 2. Translation norms

**German**

Translation semantic variability: How semantic relatedness affects learning of 
translation-ambiguous words (Bracken, Degani, Eddington and Tokowicz, 2016)

source: http://plumlab.pitt.edu/norms/
filename: german-tsv.csv
columns: "German Word", "Averaged_TSV"

**Chinese**

Translation ambiguity between English and Mandarin Chinese: The roles of proficiency and word characteristics
(Tseng, Alison M., Li-Yun Chang, and Natasha Tokowicz, 2014)

source: http://plumlab.pitt.edu/norms/ <br />
filename: chinese-translation-ambiguity.csv <br />
columns: "English Word", "Mandarin Word", "Semantic Similarity Rating"

note: average by Mandarin word -> mandarin-to-english variability;
average by English word -> english-to-mandarin variability

also: https://www.saporedicina.com/english/list-chengyu/

**Malay**

Translation norms for Malay and English words: The effects of word class, semantic variability, lexical characteristics, and language proficiency on translation
(Lee, van Heuven, Price and Leong, 2022)

source: https://osf.io/cnkjq/?view_only=54b5521c763241faa18a5b70963f2550 <br />
filename: english-malay-translation-norms.csv, malay-english-translation-norms.csv <br />
columns: "word","num_corr_resp"

note: alternatively, Mutual information of translation norms, should exclude total count < 3

**Japanese**

Cross-linguistic similarity norms for Japanese–English translation equivalents
(Allen and Conklin, 2014)

source: https://link.springer.com/article/10.3758/s13428-013-0389-z#Sec11 <br />
filename: japanese-semantic-similarity.csv <br />
columns: "English name", "Japanese name", "Semantic similarity", "No.Trans L1-L2", "No.Trans L2-L1"

note: "Cognate status" could be used for loanword analysis

**Dutch** 

Number-of-translation norms for Dutch–English translation pairs: A new tool for examining language production
(Tokowicz, Kroll, de Groot, and van Hell, 2002)

source: https://link.springer.com/content/pdf/10.3758/BF03195472.pdf?pdf=button%20sticky <br />
filename: dutch-similarityratings.csv <br />
columns: "Dutch Word", "English Word", "DE Semantic Sim Rating", "ED Semantic Sim Rating"

**Spanish**

Translation norms for English and Spanish: The role of lexical variables, word class, and L2 proficiency in negotiating translation ambiguity
(Prior, MacWhinney and Kroll, 2007) 

source: https://link.springer.com/article/10.3758/BF03193001#SecESM1 <br />
filename: EnglishToSpanish_TranslationPairs.csv, SpanishToEnglish_TranslationPairs.csv <br />
columns: "Word", "Word_num_trans"