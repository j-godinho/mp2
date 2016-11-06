from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from nltk import word_tokenize
from decimal import Decimal
import glob
import sys
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

def calc_n_grams(text, lower, upper, flag):
    if(flag == 0):
        vectorizer = CountVectorizer(ngram_range=(lower,upper), lowercase=False, tokenizer=TreebankWordTokenizer().tokenize)
    else:
        vectorizer = CountVectorizer(ngram_range=(lower,upper), lowercase=False)
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(text)

    return dict ( Counter(ngrams) )

def probability(count, n):
    return float(count) / n

def average_words_sentence(path):
    #.!?;
    #...

    f = io.open(path, 'r', encoding='utf8')
    file_data = f.read()
    tokens = word_tokenize(file_data)

    end_symbols = ['!', '?', '...', ';', '.']
    sentences = 0
    for token in tokens:
        if(token in end_symbols):
            sentences += 1

    return float(len(tokens)-sentences)/sentences

def analyze_writers():
    writers = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    writers_dict = dict()
    for i in range(len(writers)):
        print "Analyzing average words per sentence of:", writers[i]
        path = 'output/' + writers[i]+'/' + writers[i] + '.txt'
        writers_dict[writers[i]] = average_words_sentence(path)
    return writers_dict

def compare_values(writers_dict, value):
    min_value = 999999
    writer_chosen = ""
    for key in writers_dict:
        distance = abs(writers_dict[key]-value)
        if(distance<min_value):
            writer_chosen = key
            min_value=distance
    return writer_chosen

def analyze_avg_words_sentence():
    writers_dict = analyze_writers()

    #analyze first path
    path500 = 'output/test/500Palavras/'

    path1000 = 'output/test/1000Palavras/'

    files = glob.glob(path500+"*.txt")
    files = files + glob.glob(path1000+"*.txt")

    for file in files:
        average_words = average_words_sentence(file)
        print file + " " + compare_values(writers_dict, average_words)

def output_with_smoothing(path, writer):
    f_u = io.open(path + 'smoothed_unigrams.txt', 'w', encoding='utf8')
    for key in writer.s_unigrams.keys():
        f_u.write( key + '\t' + str(writer.s_unigrams[key]) + '\n')
    f_u.close()

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

def training(flag):
    writer_name = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    writers = []

    for w in writer_name:
        path = 'output/' + w + '/'
        c_writer = writer(w)
        text = read_file(path + w + '.txt')

        print '[' + w + ']'

        print 'unigrams'
        c_writer.unigrams = calc_n_grams(text, 1, 1, flag)
        print 'bigrams'
        c_writer.bigrams = calc_n_grams(text, 2, 2, flag)
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
    score = Decimal(1)

    if n == 1:
        for key in ngrams.keys():
            if key in w.unigram_probabilities.keys():
                score *= Decimal(w.unigram_probabilities[key])
            else:
                score *= 0
                return score
    elif n == 2:
        for key in ngrams.keys():
            if key in w.bigram_probabilities.keys():
                score *= Decimal(w.bigram_probabilities[key])
            else:
                score *= 0
                return score
    else:
        print 'error'

    return score

def test_writer_with_smoothing(w, ngrams, n):
    score = Decimal(1)

    if n == 1:
        for key in ngrams.keys():
            if key in w.s_unigram_probabilities.keys():
                score *= Decimal(w.s_unigram_probabilities[key])
            else:
                score *= Decimal( float(1) / (w.n + w.v) )
    elif n == 2:
        for key in ngrams.keys():
            if key in w.s_bigram_probabilities.keys():
                score *= Decimal(w.s_bigram_probabilities[key])
            else:
                word = key.split()[1]
                if word in w.s_unigrams.keys():
                    wn = w.s_unigrams[ word ]
                else:
                    wn = float(w.n) / (w.n + w.v)
                score *= Decimal( float(1) / (wn + w.v) )
    else:
        print 'error'

    return score

def testing(writers, testing_length, n, flag):
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
            ts.ngrams = calc_n_grams(text, n, n, flag)

            for w in writers:
                ts.scores[w] = test_writer_without_smoothing(w, ts.ngrams, n)
                ts.s_scores[w] = test_writer_with_smoothing(w, ts.ngrams, n)
                print  w.name + '\t\t\t' + str(ts.scores[w]) + '\t' + str(ts.s_scores[w])

            print ' '
    return tests

def main():
    norm_flag = int(sys.argv[1])
    # analyze_avg_words_sentence()

    testing_length = ['500Palavras', '1000Palavras']

    writers = training(norm_flag)
    testing(writers, testing_length, 1, norm_flag)

if __name__ == '__main__':
    main()
