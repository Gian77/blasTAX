# *blasTAX*

### A taxonomy classifier program based on BLAST!

This is a standalone classifier for marker gene sequences, like those produced in microbiome studies, that form a `.fasta` file that outputs a taxonomy table with Kingdom, Phylum, Class, Order, Family, Genus, Species. The classification is made using [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) against the whole NCBI nt (nucleotide) sequence [database](https://ftp.ncbi.nlm.nih.gov/blast/db/) that must be available locally. Code to download the NCBI ​nt is provided in the `NCBI_DB` directory which are made to work in the SLURM system but they are easily convertible work directly from the terminal.

blasTAX calculates the score at each rank and uses the same principles adopted by QIIME2 for blast classified. The hits are filtered by those which pass thresholds for percent ID (percent identity) and e-value. After that, the confidence of each rank is the percent of hits which agree with the most common taxon for that rank. For example, a confidence of 0.8 for Tuber means that 4 of 5 hits passing the filters have Tuber as the genus.

To start, clone this repository using: `git clone git@github.com:Gian77/blasTAX.git`

Once cloned, download the whole NCBI nt database. An example run of `blasTAX` is like this below, assuming that the NCBI database is in my `home/`, my sequences are in the `sequences` directory as `test.fasta` and that I want all the output in a directory called `output`.

`bash blasTAX.sh -i /mnt/home/benucci/blasTAX/sequences/test.fasta -d /mnt/home/benucci/blasTAX/NCBI_DB/nt -t 16 --max_hits 25 -c 0.65 -e 0.001 -p 90.0 -o /mnt/home/benucci/blasTAX/outputs`

If you use this, please ​add a star ​to the repo and drop me a comment.

### Acknowledgments
A huge thanks goes to [Julian Liber](https://github.com/liberjul) since part of the code is from the software [CONSTAX](https://constax.readthedocs.io/en/latest/).

