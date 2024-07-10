#! /bin/bash -l
#SBATCH -p core
#SBATCH -n 20
#SBATCH -t 4:00:00
#SBATCH -J blast_target

# go to this directory:
cd $PROJECT_DIR/primer_snp_pipeline/pipeline/1_blast

# load software modules:
module load bioinfo-tools blast

# blast sequences:
blastn -query ./$BLAST_DB -db nt -out ./blast.out -outfmt "6 sacc sstart send evalue pident sscinames" -max_target_seqs 10 -num_threads 20
