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

	We need an option file for `k4run`, see `./k4run_for_fullim/config_run_pythia8.py`. I have adapted this from this [example config](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/options/pythia.py). I adapted the path of the pythia config to point to a pythia config similar to the fast sim one but that we removed the vertex infomation. Additionally, we need to *turn off vertex smearing* in the `config_run_pythia8.py` too because it is done in `ddsim` now. 

2. Apply detector simulation with `ddsim`
3. Run reconstruction 


# Resources: 
- [MadGraph tutorial](https://twiki.cern.ch/twiki/bin/view/CMSPublic/MadgraphTutorial)
- [DelphesPythia8_EDM4HEP tutorial](https://github.com/HEP-FCC/fcc-tutorials/blob/main/fast-sim-and-analysis/k4simdelphes/doc/starterkit/FccFastSimDelphes/Readme.md)