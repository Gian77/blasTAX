#!/bin/bash 

# Use example: 
# sh runBlast.sh test.fasta /mnt/research/EvansLab/DATABASES/NCBInt_feb23/nt 16 25

eval "$(conda shell.bash hook)"
conda activate BLAST

# Set default values
outfmt="\"6 qacc sacc staxids bitscore evalue pident qcovs\"" # backslash will escape the quotes
output_dir="."

query="$1"
db="$2"
threads="$3"
max_target_seqs="$4"

# query="test.fasta"
# db="/mnt/research/EvansLab/DATABASES/NCBInt_feb23/nt"
# threads=16
# max_target_seqs=20

# Construct and run command
blast_cmd="blastn -query $query -db $db -num_threads $threads -outfmt $outfmt -max_target_seqs $max_target_seqs > blast.out"

echo $blast_cmd
eval "$blast_cmd"

conda deactivate
