
import re
def normalize_file():
	path = 'corpora/training/AlmadaNegreiros/pg22615.txt'
	f = open(path, 'r')
	read_data = f.read()
	f.close()
	tokens = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", read_data)
	

	f=open(path, 'w')
	for token in tokens:
		print token
		f.write(token+" ")

	f.close()

def main():
    normalize_file()


if __name__ == '__main__':
    main()
