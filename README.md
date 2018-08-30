# SiStripAna

Requirements:
 * python
 * ROOT

Goals:
 study trends of S/N and charge as function of the pile-up based on calibTrees

Steps:
 * choose a list of runs
 * launch analysis on calibTrees 
   * python launch -r list\_of\_runs
 * merge the output
   * python merge.py
 * produce the final plots
   * python StoN\_finalPlots.py

Remarks:
 * each of the script have several options (check with -h)
 * possibility to run on std_bunch, aag
