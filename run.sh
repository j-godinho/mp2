echo 'Criando Diretorias'

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

echo 'Verificar Dependências'
python dependencies.py

# script to normalize all given tests and training files
# norm_flag 0 - punctuation surrounded by spaces
# norm_flag 1 - lower capital letters without punctuation
# norm_flag 2 - remove punctuation
# norm_flag 3 - without punctuation and portuguese stop
# exp_flag is used to enumerate the exercise we want to run
# exp_flag	0 - first exercise
# exp_flag 	1->4 - the 4 experiences


echo 'Alinea 2'
echo 'Experiência 1'
norm_flag="2"
exp_flag="1"
python normalization.py $norm_flag 
python main.py $norm_flag $exp_flag

echo 'Experiência 2'
norm_flag="3"
exp_flag="2"
python normalization.py $norm_flag 
python main.py $norm_flag $exp_flag

echo 'Experiência 3'
norm_flag="2"
exp_flag="3"
python normalization.py $norm_flag 
python main.py $norm_flag $exp_flag


echo 'Experiência 4'
norm_flag="1"
exp_flag="4"
python normalization.py $norm_flag
python main.py $norm_flag $exp_flag

echo 'Alinea 1'
norm_flag="2"
exp_flag="0"
python normalization.py $norm_flag 
python main.py $norm_flag $exp_flag