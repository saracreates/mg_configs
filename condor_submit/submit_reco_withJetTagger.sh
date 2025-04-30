#!/bin/bash

# shell script to submit analysis job to the batch system
echo "Running analysis job ..."
start_time=$(date +%s)

# source key4ehp
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh # tagger is only included in the nighlties
# source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-01-28

# get input parameters 
INPUT_FILE=${1} # Which index to start with regarding the input root files
OUTPUT_FILE=${2} # output file

# make directory
cluster_loc=$(pwd)
mkdir -p job

# copy input files
base_name=$(basename "${INPUT_FILE}")
# Copy the file using the Python script
python3 /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py "${INPUT_FILE}" "./job/${base_name}"

# run the script
echo "time before running script: $middle_time seconds" 

# each input file has 700 events ...
cd /afs/cern.ch/work/s/saaumill/public/CLDConfig/CLDConfig/
# go on jet-impl branch - this has the tagger included and CLD_v5 as a detector version locally 
k4run CLDReconstruction.py --inputFiles ${cluster_loc}/job/${base_name} \
 --outputBasename ${cluster_loc}/job/out \
 -n 700 \
 --enableLCFIJet \
 --enableMLJetTagger \
 

echo "job done ... "
job_endtime=$(date +%s)

cd ${cluster_loc}

output_dir=$(dirname "${OUTPUT_FILE}")
# make directory if it does not exist:
if [ ! -d ${output_dir} ]; then
  mkdir -p ${output_dir}
fi

# print all output files available
echo "Output files available:"
ls -l ./job/

# copy file to output dir
python3 /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py ./job/out.edm4hep.root "${OUTPUT_FILE}"

echo "Ran script successfully!"
end_time=$(date +%s)
execution_time=$((end_time - start_time)) # rouhgly 2h for index 0 to 1000
echo "Execution time: $execution_time seconds"

