# Load software modules:
module load bioinfo-tools blast

# get sequences:
while read hit
do
  query=`echo $hit | awk '{print "-entry " $2 " -range " ($3 - 100) "-" ($4 + 100)}'`
  file_name=`echo $hit | awk '{print "./fasta_files/" $1 ".fa"}'`
  touch $file_name
  echo $query
  blastdbcmd -db ../1_blast/$BLAST_DB $query >> $file_name
done < ../1_blast/blast.out
