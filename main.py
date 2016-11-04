from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

def calc_n_grams(path, lower, upper):
    f = open(path).read()

    vectorizer = CountVectorizer(ngram_range=(lower,upper))
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(f)

    return dict ( Counter(ngrams) )

def main():
    


if __name__ == '__main__':
    main()
