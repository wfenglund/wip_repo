# Script that counts sequences in fastq-files in subfolders and reports how many loci had at least a minimum value of sequences
# Assumes that sample_folder contains at least one subfolder with fastq files
# Assumes that fastq files are named like [locus name]_[something]_[sample name]-CJ[etc].gz, example:
# Ua-snp-01y_Unknown_A11BMK241107-CJ594-ZX01-010001-01.merged.fq.gz.fastq.gz

sample_folder="./Filtered_data/SNP_*/" # assumes that fastq files are divided into separate folders starting with 'SNP_'
minimum_seqs=$1 # takes first argument from the command line

if ! [[ -n $minimum_seqs ]]
then
  minimum_seqs=1 # if no threshold is given, set it at 1
fi

echo "Number of loci containing at least $minimum_seqs sequences:"
echo ""

for method in $sample_folder # for every folder
do
  echo $method
  samples=`for i in $method/*.gz ; do i=${i/*_} ; echo ${i/-CJ*} ; done | sort | uniq`
  for sample in $samples
  do
    echo $sample":"
    counter=0
    for locus in $method/*$sample*
    do
      n_seqs=`zgrep "^@" $locus | wc -l`
      if [[ $n_seqs -gt $minimum_seqs ]]
      then
        current=1
      else
        current=0
	echo "- ${locus/$method"/"/""/} only has $n_seqs sequences."
      fi
      counter=$((counter + current))
    done
    echo $counter"/"`ls $method/*$sample* | wc -l`
  done
  echo ""
done
