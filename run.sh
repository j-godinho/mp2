echo 'creating directories'
#output training files
mkdir -p output/AlmadaNegreiros
mkdir -p output/LuisaMarquesSilva
mkdir -p output/JoseSaramago
mkdir -p output/JoseRodriguesSantos
mkdir -p output/EcaDeQueiros
mkdir -p output/CamiloCasteloBranco

#output test files
mkdir -p output/test/500Palavras
mkdir -p output/test/1000Palavras


#script to normalize all given tests and training files
#flag 0 - punctuation surrounded by spaces
#flag 1 - lower capital letters
#flag 2 - remove punctuation
norm_flag="1"
python normalization.py $norm_flag
