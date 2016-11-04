import nltk
from nltk import word_tokenize
import io

def normalize_file():
	path = 'corpora/training/AlmadaNegreiros/'
	f = io.open(path+"pg22615.txt", 'r', encoding='utf8')
	read_data = f.read()
	f.close()

	nltk.download('punkt')

	tokens = word_tokenize( read_data)
	
	f=io.open(path+"pg22615_a.txt", 'w', encoding='utf8')
	
	for token in tokens:
		print token
		f.write(token+" ")

	f.close()

def main():
    normalize_file()


if __name__ == '__main__':
    main()
