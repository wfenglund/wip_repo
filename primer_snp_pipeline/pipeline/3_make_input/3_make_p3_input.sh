# Load software modules:
module load bioinfo-tools
module load emboss

# Create one primer3 input file per fasta file:
for fasta_file in ../2_get_sequences/fasta_files/*.fa
do
  fasta_name=${fasta_file/".fa"/""}
  fasta_name=${fasta_name/"../2_get_sequences/fasta_files/"/""}
  output="./input_files/"$fasta_name"_p3_input.txt"
  touch $output
  nseq=`grep ">" $fasta_file | wc -l`
  if [ $nseq -gt 1 ] # if fasta file contains several sequences
  then
    echo $fasta_file
    conseq=`cons -sequence $fasta_file -stdout -auto | tail -n +2`
  elif [ $nseq == 1 ] # if fasta file contains exactly one sequence
  then
    conseq=`cat $fasta_file | tail -n +2` # take the sequence and not the name
  fi
  conseq=`echo $conseq | tr -d '[:blank:]'`
  echo "SEQUENCE_ID=$fasta_name" >> $output
  echo "SEQUENCE_TEMPLATE=$conseq" >> $output
  cat primer3_settings.txt >> $output
done
