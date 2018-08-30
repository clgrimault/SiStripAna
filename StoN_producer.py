import ROOT
from ROOT import TFile, TCanvas, TLatex, TLegend, TH1F, TH2F
#ROOT.gROOT.Reset()
#ROOT.gROOT.SetBatch()
#ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
#ROOT.TGaxis.SetMaxDigits(3)

import sys
import os
from optparse import OptionParser

eosdirname = "root://eoscms//eos/cms/store/group/dpg_tracker_strip/comm_tracker/Strip/Calibration/calibrationtree/GR18"

##################################################
# Parse options
##################################################

def_workdir = "/afs/cern.ch/work/e/echabert/private/SiStrip/StoN"
def_tree="std_bunch"
def_runnumber = "calibTree_321305_50.root"

#define the binnings
def_nBinsX = 20
def_minX = 0
def_maxX = 20000

def_nBinsY = 1000
def_minY = 0
def_maxY = 1000

nBinsBx = 3000
minBx = 0
maxBx = 3000

parser = OptionParser()
#define the options
parser.add_option("-d","--workdir", dest="workdir", help="working directory path where output of jobs will be stored", default=def_workdir)
parser.add_option("-t","--tree", dest="tree", help="choose input tree(s) - 3 options:\n std_bunch, aag", default=def_tree)
parser.add_option("-f","--file", dest="filename", help="input file name", default=def_runnumber)
parser.add_option("--nBinsX", dest="nBinsX", help="number of bins - X axis", default=def_nBinsX)
parser.add_option("--nBinsY", dest="nBinsY", help="number of bins - Y axis", default=def_nBinsY)
parser.add_option("--minX", dest="minX", help="range of X axis: min", default=def_minX)
parser.add_option("--maxX", dest="maxX", help="range of X axis: max", default=def_maxX)
parser.add_option("--minY", dest="minY", help="range of Y axis: min", default=def_minY)
parser.add_option("--maxY", dest="maxY", help="range of Y axis: max", default=def_maxY)
parser.add_option("--maxEvents", dest="maxEvents", help="debug mode - enter max events (default = -1)", default=-1)
(options, args) = parser.parse_args()


##################################################
# Read file
##################################################

filename = eosdirname
treename = ""
if options.tree == "std_bunch":
	treename = "gainCalibrationTreeStdBunch/tree"
	filename+="/"+str(options.filename)
if options.tree == "aag":
	treename = "gainCalibrationTreeAagBunch/tree"
	filename+="_Aag/"+str(options.filename)
if treename == "":
	print "Tree name not properly defined. Should be std_bunch or aag"
	sys.exit(-1)

instLumi = 0
print "open file",filename
print " > access to tree", treename
f = TFile(filename, "READ")
#retrieve the tree
tree = f.Get(treename)
print " > #events =",tree.GetEntriesFast()

#list of layers
layers = {(3,1):"TIB_L1",(3,2):"TIB_L2",(3,3):"TIB_L3",(3,4):"TIB_L4",(5,1):"TOB_L1",(5,2):"TOB_L2",(5,3):"TOB_L3",(5,4):"TOB_L4",(5,5):"TOB_L5",(5,6):"TOB_L6",(4,1):"TID_W1",(4,2):"TID_W2",(4,3):"TID_W3",(6,1):"TEC_W1",(6,2):"TEC_W2",(6,3):"TEC_W3",(6,4):"TEC_W4",(6,5):"TEC_W5",(6,6):"TEC_W6",(6,7):"TEC_W7",(6,8):"TEC_W8",(6,9):"TEC_W9"}



##################################################
# Define the plots
##################################################


#define the binnings
nBinsNormQ = int(options.nBinsY)
minNormQ = float(options.minY)
maxNormQ = float(options.maxY)

nBinsLumi = int(options.nBinsX)
minLumi = float(options.minX)
maxLumi = float(options.maxX)
instLumiBins = [(minLumi+(maxLumi-minLumi)/nBinsLumi)*i for i in range(nBinsLumi)]

#create the 2D plots
plot2DNormQ = {key:TH2F("NormChargeVsLumi_"+val,"",nBinsLumi,minLumi,maxLumi,nBinsNormQ,minNormQ,maxNormQ) for key, val in layers.iteritems() }
plot2DNormQBx = {key:TH2F("NormChargeVsBx_"+val,"",nBinsBx,minBx,maxBx,nBinsNormQ,minNormQ,maxNormQ) for key, val in layers.iteritems() }

pInstLumi = TH1F("pInstLumi","",100,0,5000)
#lQplot = [TH1F("lQplot_"+str(i),"",100,0,1000) for i in range(nBinsLumi)]


##################################################
# Run over the tree
##################################################


count = 0
maxEvents = int(options.maxEvents)
if maxEvents == -1:
  maxEvents = tree.GetEntries()+1

for entry in tree:
  #print entry.instLumi
  pInstLumi.Fill(entry.instLumi)

  lumiBin = int((entry.instLumi-minLumi)/(maxLumi-minLumi)*nBinsLumi)

  count+=1 
  if count == maxEvents:
     break
  
  for charge, path, rawid in zip(entry.GainCalibrationcharge, entry.GainCalibrationpath, entry.GainCalibrationrawid):
    partition = (rawid>>25)&0x7   #          //TIB=3, TID=4, TOB=5, TEC=6
    layer = (rawid>>14)&0x7       # only true for barrel
    if partition == 6: # for TEC
      layer = (rawid>>14)&0xF
    if partition == 4: # for TID
      layer = (rawid>>11)&0x3

    if partition>2 and partition<7:
    	plot2DNormQ[(int(partition),int(layer))].Fill(entry.instLumi,charge/path)
    	plot2DNormQBx[(int(partition),int(layer))].Fill(entry.bx,charge/path)


##################################################
# Write output
##################################################



ofile = TFile(options.workdir+"/tmp/"+options.tree+"/StoN_"+options.filename,"RECREATE")
ofile.cd()
pInstLumi.Write()
#for plot in lQplot:
#  plot.Write()


for key, val in plot2DNormQ.iteritems():
  val.Write()
for key, val in plot2DNormQBx.iteritems():
  val.Write()
ofile.Close()
