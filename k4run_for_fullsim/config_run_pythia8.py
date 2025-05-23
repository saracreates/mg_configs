"""
Pythia8, integrated in the FCCSW framework.

Generates according to a pythia .cmd file and saves them in fcc edm format.

"""

import os
from GaudiKernel import SystemOfUnits as units
from Gaudi.Configuration import *

from Configurables import ApplicationMgr
ApplicationMgr().EvtSel = 'NONE' 
ApplicationMgr().EvtMax = 100000
ApplicationMgr().OutputLevel = INFO
ApplicationMgr().ExtSvc +=["RndmGenSvc"]

#### Data service
from Configurables import k4DataSvc
podioevent = k4DataSvc("EventDataSvc")
ApplicationMgr().ExtSvc += [podioevent]

from Configurables import PythiaInterface
pythia8gentool = PythiaInterface()
### Example of pythia configuration file to generate events
# take from $K4GEN if defined, locally if not
# path_to_pythiafile = os.environ.get("K4GEN", "")
# pythiafilename = "Pythia_standard.cmd"
path_to_pythiafile = "/afs/cern.ch/work/s/saaumill/public/mg_configs/k4run_for_fullsim/"
pythiafilename = "p8_ee_Hgamma_ecm240.cmd"
pythiafile = os.path.join(path_to_pythiafile, pythiafilename)
# Example of pythia configuration file to read LH event file
#pythiafile="options/Pythia_LHEinput.cmd"
pythia8gentool.pythiacard = pythiafile
pythia8gentool.doEvtGenDecays = False
pythia8gentool.printPythiaStatistics = True
pythia8gentool.pythiaExtraSettings = [""]

from Configurables import GenAlg
pythia8gen = GenAlg("Pythia8")
pythia8gen.SignalProvider = pythia8gentool
pythia8gen.hepmc.Path = "hepmc"
ApplicationMgr().TopAlg += [pythia8gen]

### Reads an HepMC::GenEvent from the data service and writes a collection of EDM Particles
from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter()
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.hepmcStatusList = [] # convert particles with all statuses
hepmc_converter.GenParticles.Path="GenParticles"
ApplicationMgr().TopAlg += [hepmc_converter]

### Filters generated particles
# accept is a list of particle statuses that should be accepted
from Configurables import GenParticleFilter
genfilter = GenParticleFilter("StableParticles")
genfilter.accept = [1]
genfilter.GenParticles.Path = "GenParticles"
genfilter.GenParticlesFiltered.Path = "GenParticlesStable"
ApplicationMgr().TopAlg += [genfilter]

from Configurables import PodioOutput
out = PodioOutput("out", filename="/afs/cern.ch/work/s/saaumill/public/tmp_fullsim_output/pythia8_higgsgamma.root")
out.outputCommands = ["keep *"]
ApplicationMgr().TopAlg += [out]

