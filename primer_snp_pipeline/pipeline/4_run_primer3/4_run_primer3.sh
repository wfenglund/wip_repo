# Load software modules:
module load bioinfo-tools Primer3

# Run primer3 for every input file:
run_p3()
{
  for input_file in ../3_make_p3_input/generated_inputs/*
  do
    primer3_core < $input_file
  done
}
run_p3 | tee log.out # run script and also save output to log.out

# Move output files to output folder:
mv *.rev ./output_files/
