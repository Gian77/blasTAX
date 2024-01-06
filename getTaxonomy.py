import sys
import pandas as pd

# This script calculates the score at each rank and uses the same principles adopted by QIIME2 for 
# blast classified. The hits are filtered by those which pass thresholds for percent ID and e-value. 
# After that, the confidence of each rank is the percent of hits which agree with the most common 
# taxon for that rank. For example, a confidence of 0.8 for Tuber means that 4 of 5 hits passing 
# the filters have Tuber as the genus.

# Get arguments from command line
confidence = float(sys.argv[1])   
max_hits = int(sys.argv[2])
ethresh = float(sys.argv[3])  
p_iden_thresh = float(sys.argv[4])

blast_file = "taxonomy.blast" 
output_dir="."
output_file = f"{output_dir}/otu_taxonomy_blast_final.txt"
ranks = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]

def reformat_BLAST(blast_file, output_dir, confidence, max_hits, ethresh, p_iden_thresh, ranks):
  if ranks[0] == "Kingdom":
      classification_buf = "OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score"
      classification_buf += "\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n"
  else:
      classification_buf = "OTU_ID\tOTU_Score"
      for r in ranks:
          classification_buf += f"\t{r}\t{r.replace('ank_', '')}_score"
      classification_buf += "\n"

  blast_res = pd.read_csv(blast_file)  
  blast_res = blast_res.astype({"e_value": "float64", "query": "str"})
  uniq = pd.unique(blast_res["query"])

  for q in uniq:
      q_list = [q.split(" ")[0], "0.0"]  
      q_sub = blast_res[(blast_res["query"] == q) & (blast_res["e_value"] <= ethresh) & (blast_res["percent_identity"] >= p_iden_thresh)]

      if len(q_sub) == 0:
          q_list.extend([""] * len(ranks) * 2)
      else:
          q_sub = q_sub[:min([len(q_sub), max_hits])]
          for t in ranks:
              if t not in q_sub.columns and t == "Kingdom":
                  t = "Domain"
              vcs = q_sub[t].value_counts(normalize=True)
              if len(vcs) == 0 or "unidentified" in vcs.index[0] or vcs[0] < confidence or (
                      t == ranks[-1] and vcs.index[0].endswith("_sp")):
                  break
              else:
                  if "ncertae_sedis" in vcs.index[0]:
                      q_list.extend(["Incertae_sedis", str(vcs[0])]) 
                  else:
                      q_list.extend([vcs.index[0], str(vcs[0])])
                  q_list[1] = str(vcs[0])

      classification_buf += "\t".join(q_list) + "\n"

  with open(output_file, "w") as ofile:
      ofile.write(classification_buf)

  return output_file


# Call function with hardcoded blast_file and passed arguments
reformat_BLAST(blast_file, output_dir, confidence, max_hits, ethresh, p_iden_thresh, ranks)
