results_dir="../4_run_primer3/output_files/"
inputs_dir="../3_make_p3_input/generated_inputs/"

rev_comp()
{
  python3 ~/CGIBashScripts/subscripts/pmocver.py $1
}

echo "locus;fwd_primer;rev1_seq;rev1_rvcmp;amp1_len;rev2_seq;rev2_rvcmp;amp2_len;rev3_seq;rev3_rvcmp;amp3_len;rev4_seq;rev4_rvcmp;amp4_len;rev5_seq;rev5_rvcmp;amp5_len;rev6_seq;rev6_rvcmp;amp6_len;rev7_seq;rev7_rvcmp;amp7_len;rev8_seq;rev8_rvcmp;amp8_len;rev9_seq;rev9_rvcmp;amp9_len;rev10_seq;rev10_rvcmp;amp10_len;full_seq"
for file in $results_dir*.rev
do
  input_file=${file/$results_dir/$inputs_dir}
  raw_loc=${file/$results_dir/""}
  cur_loc=${raw_loc/".rev"/""}
  raw_seq=`tail -n +2 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_seq=${raw_seq/"SEQUENCE_TEMPLATE="/""}
  raw_fwd=`tail -n +3 ${input_file/".rev"/"_p3_input.txt"} | head -1`
  cur_fwd=${raw_fwd/"SEQUENCE_PRIMER="/""} # this is the shortened one
  cur_rev1=`tail -n +4 $file | head -1 | awk '{print $2}'`
  cur_rev2=`tail -n +5 $file | head -1 | awk '{print $2}'`
  cur_rev3=`tail -n +6 $file | head -1 | awk '{print $2}'`
  cur_rev4=`tail -n +7 $file | head -1 | awk '{print $2}'`
  cur_rev5=`tail -n +8 $file | head -1 | awk '{print $2}'`
  cur_rev6=`tail -n +9 $file | head -1 | awk '{print $2}'`
  cur_rev7=`tail -n +10 $file | head -1 | awk '{print $2}'`
  cur_rev8=`tail -n +11 $file | head -1 | awk '{print $2}'`
  cur_rev9=`tail -n +12 $file | head -1 | awk '{print $2}'`
  cur_rev10=`tail -n +13 $file | head -1 | awk '{print $2}'`
  cur_rvcmp1=`rev_comp $cur_rev1`
  cur_rvcmp2=`rev_comp $cur_rev2`
  cur_rvcmp3=`rev_comp $cur_rev3`
  cur_rvcmp4=`rev_comp $cur_rev4`
  cur_rvcmp5=`rev_comp $cur_rev5`
  cur_rvcmp6=`rev_comp $cur_rev6`
  cur_rvcmp7=`rev_comp $cur_rev7`
  cur_rvcmp8=`rev_comp $cur_rev8`
  cur_rvcmp9=`rev_comp $cur_rev9`
  cur_rvcmp10=`rev_comp $cur_rev10`
  cur_len1=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp1" | wc -m`
  cur_len2=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp2" | wc -m`
  cur_len3=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp3" | wc -m`
  cur_len4=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp4" | wc -m`
  cur_len5=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp5" | wc -m`
  cur_len6=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp6" | wc -m`
  cur_len7=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp7" | wc -m`
  cur_len8=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp8" | wc -m`
  cur_len9=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp9" | wc -m`
  cur_len10=`echo $cur_seq | grep -o "$cur_fwd.*$cur_rvcmp10" | wc -m`
  echo "$cur_loc;$cur_fwd;$cur_rev1;$cur_rvcmp1;$cur_len1;$cur_rev2;$cur_rvcmp2;$cur_len2;$cur_rev3;$cur_rvcmp3;$cur_len3;$cur_rev4;$cur_rvcmp4;$cur_len4;$cur_rev5;$cur_rvcmp5;$cur_len5;$cur_rev6;$cur_rvcmp6;$cur_len6;$cur_rev7;$cur_rvcmp7;$cur_len7;$cur_rev8;$cur_rvcmp8;$cur_len8;$cur_rev9;$cur_rvcmp9;$cur_len9;$cur_rev10;$cur_rvcmp10;$cur_len10;$cur_seq"
done
