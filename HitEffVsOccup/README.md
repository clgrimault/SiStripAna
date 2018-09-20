Instructions to obtain HitEff vs occupancy plots

  * run DPGAnalysis/SiStripTools/test/OccupancyPlotsTest_cfg.py
  * can run on ALCARECO sample
  * requires to remove process.APVPhases sequence from process.seqEventHistoryReco 
  * requires to run the HitEff scripts on the same runs
  * check that the lumi is the same between the ALCARECO files and the hitEff
  * change the list of runs in HitEffvsOccupancy.py [check file names and their existence]
  * python HitEffvsOccupancy.py

