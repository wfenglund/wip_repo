# Load software modules:
module load bioinfo-tools blast

# create output file:
touch seqs_hits.fa

# get sequences:
while read hit
do
	query=`echo $hit | awk '{print "-entry " $2 " -range " $3 "-" $4}'`
	blastdbcmd -db ../1_blast/$BLAST_DB $query >> seqs_hits.fa
done < ../1_blast/blast.out
