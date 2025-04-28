import math

def generate_analysis_sub():
    num_events = 1400 # this take a bit more than 3h
    max_events = 75000 
    # input_file = "/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/pythia8_higgsgamma.hepmc"
    output_base = "/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/ddsim_higgsgamma/"
    
    # Prepare the header of the file
    header = """# run commands for analysis,

# here goes your shell script
executable    = submit_ddsim.sh
#requirements = (OpSysAndVer =?= "CentOS7")
# here you specify where to put .log, .out and .err files
output                = /afs/cern.ch/work/s/saaumill/public/condor/std-ddsim/job.$(ClusterId).$(ProcId).out
error                 = /afs/cern.ch/work/s/saaumill/public/condor/std-ddsim/job.$(ClusterId).$(ProcId).err
log                   = /afs/cern.ch/work/s/saaumill/public/condor/std-ddsim/job.$(ClusterId).$(ClusterId).log

+AccountingGroup = "group_u_FCC.local_gen"
+JobFlavour    = "workday"
"""

    # Prepare the content with arguments
    # consider updating this with https://htcondor.readthedocs.io/en/latest/faq/users/convert-multi-q-statements.html 
    content = ""
    job_counter = 0
    i = 0
    mylist = []
    while (i<max_events):
        output_file = f"{output_base}ddsim_higgsgamma_{job_counter}.root"
        arguments = f"{i} {num_events} {output_file}"
        content += f"arguments=\"{arguments}\"\nqueue\n"
        job_counter += 1
        i += num_events

    # Write to the analysis.sub file
    with open("ddsim.sub", "w") as file:
        file.write(header)
        file.write(content)

# Run the function to generate the file
generate_analysis_sub()
