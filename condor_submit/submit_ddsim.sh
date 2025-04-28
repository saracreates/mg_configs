#!/bin/bash

# shell script to submit analysis job to the batch system
echo "Running analysis job ..."
start_time=$(date +%s)

# source key4ehp
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-01-28

# get input parameters 
FROM_I=${1} # Which index to start with regarding the input root files
NUM_FILES=${2} # number of files to process
OUTPUT_FILE=${3} # output file

# input files 


# make directory
mkdir -p job

# copy input files
input_file="/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/pythia8_higgsgamma.hepmc" # CHANGE input file here
base_name=$(basename "${input_file}")
# Copy the file using the Python script
python3 /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py "${input_file}" "./job/${base_name}"

# run the script
echo "time before running script: $middle_time seconds" 
ddsim --inputFiles ./job/${base_name} \
  -N ${NUM_FILES} \
  --skipNEvents ${FROM_I} \
	--steeringFile $CLDCONFIG/share/CLDConfig/cld_steer.py \
	--compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v05/CLD_o2_v05.xml \
	--outputFile ./job/out.root
echo "job done ... "
job_endtime=$(date +%s)

output_dir=$(dirname "${OUTPUT_FILE}")
# make directory if it does not exist:
if [ ! -d ${output_dir} ]; then
  mkdir -p ${output_dir}
fi

# copy file to output dir
python3 /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py ./job/out.root ${OUTPUT_FILE}
echo "Ran script successfully!"
end_time=$(date +%s)
execution_time=$((end_time - start_time)) # rouhgly 2h for index 0 to 1000
echo "Execution time: $execution_time seconds"

