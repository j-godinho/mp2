from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import re
import io
from nltk.tokenize import TreebankWordTokenizer
import sys
def add_one_smoothing(d, n):
    ds = dict ()
    v = len(d.keys())
    for key in d.keys():
        ds[key] = float(d[key] + 1) * ( float(n) / (n + v) )
    return ds

def calc_number_of_tokens(counts):
    n = 0
    for i in counts.values():
        n += i
    return n

def calc_n_grams(text, lower, upper, flag):
    if(flag == 0):
        vectorizer = CountVectorizer(ngram_range=(lower,upper), lowercase=False, tokenizer=TreebankWordTokenizer().tokenize)
    else:    
        vectorizer = CountVectorizer(ngram_range=(lower,upper), lowercase=False)
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(text)

    return dict ( Counter(ngrams) )

def main():

    norm_flag = int(sys.argv[1])

    file = io.open('output/LuisaMarquesSilva/LuisaMarquesSilva.txt', 'r')
    text = file.read()
    counts = calc_n_grams(text, 1, 2, norm_flag)
    n_tokens = calc_number_of_tokens(counts)
    counts_smoothed = add_one_smoothing(counts, n_tokens)
    for key in counts.keys():
        print '{}\t\t\t{}\t\t\t{}'.format(key.encode('utf-8'), counts[key], counts_smoothed[key])

if __name__ == '__main__':
    main()
