from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import re
import io
from nltk import word_tokenize
import glob



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

def calc_n_grams(text, lower, upper):
    vectorizer = CountVectorizer(ngram_range=(lower,upper))
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
    


def analyze_files():
    writers_dict = analyze_writers()

    #analyze first path
    path500 = 'output/test/500Palavras/'

    path1000 = 'output/test/1000Palavras/'
    
    files = glob.glob(path500+"*.txt")
    files = files + glob.glob(path1000+"*.txt")

    for file in files:
        average_words = average_words_sentence(file)
        print file + " " + compare_values(writers_dict, average_words)
    

def main():
    analyze_files()


if __name__ == '__main__':
    main()

