min_len=120 # minimum amplicon size (if none of this size exists, longest one shorter than this is picked)
max_len=180 # maximum anplicon size

results_dir="../4_run_primer3/output_files/"
inputs_dir="../3_make_p3_input/generated_inputs/"

rev_comp()
{
  python3 ~/CGIBashScripts/subscripts/pmocver.py $1
}

pick_primer() { # pick the best primer that generates the right amplicon size
  filenm="$1" # name of primer3 result file
  minlen=$2 # minimum amplicon size
  maxlen=$3 # maximum amplicon size
  fwdprm="$4" # forward primer
  fllseq="$5" # full sequence
  countr=1 # result file line counter
  bstlen=0 # longest length so far shorter than maxlen
  while read primer_res
  do
    cur_numb=`echo $primer_res | awk '{print $1}'` # get primer index
    cur_prim=`echo $primer_res | awk '{print $2}'` # get reverse primer
    cur_revcomp=`rev_comp $cur_prim` # reverse complement primer
    curlen=`echo $fllseq | grep -o "$fwdprm.*$cur_revcomp" | wc -m` # get amplicon size
    if [ $curlen -gt $minlen ] && [ $curlen -lt $maxlen ] && [ $countr -gt 3 ]
    then
      correct_prim=$cur_prim # pick this primer if it gives the right size of amplicon
      break
    elif [ $curlen -gt 1 ] && [ $curlen -gt $bstlen ] && [ $curlen -lt $maxlen ]
    then
      correct_prim=$cur_prim # save the best primer so far
      bstlen=$curlen
    fi
    countr=$((countr + 1))
  done < ./$filenm
  echo "$cur_numb;$correct_prim" # return primer index and primer
}

echo "locus;fwd_primer;primer_index;rev_seq;rev_rvcmp;amp_len;full_seq"
for file in $results_dir*.rev
do
  input_file=${file/$results_dir/$inputs_dir}
  raw_loc=${file/$results_dir/""}
  cur_loc=${raw_loc/".rev"/""}
  raw_seq=`tail -n +2 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_seq=${raw_seq/"SEQUENCE_TEMPLATE="/""}
  raw_fwd=`tail -n +3 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_fwd=${raw_fwd/"SEQUENCE_PRIMER="/""} # this is the shortened one
  primer_pick=`pick_primer "$file" $min_len $max_len $cur_fwd $cur_seq`
  primer_arr=(${primer_pick//;/ })
  cur_ind=${primer_arr[0]}
  cur_rev=${primer_arr[1]}
  cur_rvcmp=`rev_comp $cur_rev`
  cur_len=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp" | wc -m`
  echo "$cur_loc;$cur_fwd;$cur_ind;$cur_rev;$cur_rvcmp;$cur_len;$cur_seq"
done
