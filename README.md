# *blasTAX*

### A taxonomy classifier program based on BLAST!

This is a standalone classifier for marker gene sequences, like those produced in microbiome 
studies, that form a `.fasta` file that outputs a taxonomy table with Kingdom, Phylum, Class, 
Order, Family, Genus, Species and confidence scores at each rank. The classification is made 
using [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) against the whole NCBI nt (nucleotide) 
sequence [database](https://ftp.ncbi.nlm.nih.gov/blast/db/) that must be available locally. 

**blasTAX** calculates the score at each rank and uses the same principles adopted by 
[QIIME2](https://qiime2.org/) for classification with BLAST. The hits are filtered by those 
which pass thresholds for percent ID (percent identity) and e-value. After that, the 
confidence of each rank is the percent of hits which agree with the most common taxon for that
 rank. For example, a confidence of 0.8 for *Tuber* means that 4 of 5 hits passing the filters
 have *Tuber* as the genus.

To start, clone this repository using: `git clone git@github.com:Gian77/blasTAX.git`

Once cloned, download the whole NCBI nt database. Code to download the NCBI ​nt is provided in 
the `NCBI_DB` directory which are made to work in the SLURM system but they are easily 
convertible work directly from the terminal.

After that, you should install the two necessary softwares: `BLAST` and `taxonkit`. **blasTAX** 
is written to use a `conda` environemnt for this purpose that is called *BLAST*. To generate 
the conda environment you need to have a version of anaconda or miniconda installed. Please 
refer to [this](https://docs.anaconda.com/free/anaconda/install/index.html) link. 
In the `condaEnv/` directory you can find a file called `blasTAX.yml` that you should use to 
regenerate the **blasTAX** conda environment. Both *BLAST* and *taxonkit* may be updated in 
the future so it is up to you if you want to use the newwest versions.

To generate the required conda environment, from the cloned **blasTAX** repo, use:

`conda env create -f condaEnv/blasTAX.yml`

An example run of **blasTAX** is like this below, assuming that the NCBI database is in my 
`home/`, my sequences are in the `sequences/` directory as `test.fasta` and that I want all
 the output in a directory called `output`.

```
conda activate blasTAX

bash blasTAX.sh \
	-i /mnt/home/benucci/blasTAX/sequences/test.fasta \
	-d /mnt/home/benucci/blasTAX/NCBI_DB/nt \
	-t 16 \
	--max_hits 25 \
	-c 0.65 \
	-e 0.001 \
	-p 90.0 \
	-o /mnt/home/benucci/blasTAX/outputs`
```

A `blasTAX-SLURM.sb` and a `blasTAX-SLURM-ARRAY.sb` are also provided if you run it within an HPC 
that runs SLURM and if you want to run it through an array. For the latter, you can generate an 
array using `generateArray.sh` in the `array/` directory where all the `.fasta` files with the
sequences you want to classify should be placed.

An example of 20 sequences called `test.fasta` is given in the `sequences/` directory. All the 
generated **blasTAX** results are also provided in the `outputs/` directory.

By default, **blasTAX** renames your sequeunce headers to *Query_1, Query_2, ..., etc.* The orginal
headers, as well as, the new headers are written in the file `outputs/name_mapping.txt`.

If you use this, please ​add a star ​to the repo and drop me a comment. Soon to have a real citation!

### Advantages of **blasTAX**

* It is easy to install and run.
* It is a standalone program.
* It can be used with any DNA sequence.
* It could be easily integerated into a pipeline.
* It is scalabale.

### Acknowledgments
A huge thanks goes to [Julian Liber](https://github.com/liberjul) since part of the code is from the 
software [CONSTAX](https://constax.readthedocs.io/en/latest/).
