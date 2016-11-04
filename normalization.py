import nltk
from nltk import word_tokenize
import io
import glob

def read_writer_file(path):
	f = io.open(path, 'r', encoding='utf8')
	read_data = f.read()
	f.close()
	
	return read_data	

def normalize_file(data, writer):
	
	output_path = 'output/'+writer+'/'+writer+'.txt'

	tokens = word_tokenize(data)

	f=io.open(output_path, 'w', encoding='utf8')

	for token in tokens:
		f.write(token+" ")
	f.close()

def read_writer_files(writer):
	path = 'corpora/training/' + writer + '/*.txt'
	files = glob.glob(path)
	
	read_data = ""
	
	for i in range(len(files)):
		read_data += read_writer_file(files[i])

	normalize_file(read_data, writer)

def read_files():
	writers = ["AlmadaNegreiros", "EcaDeQueiros", "JoseRodriguesSantos", "CamiloCasteloBranco", "JoseSaramago", "LuisaMarquesSilva"]
	for i in range(len(writers)):
		print "Writing normalized files of:", writers[i]
		read_writer_files(writers[i])

def normalize_test_file(path, output_path, index):

	data = read_writer_file(path)

	tokens = word_tokenize(data)

	output_path = output_path+str(index)+".txt"

	f=io.open(output_path, 'w', encoding='utf8')

	for token in tokens:
		f.write(token+" ")

	f.close()


def normalize_tests():
	path_input1 = 'corpora/test/500Palavras/*.txt'
	path_input2 = 'corpora/test/1000Palavras/*.txt'

	path_output1 = 'output/test/500Palavras/'
	path_output2 = 'output/test/1000Palavras/'

	files = glob.glob(path_input1)
	for i in range (len(files)):
		normalize_test_file(files[i], path_output1, i)

	files = glob.glob(path_input2)
	for i in range (len(files)):
		normalize_test_file(files[i], path_output2, i)





def main():
	nltk.download('punkt')
	#normalize all training files
	read_files()
	
	#normalize test files
	normalize_tests()

if __name__ == '__main__':
    main()
