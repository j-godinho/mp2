
import re
def normalize_file():
	path = 'corpora/training/AlmadaNegreiros/'
	f = open(path+"pg22615.txt", 'r')
	read_data = f.read()
	f.close()
	tokens = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", read_data)
	

	f=open(path+"pg22615_a.txt", 'w')
	
	for token in tokens:
		print token
		f.write(token+" ")

	f.close()

def main():
    normalize_file()


if __name__ == '__main__':
    main()
