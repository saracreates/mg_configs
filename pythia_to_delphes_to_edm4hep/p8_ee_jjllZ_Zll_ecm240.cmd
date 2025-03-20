! 1) Settings used in the main program.

Main:numberOfEvents = 100000         ! number of events to generate
Main:timesAllowErrors = 150          ! how many aborts before run stops (I sometimes get `fastjet::Error:  Requested 2 exclusive jets, but there were only 0 particles in the event`, every 1k events or so)

! 2) Settings related to output in init(), next() and stat().

Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 1           ! print event record n times

! Vertex smearing : (from https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Generator/Pythia8/p8_ee_ZZ_ecm240.cmd#L16C1-L20C42)
! Check official values here: https://github.com/HEP-FCC/FCCeePhysicsPerformance/blob/master/General/README.md#vertex-distribution 
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 9.80e-3   !  9.80 mum
Beams:sigmaVertexY = 25.4E-6   !  25.4 nm
Beams:sigmaVertexZ = 0.64      !  0.64 mm

! 3) Set the input LHE file

Beams:frameType = 4 ! Reads info of beam parameters from LHE file
!Beams:LHEF = examples/Pythia8/events.lhe
Beams:LHEF = /afs/cern.ch/work/s/saaumill/public/tmp_madgraph_output/ee_jjllZ_Zll/Events/run_0/unweighted_events.lhe  ! LHE file for ee_llZZ events

! Allow the Z decay ONLY into e, mu, tau

! 23:onMode = off
! 23:onIfAny = 11 -11 13 -13 -15 15