module load bioinfo-tools
module load emboss

for fasta_file in ../2_get_sequences/fasta_files/*.fa
do
  # parse sequence info:
  fasta_raw=${fasta_file/".fa"/""}
  fasta_raw=${fasta_raw/"../2_get_sequences/fasta_files/"/""}
  fasta_name=`echo $fasta_raw | awk 'BEGIN{FS="___"};{print $1}'`
  output="./generated_inputs/"$fasta_name"_p3_input.txt"
  fw_primer=`echo $fasta_raw | awk 'BEGIN{FS="___"};{print $2}'`
  
  # get sequence(s), make consensus if there are several:
  nseq=`grep ">" $fasta_file | wc -l`
  if [ $nseq -gt 1 ] # if there are more than one sequence in file
  then
    echo $fasta_file
    conseq=`cons -sequence "$fasta_file" -stdout -auto | tail -n +2`
  elif [ $nseq == 1 ] # if there is only one sequence in file
  then
    conseq=`cat $fasta_file | tail -n +2`
  fi
  conseq=`echo $conseq | tr -d '[:blank:]'`

  # write output:
  touch $output
  echo "SEQUENCE_ID=$fasta_name" >> $output
  echo "SEQUENCE_TEMPLATE=$conseq" >> $output
  echo "SEQUENCE_PRIMER=$fw_primer" >> $output
  cat primer3_settings.txt >> $output
done
