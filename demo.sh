#!/bin/bash


source /afs/cern.ch/user/e/echabert/.bashrc
#coredumpsize limit (kbytes)
ulimit -c 0
cd /afs/cern.ch/user/e/echabert/CalibTreeAna/StoN/CMSSW_10_1_0/src
eval `scram runtime -sh`
cd /afs/cern.ch/user/e/echabert/CalibTreeAna/SiStripAna
python StoN_producer.py OPTIONS
