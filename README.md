# Using MadGraph for event generation at FCC-ee

We want to so some fancy FCC anlaysis! Normally we use whizard for event generation and then have centrally produced files. But when we want to use MadGraph instead of Whizard, we need a pipeline to use pythia, then delphes and then get a edm4hep file as an output. This repo stores my configs and information about this pipeline.

## 1. Create `.lhe` files with MadGraph

(! `mg5_aMC` is included in the `key4hep` stack, so consider using that instead of the procedure described here!)

- install MadGraph locally by downloading it from [here](https://launchpad.net/mg5amcnlo).
- then go into the folder and launch Madgraph with `.bin/mg5_aMC` and providing a config file like the ones found in the `madgraph_configs` in this repo!

E.g. for me, this looks like:

```
cd /afs/cern.ch/work/s/saaumill/public/MG5_aMC_v3_5_7
./bin/mg5_aMC ./../madgraph_to_edm4hep_pipeline/madgraph_configs/ee_llZZ.dat
```


## 2a. Use pythia and delphes (fast sim)

We use the `DelphesPythia8_EDM4HEP` module from the key4hep software stack to propagate our `.lhe` files through pythia, then delphes to then get an edm4hep output. The config files for this step can be found in the `pythia_to_delphes_to_edm4hep` folder! 

E.g.

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh 

cd /afs/cern.ch/work/s/saaumill/public/mg_configs/pythia_to_delphes_to_edm4hep

DelphesPythia8_EDM4HEP \
	card_IDEA.tcl \
	edm4hep_IDEA.tcl \
	p8_ee_Hgamma_ecm240.cmd \
	p8_ee_Hgamma_ecm240.root 

```

## 2b. Use `k4run` for pythia (full sim)

For full sim samples, we want to

1. Apply pythia8 and get edm4hep files outputs

	We need an option file for `k4run`, see `./k4run_for_fullim/config_run_pythia8.py`. I have adapted this from this [example config](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/options/pythia.py). I adapted the path of the pythia config to point to a pythia config similar to the fast sim one. But we need to *turn off vertex smearing* in both, the `./k4run_for_fullim/p8_ee_Hgamma_ecm240.cmd` and `./k4run_for_fullim/config_run_pythia8.py` because it is done in `ddsim` now. 

	To run pythia8 over the LH event files from MadGraph, run:

	```
	source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh 

	cd /afs/cern.ch/work/s/saaumill/public/mg_configs/k4run_for_fullsim/

	k4run config_run_pythia8.py
	```

	This will produce a `.root` file. (At the moment, then can not be processed with `ddsim` in the next step... but should work in the future)


	**Alternative solution**
	Use the `pythiaLHERunner` which produced `.hepmc` files. 
	
	*Approach 1*: check the source file [here](https://github.com/key4hep/k4GeneratorsConfig/blob/2eab3f7757bf26218e2cb2248b3d3b5a05c99e63/k4GeneratorsConfig/src/pythiaLHERunner.cxx) and check if `pythia.settings.addFlag("Main:writeHepMC",true);`

	Source the latest stable key4hep stack and run it via: 

	```
	source /cvmfs/sw.hsf.org/key4hep/setup.sh 
	cd ./k4run_for_fullsim

	pythiaLHERunner -f p8_ee_Hgamma_ecm240.cmd -l /path/to/lhe/unweighted_events.lhe -o /output/path/pythia8_higgsgamma.hepmc
	```

	*Approach 2*: If approach 1 is not working, e.g. because the `writeHepMC` option is false, modify the file locally by wgetting it [here](https://raw.githubusercontent.com/key4hep/k4GeneratorsConfig/2eab3f7757bf26218e2cb2248b3d3b5a05c99e63/k4GeneratorsConfig/src/pythiaLHERunner.cxx) and compile it to the latest *stable* stack with 

	```
	LD_LIBRARY_PATH=/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/hepmc3/3.3.0-c2oek4/lib:$LD_LIBRARY_PATH
	g++ pythiaLHERunner.cxx `pythia8-config --cflags` -I/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/hepmc3/3.3.0-c2oek4/include -L/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/hepmc3/3.3.0-c2oek4/lib -l HepMC3 `pythia8-config --libs` -o pythiaLHERunner
	```

	Run it similar to approach 1:

	```
	./pythiaLHERunner -f p8_ee_Hgamma_ecm240.cmd -l /afs/cern.ch/work/s/saaumill/public/tmp_madgraph_output/ee_Hgamma/Events/run_0/unweighted_events.lhe -o /afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/pythia8_higgsgamma.hepmc
	```


2. Apply detector simulation with `ddsim`

	We run CLD (or any detector that might be available in the future) full simulation with [ddsim](https://fcc-ee-detector-full-sim.docs.cern.ch/CLD/) (source latest stable key4hep beforehand like shown above):

	```
	ddsim --inputFiles /afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/pythia8_higgsgamma.hepmc -N 75000 \
	--steeringFile $CLDCONFIG/share/CLDConfig/cld_steer.py \
	--compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v05/CLD_o2_v05.xml \
	--outputFile /afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/ddsim_higgsgamma.root
	```

	As for my example this takes quite long, I have written a [HTCondor](https://batchdocs.web.cern.ch/local/quick.html) submit file in `condor_submit`. 

3. Run reconstruction 

	Then, we need to run the CLD reconstruction. Find a documentation about it [here](https://fcc-ee-detector-full-sim.docs.cern.ch/CLD/). We can run it with: 

	```
	k4run CLDReconstruction.py --inputFiles /afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/ddsim_higgsgamma.root --outputBasename reco_higgsgamma -n 75000 --enableLCFIJet
	```
	
	- the CLDReconstruction.py can be found [here](https://github.com/key4hep/CLDConfig/blob/main/CLDConfig/CLDReconstruction.py). 
	- the `--enableLCFIJet` option is set to perform jet clustering. 
	


**Comments** 

Make sure that
- you use the SAME STACK version in all of the above steps
- you use the correct detector version



# Resources: 
- [MadGraph tutorial](https://twiki.cern.ch/twiki/bin/view/CMSPublic/MadgraphTutorial)
- [DelphesPythia8_EDM4HEP tutorial](https://github.com/HEP-FCC/fcc-tutorials/blob/main/fast-sim-and-analysis/k4simdelphes/doc/starterkit/FccFastSimDelphes/Readme.md)