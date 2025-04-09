! 1) Settings used in the main program.

Main:numberOfEvents = 100000         ! number of events to generate
Main:timesAllowErrors = 150          ! how many aborts before run stops (Problem: `fastjet::Error:  Requested 2 exclusive jets, but there were only 0 particles in the event`)
! 2) Settings related to output in init(), next() and stat().

Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 1           ! print event record n times

! Turn of vertex smearing here because for full sim it is done in ddsim
Beams:allowVertexSpread = off

! 3) Set the input LHE file

Beams:frameType = 4 ! Reads info of beam parameters from LHE file
Beams:LHEF = /afs/cern.ch/work/s/saaumill/public/tmp_madgraph_output/ee_Hgamma/Events/run_0/unweighted_events.lhe  ! LHE file for ee_llZZ events

! 4) Debug? 

SLHA:minMassSM = 100.00000
