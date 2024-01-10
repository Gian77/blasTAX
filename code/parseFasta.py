import os
import argparse

def rename_reads(input_fasta, output_dir, prefix="query"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Output file for storing old and new read headers
    output_file_path = os.path.join(output_dir, "name_mapping.txt")

    # Set the output file name based on the input file
    #fixed_prefix = "parsed" 
    #new_name = f"{fixed_prefix}_{os.path.basename(input_fasta)}"
    new_name="parsed_input.fasta"

    # Open the output files
    with open(output_file_path, "w") as output_file, open(input_fasta, "r") as input_file:
        count = 0
        with open(os.path.join(output_dir, new_name), "w") as output_fasta:
            current_sequence = ""
            for line in input_file:
                if line.startswith(">"):
                    old_header = line.strip()
                    new_header = f"{prefix}_{count + 1}"
                    output_file.write(f"{old_header}\t{new_header}\n")
                    if current_sequence:
                        output_fasta.write(current_sequence + "\n")
                        current_sequence = ""
                    output_fasta.write(f">{new_header}\n")
                    count += 1
                else:
                    current_sequence += line.strip()

            # Write the last sequence
            if current_sequence:
                output_fasta.write(current_sequence + "\n")

    print(f"Renamed reads in: {input_fasta} to {os.path.join(output_dir, new_name)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename headers in a FASTA file.")
    parser.add_argument("input_fasta", help="Path to the input FASTA file")
    parser.add_argument("output_dir", help="Path to the output directory")
    parser.add_argument("--prefix", default="query", help="Custom prefix for the renamed reads")
    args = parser.parse_args()

    rename_reads(args.input_fasta, args.output_dir, args.prefix)

