import argparse
import os

# Assuming OTUs contain multuple hist is the string containing your blast hit line
# e.g. OTU_1611	1983000;1983018;1983033	211	96.124	1.92e-50	100	KY791277.1"

def modify_blast_output(input_file, output_file, output_dir):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line.startswith("#"):
                continue  # Skip comment lines
            fields = line.strip().split("\t")
            otu_id = fields[0]
            query_id = fields[1]
            taxon_ids = fields[2].split(";")  # Adjust index based on the actual position
            bitscore = fields[3]  # Assuming bitscore is in the 5th column
            e_value = fields[4]  # Assuming e-value is in the 4th column
            percent_identity = fields[5]  # Assuming percent identity is in the 6th column
            query_coverage = fields[6]

            for taxon_id in taxon_ids:
                new_line = "\t".join([otu_id, query_id, taxon_id, bitscore, e_value, percent_identity, query_coverage])
                outfile.write(new_line + "\n")

    # Check if the output directory exists, create it if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Move the modified file to the output directory
    output_path = os.path.join(output_dir, os.path.basename(output_file))
    os.rename(output_file, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify BLAST output.")
    parser.add_argument("-i", "--input", required=True, help="Input BLAST output file")
    parser.add_argument("-o", "--output", help="Output modified file")
    parser.add_argument("-d", "--output_dir", help="Output directory")
    args = parser.parse_args()

    # If output file name not provided, use a default name based on the input file
    if not args.output:
        args.output = os.path.splitext(os.path.basename(args.input))[0] + "_modified.txt"

    # If output directory not provided, use the directory of the input file
    if not args.output_dir:
        args.output_dir = os.path.dirname(args.input)

    modify_blast_output(args.input, args.output, args.output_dir)

