from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import re

def calc_n_grams(text, lower, upper):
    vectorizer = CountVectorizer(ngram_range=(lower,upper))
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(text)

    return dict ( Counter(ngrams) )

def space_normalization(path):
    f = open(path).read()
    f = re.sub('([.,!?():\[\]_+#])', r' \1 ', f)                                       # TODO: check if _ ' + [ ] : # are punctuation
    return re.sub('\s{2,}', ' ', f)


def main():
    print space_normalization('corpora/training/AlmadaNegreiros/pg22615.txt')

if __name__ == '__main__':
    main()
