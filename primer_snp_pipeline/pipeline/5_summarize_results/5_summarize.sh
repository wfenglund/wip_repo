results_dir="../4_run_primer3/output_files/"
inputs_dir="../3_make_p3_input/generated_inputs/"

for file in $results_dir*.rev
do
  input_file=${file/$results_dir/$inputs_dir}
  raw_seq=`tail -n +2 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_seq=${raw_seq/"SEQUENCE_TEMPLATE="/""}
  raw_fwd=`tail -n +3 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_fwd=${raw_fwd/"SEQUENCE_PRIMER="/""}
  echo $cur_seq # full sequence
  echo $cur_fwd # forward primer
  tail -n +4 $file | head -3 | awk '{print $2}' # top three reverse primers

  # todo:
  ## figure out top three primers
  ## figure out amplicon for each, print each primer followed by each length
  ## final row to be put in file should be:
  ### locus;fwd;rev1;len1;rev2;len2;rev3;len3;full_sequence
done
