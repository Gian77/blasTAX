#!/bin/bash

cat << "EOF"
     _      _             _____   _    __  __
    | |__  | |  __ _  ___|_   _| / \   \ \/ /
    | '_ \ | | / _` |/ __| | |  / _ \   \  / 
    | |_) || || (_| |\__ \ | | / ___ \  /  \ 
    |_.__/ |_| \__,_||___/ |_|/_/   \_\/_/\_\
    ******************************************
   ********************************************                                         
EOF

echo -e "
** A taxonomy classifier program based on BLAST! **\n
blasTAX v.1.0 by Gian M. N. Benucci, P.hD.
email: benucci[at]msu[dot]edu
January 05, 2024\n"

# Function to display help
show_help() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -i, --input_file     Specify the input file with sequences in fasta format."
  echo "  -d, --database       Specify the database path (default: /mnt/research/EvansLab/DATABASES/NCBInt_feb23/nt)"
  echo "  -t, --threads        Specify the number of threads (default: 16)"
  echo "  -m, --max_hits       Specify the number of threads (default: 25)"
  echo "  -c, --confidence     Specify the confidence level (default: 0.7)"
  echo "  -e, --ethresh        Specify the E-value threshold (default: 0.001)"
  echo "  -p, --p_iden_thresh  Specify the percent identity threshold (default: 95.0)"
  echo "  -o, --out_dir        Specify the output directory (default: current directory)"
  echo "  -h, --help           Display this help message"
  exit 0
}

# Default values
input_file=train.fasta
db="/mnt/research/EvansLab/DATABASES/NCBInt_feb23"
threads=16
max_hits=25
confidence=0.7
ethresh=0.001
p_iden_thresh=95.0
out_dir="."

# Parse options
while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--input_file)
      input_file="$2"
      shift # past argument
      ;;
    -d|--database)
      db="$2"
      shift # past argument
      ;;
    -t|--threads)
      threads="$2"
      shift # past argument  
      ;;
    -m|--max_hits)
      max_hits="$2"
      shift # past argument
      ;; 
    -c|--confidence)
      confidence="$2"
      shift # past argument
      ;; 
    -e|--ethresh)
      ethresh="$2"
      shift # past argument
      ;;
    -p|--p_iden_thresh)
      p_iden_thresh="$2"
      shift # past argument
      ;;
    -o|--out_dir)
      out_dir="$2"
      shift # past argument
      ;;
    -h|--help)
      show_help
      ;;
  esac
  shift # past argument or value
done

# Activate conda environment
#source /mnt/home/benucci/anaconda2/bin/activate BLAST
eval "$(conda shell.bash hook)"
conda activate BLAST

echo -e ">>>> Rename input .fasta file <<<<\n"
python code/parseFasta.py $input_file ${out_dir} --prefix Query

echo -e ">>>> Running BLAST <<<<\n"
sh code/blast.sh ${out_dir}/parsed_input.fasta $db/nt $threads $max_hits $out_dir
echo -e "\nBLAST hits obtained. Moving on...\n"

# modify the output to spread the hits that gave the same score
python code/modBlast.py -i ${out_dir}/blast.out -o ${out_dir}/blast_mod.out -d $out_dir
 
# extract taxids and generate taxonomy lineage from taxids
cut -f 1,3 ${out_dir}/blast_mod.out > ${out_dir}/taxids.txt

# Need to modify the db variable for taxonkit
#NCBI_nt=$(echo $db | cut -d"/" -f1,2,3,4,5,6) 
grep "Query" ${out_dir}/taxids.txt | cut -f 2 | taxonkit reformat -I 1 --threads $threads --data-dir $db > ${out_dir}/full_lineage.txt

paste ${out_dir}/blast_mod.out ${out_dir}/taxids.txt ${out_dir}/full_lineage.txt > ${out_dir}/taxformat.txt

cat ${out_dir}/taxformat.txt | tr "\t" "," | tr ";" "," | cut -d"," -f 1,2,4,5,6,7,11,12,13,14,15,16,17 | sed '1i query,subject,bitscore,e_value,percent_identity,query_coverage,Kingdom,Phylum,Class,Order,Family,Genus,Species' > ${out_dir}/taxonomy.blast

echo -e "\n>>>> Generating taxonomy file <<<<\n"
echo -e "python getTaxonomy.py -c $confidence -m $max_hits -e $ethresh -p $p_iden_thresh -o $out_dir\n"
python code/getTaxonomy.py $confidence $max_hits $ethresh $p_iden_thresh $out_dir

conda deactivate

echo -e ">>>> All done! <<<<\n"
