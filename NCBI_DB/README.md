# This what a NCBI nucelotide DB must contains

You need to download and unpack:
* `nt` files, e.g. from `nt.000.tar.gz` to `nt.124.tar.gz` as of 2024-01-08 
* `taxdb-metadata.json`
* `taxdb.tar.gz` 
* `nt-nucl-metadata.json`

These are available here: https://ftp.ncbi.nlm.nih.gov/blast/db/

You also need to download:

* `taxdump.tar.gz`
* `taxdump_readme.txt`

These are available here: https://ftp.ncbi.nih.gov/pub/taxonomy/

After that you would need to make the file readable and executable using 

`chmod 755 *dmp`
`for i in ls nt* ; do chmod 755 $i; done`
`chmod 755 taxdb.bti`
`chmod 755 taxdb.btd`

TO check your database run, for example 
`blastdbcheck -db /mnt/research/bonito_lab/DATABASES/NCBInt_0124/nt`
