# Load software modules:
module load bioinfo-tools blast

# get sequences:
while read hit
do
  cur_seq=`echo $hit | awk '{print $1}'`
  range_fr=`echo $hit | awk '{print $3}'`
  range_to=`echo $hit | awk '{print $4}'`
  if [ $range_to -gt $range_fr ]
  then
    query=`echo $hit | awk '{print "-entry " $2 " -range " ($3 - 100) "-" ($4 + 200)}'`
    file_name="./fasta_files/$cur_seq.fa"
    touch $file_name
    echo "Running $query"
    blastdbcmd -db ../1_blast/$BLAST_DB $query >> $file_name
  else
    echo "Start is larger than stop for sequence $cur_seq"
  fi
done < ../1_blast/blast.out
