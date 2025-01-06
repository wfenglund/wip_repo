# Script to update one fasta file with sequences from another (reference) fasta file.
# All fasta names that exist in both will be printed as the reference sequence, otherwise the old one is kept.

# import sys

old_file = './fasta_file.fa' # file with sequences
ref_file = './reference_fasta_file.fa' # file with reference sequences

def parse_fasta(fasta_file):
    fasta_dict = {}
    with open(fasta_file) as in_file:
        for line in in_file:
            if line.startswith('>'):
                fasta_name = line.strip()
            else:
                fasta_dict[fasta_name] = line.strip()
    return fasta_dict

old_dict = parse_fasta(old_file)
ref_dict = parse_fasta(ref_file)

new_dict = {}
for key in old_dict.keys():
    if key in ref_dict.keys():
#         print(f'{key} is updated.', file=sys.stderr)
        new_dict[key] = ref_dict[key]
    else:
        new_dict[key] = old_dict[key]

for key in new_dict.keys():
    print(key)
    print(new_dict[key])
