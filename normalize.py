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

def main():
	nltk.download('punkt')
	read_files()

if __name__ == '__main__':
    main()
