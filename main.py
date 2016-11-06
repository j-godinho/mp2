from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import io

class writer(object):

    def __init__(self, name):
        self.name = name

class test_subject(object):

    def __init__(self, test_length, index):
        self.test_length = test_length
        self.index = index

def read_file(path):
    f = io.open(path, 'r', encoding='utf8')
    text = f.read()
    f.close()

    return text

def output_with_smoothing(path, w):
    f_u = io.open(path + 'smoothed_unigrams.txt', 'w', encoding='utf8')
    for key in w.s_unigrams.keys():
        f_u.write( key + '\t' + str(w.s_unigrams[key]) + '\n')
    f_u.close()

    f_b = io.open(path + 'smoothed_bigrams.txt', 'w', encoding='utf8')
    for key in w.s_bigrams.keys():
        f_b.write( key + '\t' + str(w.s_bigrams[key]) + '\n')
    f_b.close()

def output_without_smoothing(path, w):
    f_u = io.open(path + 'unigrams.txt', 'w', encoding='utf8')
    for key in w.unigrams.keys():
        f_u.write( key + '\t' + str(w.unigrams[key]) + '\n')
    f_u.close()

    f_b = io.open(path + 'bigrams.txt', 'w', encoding='utf8')
    for key in w.bigrams.keys():
        f_b.write( key + '\t' + str(w.bigrams[key]) + '\n')
    f_b.close()

def add_one_smoothing(count, n, v):
    return float(count + 1) * ( float(n) / (n + v) )

def smoothing_unigrams(unigrams, n, v):
    ds = dict ()
    for key in unigrams.keys():
        ds[key] = add_one_smoothing( unigrams[key], n, v )
    return ds

def smoothing_bigrams(unigrams, bigrams, v):
    ds = dict ()
    for key in bigrams.keys():
        n = unigrams[ key.split()[1] ]
        ds[key] = add_one_smoothing( bigrams[key], n, v )
    return ds

def calc_number_of_tokens(counts):
    n = 0
    for i in counts.values():
        n += i
    return n

def calc_n_grams(text, lower, upper):
    vectorizer = CountVectorizer(ngram_range=(lower,upper))
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(text)

    return dict ( Counter(ngrams) )

def probability(count, n):
    return float(count) / n

def calc_unigram_probabilities(unigrams, n):
    pu = dict ()
    for key in unigrams.keys():
        pu[key] = probability(unigrams[key], n)
    return pu

def calc_bigram_probabilities(unigrams, bigrams):
    pb = dict ()
    for key in bigrams.keys():
        n = unigrams[ key.split()[1] ]
        pb[key] = probability(bigrams[key], n)
    return pb

def training():
    writer_name = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    writers = []

    for w in writer_name:
        path = 'output/' + w + '/'
        c_writer = writer(w)
        text = read_file(path + w + '.txt')

        print '[' + w + ']'

        print 'unigrams'
        c_writer.unigrams = calc_n_grams(text, 1, 1)
        print 'bigrams'
        c_writer.bigrams = calc_n_grams(text, 2, 2)
        print 'N'
        c_writer.n = calc_number_of_tokens(c_writer.unigrams)
        print 'V'
        c_writer.v = len(c_writer.unigrams.keys())
        print 'smoothed unigrams'
        c_writer.s_unigrams = smoothing_unigrams(c_writer.unigrams, c_writer.n, c_writer.v)
        print 'smoothed bigrams'
        c_writer.s_bigrams = smoothing_bigrams(c_writer.unigrams, c_writer.bigrams, c_writer.v)
        print 'unigram probabilities'
        c_writer.unigram_probabilities = calc_unigram_probabilities(c_writer.unigrams, c_writer.n)
        print 'bigram probabilities'
        c_writer.bigram_probabilities = calc_bigram_probabilities(c_writer.unigrams, c_writer.bigrams)
        print 'smoothed unigram probabilities'
        c_writer.s_unigram_probabilities = calc_unigram_probabilities(c_writer.s_unigrams, c_writer.n)
        print 'smoothed bigram probabilities'
        c_writer.s_bigram_probabilities = calc_bigram_probabilities(c_writer.s_unigrams, c_writer.s_bigrams)

        print 'writing files'
        output_without_smoothing(path, c_writer)
        output_with_smoothing(path, c_writer)

        writers.append( c_writer )

        print ' '

    return writers

def test_writer_without_smoothing(w, ngrams, n):
    score = 1

    if n == 1:
        for key in ngrams.keys():
            if key in w.unigram_probabilities.keys():
                score *= w.unigram_probabilities[key]
            else:
                score *= 0
                return score
    elif n == 2:
        for key in ngrams.keys():
            if key in w.bigram_probabilities.keys():
                score *= w.bigram_probabilities[key]
            else:
                score *= 0
                return score
    else:
        print 'error'

    return score

def test_writer_with_smoothing(w, ngrams, n):
    score = 1

    if n == 1:
        for key in ngrams.keys():
            if key in w.s_unigram_probabilities.keys():
                score *= w.s_unigram_probabilities[key]
            else:
                score *= ( float(1) / w.n + w.v )
    elif n == 2:
        for key in ngrams.keys():
            if key in w.s_bigram_probabilities.keys():
                score *= w.s_bigram_probabilities[key]
            else:
                word = key.split()[1]
                if word in w.s_unigrams.keys():
                    wn = w.s_unigrams[ word ]
                else:
                    wn = float(w.n) / (w.n + w.v)
                score *= ( float(1) / wn + w.v )
    else:
        print 'error'

    return score

def testing(writers, testing_length, n):
    tests = []
    for t in testing_length:
        path = 'output/test/' + t + '/'
        for i in range(6):
            ts = test_subject(t, i)
            ts.scores = dict ()
            ts.s_scores = dict ()
            text = read_file(path + str(i) + '.txt')

            print '[' + t + ' test ' + str(i) + ']'

            print  str(n) + '-grams'
            ts.ngrams = calc_n_grams(text, n, n)

            for w in writers:
                ts.scores[w] = test_writer_without_smoothing(w, ts.ngrams, n)
                ts.s_scores[w] = test_writer_with_smoothing(w, ts.ngrams, n)
                print  w.name + '\t\t\t' + str(ts.scores[w]) + '\t' + str(ts.s_scores[w])

            print ' '
    return tests

def main():
    testing_length = ['500Palavras', '1000Palavras']

    writers = training()
    testing(writers, ['500Palavras'], 1)


if __name__ == '__main__':
    main()
