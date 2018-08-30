import os
import sys
import subprocess 
from optparse import OptionParser


eos_dir = "/eos/cms/store/group/dpg_tracker_strip/comm_tracker/Strip/Calibration/calibrationtree/GR18" 


#current dir
cwd = os.getcwd()

##################################################
# Parse options
##################################################

def_workdir = "/afs/cern.ch/work/e/echabert/private/SiStrip/StoN"
def_tree="both"
def_runnumber = "321305"

parser = OptionParser()

#define the options
parser.add_option("-d","--workdir", dest="workdir", help="working directory path where output of jobs will be stored", default=def_workdir)
parser.add_option("-t","--tree", dest="tree", help="choose input tree(s) - 3 options:\n std_bunch, aag, both", default=def_tree)
parser.add_option("-r","--runs", dest="runs", help="list of run numbers - has to be written in quotes or separated with comma without space ", default=def_runnumber)


(options, args) = parser.parse_args()


##################################################
# Run for aag /std_bunch or both
##################################################

tree_list = []
if options.tree == "both":
  tree_list = ["std_bunch","aag"]
if options.tree == "aag":
  tree_list = ["aag"]
if options.tree == "std_bunch":
  tree_list = ["std_bunch"]

for tree in tree_list: 

 fulllist = ""
 if tree == "std_bunch":
   fulllist = subprocess.check_output(['ls',options.workdir+str("/tmp/std_bunch/")])
 if tree == "aag":
   fulllist = subprocess.check_output(['ls',options.workdir+str("/tmp/aag/")])
 runs = [el for el in options.runs.replace(',',' ').split(' ') if el !=str() ]
 calibTreeList = []
 for run in runs:
	#print "RUN = ", run
	cList = [ i  for i in fulllist.split('\n') if i.find(str(run))>0]
	#print cList
	calibTreeList.extend(cList)

 #### merge the file
 ofile = options.workdir+"/"+tree+"_"+"_".join(runs)+".root"
 idir = options.workdir+"/tmp/"+tree+"/"
 print "Create file ", ofile
 #subprocess.check_output(['hadd','-f',ofile,(" "+idir).join(calibTreeList)])
 #subprocess.call(['hadd','-f',ofile,idir+(" "+idir).join(calibTreeList)],shell=True)
 #p = subprocess.Popen(['hadd','-f',ofile,idir+(" "+idir).join(calibTreeList)],stdout=subprocess.PIPE)
 p = subprocess.Popen(['hadd','-f',ofile]+[idir+f for f in calibTreeList],stdout=subprocess.PIPE)
 #print p.communicate()
