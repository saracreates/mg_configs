import os 
import glob

def generate_analysis_sub():
    num_events = 1400 # this take a bit more than 3h
    max_events = 75000 
    input_base = "/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/ddsim_higgsgamma/"
    output_base = "/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/reco_higgsgamma/"
    
    # Prepare the header of the file
    header = """# run commands for analysis,

# here goes your shell script
executable    = submit_ddsim.sh
#requirements = (OpSysAndVer =?= "CentOS7")
# here you specify where to put .log, .out and .err files
output                = /afs/cern.ch/work/s/saaumill/public/condor/std-reco/job.$(ClusterId).$(ProcId).out
error                 = /afs/cern.ch/work/s/saaumill/public/condor/std-reco/job.$(ClusterId).$(ProcId).err
log                   = /afs/cern.ch/work/s/saaumill/public/condor/std-reco/job.$(ClusterId).$(ClusterId).log

+AccountingGroup = "group_u_FCC.local_gen"
+JobFlavour    = "workday"
"""

    # Prepare the content with arguments
    # consider updating this with https://htcondor.readthedocs.io/en/latest/faq/users/convert-multi-q-statements.html 
    content = ""
    job_counter = 0

    # List all .root files in input_base
    input_files = sorted(glob.glob(os.path.join(input_base, "*.root")))

    for input_file in input_files:
        output_file = f"{output_base}reco_higgsgamma_{job_counter}.root"
        arguments = f"{input_file} {output_file}"
        content += f"arguments=\"{arguments}\"\nqueue\n"
        job_counter += 1

    # Write to the analysis.sub file
    with open("reco.sub", "w") as file:
        file.write(header)
        file.write(content)

# Run the function to generate the file
generate_analysis_sub()
