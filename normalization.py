import nltk
from nltk import word_tokenize
import io
import glob
import string
import sys

def read_writer_file(path):
	f = io.open(path, 'r', encoding='utf8')
	read_data = f.read()
	f.close()

	return read_data


def read_writer_files(writer, flag):
	path = 'corpora/training/' + writer + '/*.txt'
	files = glob.glob(path)
	read_data = ""

	for i in range(len(files)):
		read_data += read_writer_file(files[i])

	normalize_train_file(read_data, writer, flag)

def read_train_files(flag):
	writers = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
	for i in range(len(writers)):
		print "Writing normalized files of:", writers[i]
		read_writer_files(writers[i], flag)

def normalize_train_file(data, writer, flag):
	
	output_path = 'output/'+writer+'/'+writer+'.txt'

	tokens = word_tokenize(data)

	f=io.open(output_path, 'w', encoding='utf8')

	if(flag == 3):
		stopwords = nltk.corpus.stopwords.words('portuguese')
		
	for token in tokens:
		if(flag == 0):
			f.write(token + " ")
		if(flag==1):
			f.write(token.lower() + " ")
		if(flag==2):
			if(token not in string.punctuation):
				f.write(token + " ")
		if(flag==3):
			if(token not in stopwords):
				f.write(token + " ")
	f.close()



def normalize_test_file(path, output_path, index, flag):
	data = read_writer_file(path)
	tokens = word_tokenize(data)
	output_path = output_path+str(index)+".txt"

	f = io.open(output_path, 'w', encoding='utf8')
	if(flag == 3):
		stopwords = nltk.corpus.stopwords.words('portuguese')

	for token in tokens:	
		if(flag == 0):
			f.write(token + " ")
		if(flag==1):
			f.write(token.lower() + " ")
		if(flag==2):
			if(token not in string.punctuation):
				f.write(token + " ")
		if(flag==3):
			if(token not in stopwords):
				f.write(token + " ")
	f.close()


def normalize_tests(flag):
	print "Normalizing test files"
	path_input1 = 'corpora/test/500Palavras/*.txt'
	path_input2 = 'corpora/test/1000Palavras/*.txt'

	path_output1 = 'output/test/500Palavras/'
	path_output2 = 'output/test/1000Palavras/'

	files = glob.glob(path_input1)
	for i in range (len(files)):
		normalize_test_file(files[i], path_output1, i, flag)

	files = glob.glob(path_input2)
	for i in range (len(files)):
		normalize_test_file(files[i], path_output2, i, flag)


def main():
	
	norm_flag = int(sys.argv[1])

	#normalize all training files
	read_train_files(norm_flag)
	
	#normalize test files
	normalize_tests(norm_flag)

if __name__ == '__main__':
    main()
