from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import re
import io
from nltk import word_tokenize
import glob
from nltk.tokenize import TreebankWordTokenizer
import sys


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

        print 'writing files'
        output_without_smoothing(path, c_writer)
        output_with_smoothing(path, c_writer)

        writers.append( c_writer )

        print ' '

    return writers

def testing(testing_length, flag):
    tests = []
    for t in testing_length:
        path = 'output/test/' + t + '/'
        for i in range(6):
            ts = test_subject(t, i)
            text = read_file(path + str(i) + '.txt')

            print '[' + t + ' test ' + str(i) + ']'

            print  str(n) + '-grams to ' + str(m) +
            ts.unigrams = calc_n_grams(text, 1, 1, flag)

            print ' '
    return tests

def main():
    norm_flag = int(sys.argv[1])
    analyze_avg_words_sentence()
    # file = io.open('output/LuisaMarquesSilva/LuisaMarquesSilva.txt', 'r')
    # text = file.read()
    # counts = calc_n_grams(text, 1, 2, norm_flag)
    # n_tokens = calc_number_of_tokens(counts)
    # counts_smoothed = add_one_smoothing(counts, n_tokens)
    # for key in counts.keys():
    #     print '{}\t\t\t{}\t\t\t{}'.format(key.encode('utf-8'), counts[key], counts_smoothed[key])

    testing_length = ['500Palavras', '1000Palavras']

    training(norm_flag)
    testing(['500Palavras'])



if __name__ == '__main__':
    main()

