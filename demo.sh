#!/bin/bash


source /afs/cern.ch/user/e/echabert/.bashrc
#coredumpsize limit (kbytes)
ulimit -c 0
cd /afs/cern.ch/user/e/echabert/CalibTreeAna/StoN
cd CMSSW_10_1_0/src
eval `scram runtime -sh`
cd -
python StoN_producer.py OPTIONS
