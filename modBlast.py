import argparse

# Assuming OTUs contain multuple hist is the string containing your blast hit line
# e.g. OTU_1611	1983000;1983018;1983033	211	96.124	1.92e-50	100	KY791277.1"

import argparse

def modify_blast_output(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line.startswith("#"):
                continue  # Skip comment lines
            fields = line.strip().split("\t")
            otu_id = fields[0]
            query_id = fields[1]
            taxon_ids = fields[2].split(";")  # Adjust index based on the actual position
            bitscore = fields[3] # Assuming bitscore is in the 5th column
            e_value = fields[4]  # Assuming e-value is in the 4th column
            percent_identity = fields[5]  # Assuming percent identity is in the 6th column
            query_coverage = fields[6]

            for taxon_id in taxon_ids:
                new_line = "\t".join([otu_id, query_id, taxon_id, bitscore, e_value, percent_identity, query_coverage])
                outfile.write(new_line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify BLAST output.")
    parser.add_argument("-i", "--input", required=True, help="Input BLAST output file")
    parser.add_argument("-o", "--output", required=True, help="Output modified file")
    args = parser.parse_args()

    modify_blast_output(args.input, args.output)

