from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from nltk import word_tokenize
from decimal import Decimal
from math import log
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
    return writer_chosen, min_value

def analyze_avg_words_sentence():
    writers_dict = analyze_writers()

    #analyze first path
    path500 = 'output/test/500Palavras/'

    path1000 = 'output/test/1000Palavras/'

    files = glob.glob(path500+"*.txt")
    files = files + glob.glob(path1000+"*.txt")

    for file in files:
        average_words = average_words_sentence(file)
        returned = compare_values(writers_dict, average_words)
        print file + " " + returned[0] + " " + str(returned[1])

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

def training(flag, exp_flag):
    writer_name = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    writers = []

    for w in writer_name:
        path = 'output/' + w + '/'
        c_writer = writer(w)
        text = read_file(path + w + '.txt')

        print '[' + w + ']'

        c_writer.unigrams = calc_n_grams(text, 1, 1, flag)

        c_writer.bigrams = calc_n_grams(text, 2, 2, flag)

        c_writer.n = calc_number_of_tokens(c_writer.unigrams)

        c_writer.v = len(c_writer.unigrams.keys())

        c_writer.s_unigrams = smoothing_unigrams(c_writer.unigrams, c_writer.n, c_writer.v)

        c_writer.s_bigrams = smoothing_bigrams(c_writer.unigrams, c_writer.bigrams, c_writer.v)

        c_writer.unigram_probabilities = calc_unigram_probabilities(c_writer.unigrams, c_writer.n)

        c_writer.bigram_probabilities = calc_bigram_probabilities(c_writer.unigrams, c_writer.bigrams)

        c_writer.s_unigram_probabilities = calc_unigram_probabilities(c_writer.s_unigrams, c_writer.n)

        c_writer.s_bigram_probabilities = calc_bigram_probabilities(c_writer.s_unigrams, c_writer.s_bigrams)

        if(exp_flag == 0):
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



            print  str(n) + '-grams'
            ts.ngrams = calc_n_grams(text, n, n, flag)

            m = -1
            for w in writers:
                ts.scores[w] = test_writer_without_smoothing(w, ts.ngrams, n)
                ts.s_scores[w] = test_writer_with_smoothing(w, ts.ngrams, n)
                if m < ts.s_scores[w]:
                    m = ts.s_scores[w]
                    m_w = w
            print '[' + t + ' test ' + str(i) + '] ' + m_w
    return tests

def calc_tf(path, lower, upper):
    f = read_file(path)

    vectorizer = CountVectorizer(ngram_range=(lower, upper))
    analyze = vectorizer.build_analyzer()
    ngrams = analyze(f)

    return dict ( Counter(ngrams) )

def calc_idf(lower, upper):
    writer_name = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    of = []

    for w in writer_name:
        path = 'output/' + w + '/'
        of.append( read_file(path + w + '.txt') )

    vectorizer = TfidfVectorizer(ngram_range=(lower,upper), min_df=1)
    X = vectorizer.fit_transform(of)
    idf = vectorizer.idf_
    return dict ( zip ( vectorizer.get_feature_names(), idf ) )

def calc_precision(rw, sw):
    n = 0
    for word in sw:
        if word in rw:
            n += 1
    return float(n) / len(sw)

def calc_recall(rw, sw):
    n = 0
    for word in sw:
        if word in rw:
            n += 1
    return float(n)/len(rw)

def calc_f1(precision, recall):
    beta = 0.5
    if precision == 0 or recall == 0:
        return 0
    else:
        return ( (pow(beta, 2) + 1) * precision * recall ) / ((pow(beta, 2) * precision) + recall)

def calc_tf_idf(lower, upper, top):
    writer_name = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
    testing_length = ["500Palavras", "1000Palavras"]
    writers = []
    print 'calculating idf'
    idf = calc_idf(lower, upper)

    for w in writer_name:
        print 'calculating tf for ' + w
        tf = calc_tf('output/' + w + '/' + w + '.txt', lower, upper)
        c_writer = writer(w)
        c_writer.tf_idf = dict ()
        print 'calculating tf-idf for ' + w
        for ngram in tf.keys():
            if ngram in idf.keys():
                c_writer.tf_idf[ngram] = tf[ngram] * idf[ngram]
            else:
                c_writer.tf_idf[ngram] = tf[ngram] * log(64/1) # 64 ficheiros de treino
        writers.append( c_writer )

    for t in testing_length:
        path = 'output/test/' + t + '/'
        for i in range(6):
            print 'calculating tf for ' + t + ' ' + str(i)
            tf = calc_tf( path + str(i) + '.txt', lower, upper)
            tf_idf = dict ()
            print 'calculating tf-idf for ' + t + ' ' + str(i)
            for ngram in tf.keys():
                if ngram in idf.keys():
                    tf_idf[ngram] = tf[ngram] * idf[ngram]
                else:
                    tf_idf[ngram] = tf[ngram] * log(64/1) # 64 ficheiros de treino

            print 'calculating top measures for ' + t + ' ' + str(i)
            m = -1
            for w in writers.keys():
                top_ranked_test = sorted(tf_idf.items(), key=operator.itemgetter(1))[0:(top * len(tf_idf.keys()))]
                top_ranked_writer = sorted(writers[w].tf_idf.items(), key=operator.itemgetter(1))[0:(top * len(writers[w].tf_idf.keys()))]
                prec = calc_precision(top_ranked_writer, top_ranked_test)
                rec = calc_recall(top_ranked_writer, top_ranked_test)
                f1 = calc_f1(prec, rec)
                print '{}\t{}\t{}\t{}'.format(w, prec, rec, f1)
                if m < f1:
                    m = f1
                    m_w = w
            print '[' + t + ' ' + str(i) + '] ' + w
            print ' '

def main():
    norm_flag = int(sys.argv[1])
    exp_flag = int(sys.argv[2])

    if(exp_flag == 0):
        training(norm_flag, exp_flag)
    if(exp_flag == 1 or exp_flag==2):
        testing_length = ['500Palavras', '1000Palavras']
        writers = training(norm_flag, exp_flag)
        testing(writers, testing_length, 1, norm_flag)
        testing(writers, testing_length, 2, norm_flag)


    elif(exp_flag == 3):
        calc_tf_idf(1, 2, 0.1)

    elif(exp_flag == 4):
        analyze_avg_words_sentence()


if __name__ == '__main__':
    main()
