# Extract sequences and forward primers from csv-file with awk and sed (replacing the snp with an N).
#
# Forward primer will be written in the fasta sequence name after three underscores '___'.
#
# This script assumes that:
# 1. The input is a semi-colon separated file (with a header, since first line will be ignored).
# 2. That the name of the sequence is located in column 3
# 3. That the sequence is located in column 9
# 4. That the forward primer is located in column 12
#
# Generate fasta file:
tail -n +2 Copy\ of\ Ua_2018_8941FSTP18T1_DESIGN.csv | awk 'BEGIN{FS=";"};{print ">"$3"___"$12 "\n" $9}' | sed 's/\[\w\/\w\]/N/g' > sequences.fa
