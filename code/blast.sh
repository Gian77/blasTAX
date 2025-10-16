#!/bin/bash 

# Use example: 
# sh runBlast.sh test.fasta /mnt/research/glbrc_group/benuccigmn/DATABASES/NCBI_core_nt/core_nt 16 25

#eval "$(conda shell.bash hook)"
#conda activate blasTAX

# Set default values
outfmt="\"6 qacc sacc staxids bitscore evalue pident qcovs\"" # backslash will escape the quotes
output_dir="."

query="$1"
db="$2"
threads="$3"
max_target_seqs="$4"
out_dir="$5"

# query="test.fasta"
# db="/mnt/research/glbrc_group/benuccigmn/DATABASES/NCBI_core_nt/core_nt"
# threads=16
# max_target_seqs=20

# Construct and run command
blast_cmd="blastn -query $query -db $db -num_threads $threads -outfmt $outfmt -max_target_seqs $max_target_seqs > ${out_dir}/blast.out"

echo $blast_cmd
eval "$blast_cmd"

#conda deactivate
