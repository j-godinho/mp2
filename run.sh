echo 'creating directories'

#output training files
mkdir -p output
mkdir -p output/AlmadaNegreiros
mkdir -p output/LuisaMarquesSilva
mkdir -p output/JoseSaramago
mkdir -p output/JoseRodriguesSantos
mkdir -p output/EcaDeQueiros
mkdir -p output/CamiloCasteloBranco

#output test files
mkdir -p output/test/500Palavras
mkdir -p output/test/1000Palavras

python dependencies.py 

#script to normalize all given tests and training files
#flag 0 - punctuation surrounded by spaces
#flag 1 - lower capital letters without punctuation
#flag 2 - remove punctuation
#flag 3 - without punctuation and portuguese stop words were removed
norm_flag="3"
python normalization.py $norm_flag

python main.py $norm_flag

