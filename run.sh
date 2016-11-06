echo 'Creating directories'

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

echo 'Checking dependencies'
python dependencies.py

# script to normalize all given tests and training files
# flag 0 - punctuation surrounded by spaces
# flag 1 - lower capital letters without punctuation
# flag 2 - remove punctuation
# flag 3 - without punctuation and portuguese stop
echo 'Normalizing'
norm_flag="2"
python normalization.py $norm_flag

echo 'Analyzing...'
python main.py $norm_flag
