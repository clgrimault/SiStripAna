import subprocess 
import os
import sys
from optparse import OptionParser


eos_dir = "/eos/cms/store/group/dpg_tracker_strip/comm_tracker/Strip/Calibration/calibrationtree/GR18" 


#current dir
cwd = os.getcwd()

##################################################
# Parse options
##################################################

def_workdir = "/afs/cern.ch/work/e/echabert/private/SiStrip/StoN"
def_pbs_queue = "1nh"
def_tree="both"
def_runnumber = "321305"
def_script = "demo.sh"

#define the binnings
def_nBinsX = 20
#def_minX = 9000
def_minX = 0
def_maxX = 20000

def_nBinsY = 1000
def_minY = 0
def_maxY = 1000
parser = OptionParser()

#define the options
parser.add_option("-d","--workdir", dest="workdir", help="working directory path where output of jobs will be stored", default=def_workdir)
parser.add_option("-q","--queue", dest="queue", help="pbs queue", default=def_pbs_queue)
parser.add_option("-t","--tree", dest="tree", help="choose input tree(s) - 3 options:\n std_bunch, aag, both", default=def_tree)
parser.add_option("-r","--runs", dest="runs", help="list of run numbers - has to be written in quotes or separated with comma without space ", default=def_runnumber)
parser.add_option("-s","--script", dest="script", help="demo script file - template of job launch", default=def_script)
parser.add_option("--nBinsX", dest="nBinsX", help="number of bins - X axis", default=def_nBinsX)
parser.add_option("--nBinsY", dest="nBinsY", help="number of bins - Y axis", default=def_nBinsY)
parser.add_option("--minX", dest="minX", help="range of X axis: min", default=def_minX)
parser.add_option("--maxX", dest="maxX", help="range of X axis: max", default=def_maxX)
parser.add_option("--minY", dest="minY", help="range of Y axis: min", default=def_minY)
parser.add_option("--maxY", dest="maxY", help="range of Y axis: max", default=def_maxY)
parser.add_option("--maxEvents", dest="maxEvents", help="debug mode - enter max events (default = -1)", default=-1)
(options, args) = parser.parse_args()







##################################################
# Create directories
##################################################

launchdir = options.workdir+str("/launch")
if not os.path.exists(launchdir):
  os.makedirs(launchdir)
if not os.path.exists(options.workdir+str("/tmp")):
  os.makedirs(options.workdir+str("/tmp"))
if not os.path.exists(options.workdir+str("/tmp/std_bunch")):
  os.makedirs(options.workdir+str("/tmp/std_bunch"))
if not os.path.exists(options.workdir+str("/tmp/aag")):
  os.makedirs(options.workdir+str("/tmp/aag"))

#f = open("demo.sh")
f = open(options.script)
content = f.read()	

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
   fulllist = subprocess.check_output(['ls',eos_dir])
 if tree == "aag":
   fulllist = subprocess.check_output(['ls',eos_dir+"_Aag"])
 runs = [el for el in options.runs.replace(',',' ').split(' ') if el !=str() ]
 calibTreeList = []
 for run in runs:
	print "RUN = ", run
	cList = [ i  for i in fulllist.split('\n') if i.find(str(run))>0]
	print cList
	calibTreeList.extend(cList)

 for file in calibTreeList:
   #modify content
   ocontent = content
   theOptions = " --file "+file+str(" -d ")+options.workdir
   theOptions+=" -t "+tree
   theOptions+=" --maxEvents \""+str(options.maxEvents)+"\""
   theOptions+=" --nBinsX "+str(options.nBinsX)
   theOptions+=" --nBinsY "+str(options.nBinsY)
   theOptions+=" --minX "+str(options.minX)
   theOptions+=" --minY "+str(options.minY)
   theOptions+=" --maxX "+str(options.maxX)
   theOptions+=" --maxY "+str(options.maxY)
   ocontent = ocontent.replace("OPTIONS",theOptions)

   #create file job
   filename = launchdir+"/job_"+file+"_"+tree+"_.sh"
   ofile = open(filename,"w")
   ofile.write(ocontent)
   ofile.close()

   
   #go to the launch directory
   os.chdir(launchdir)
   #launch the job
   #command = ["bsub","-q","8nm",filename]
   mailoption = "-o /dev/null -e /dev/null"
   command = ["bsub","-q",options.queue,mailoption,filename]
   print command
   #subprocess.call(command)
   p = subprocess.Popen(["chmod","+x",filename], stdout=subprocess.PIPE)
   p = subprocess.Popen(command, stdout=subprocess.PIPE)
   print p.communicate()

   #go back
   os.chdir(cwd)
