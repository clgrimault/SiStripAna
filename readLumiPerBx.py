import sys
import csv
from ROOT import TCanvas, TGraph, TFile
from collections import Counter, OrderedDict


if len(sys.argv)<2:
  print "Syntax is:  readLumiPerBx.py  runnumber  "
  exit()

run=str(sys.argv[1])


# Input

#remove the first line of the file
#f = open('lumi_run'+run+'.csv','rb')
#lines = f.readlines()
#f.close()
#the_input = '\n'.join( lines[1:] )
#print the_input

fin = csv.DictReader(open('lumi_run'+run+'.csv','rb'))
#fin = csv.DictReader(the_input)


#run:fill,ls,time,beamstatus,E(GeV),delivered(/ub),recorded(/ub),avgpu,source,[bxidx bxdelivered(/ub) bxrecorded(/ub)]

lumiPerBxPerLs = {}

# Count col bx
colBx=[]
for row in fin:
 #print row.keys()
 if 'beamstatus' not in row.keys():
   continue
 #print row['beamstatus']
 if row['beamstatus']=='STABLE BEAMS' and type(row['ls']) == type(str()):
  if ':' in row['ls']:
    LS = row['ls'].split(':')[0]
#  if row['ls']=='100:100':
    fulllist=row['[bxidx bxdelivered(/ub) bxrecorded(/ub)]'].replace('[','').replace(']','').split(' ')
    colBx.append(len(fulllist)/3)
counter = Counter(colBx)
max_count = max(counter.values())
for k,v in counter.items():
  print k, v
mode = [k for k,v in counter.items() if v == max_count]
print 'found '+str(mode[0])+' col. bx'

# Get lumi
fin = csv.DictReader(open('lumi_run'+run+'.csv','rb'))
for row in fin:
 if row['beamstatus']=='STABLE BEAMS' and type(row['ls']) == type(str()):
  if ':' in row['ls']:
    LS = row['ls'].split(':')[0]
#  if row['ls']=='100:100':
    fulllist=row['[bxidx bxdelivered(/ub) bxrecorded(/ub)]'].replace('[','').replace(']','').split(' ')
    lumiPerBx = {}
    for i in range(len(fulllist)/3):
       lumiPerBx[ fulllist[i*3] ] = fulllist[i*3+1]
    #print len(lumiPerBx)
    if len(lumiPerBx) == mode[0] : 
       lumiPerBxPerLs[ LS ] = lumiPerBx


# Compute avg over LS
avg = {}
for key in lumiPerBxPerLs.values()[0].keys():
   avg[int(key)]=0

for ls in lumiPerBxPerLs.keys():
   for key, value in lumiPerBxPerLs[ls].items():
      avg[int(key)]+=float(value)

avg_ordered = OrderedDict(sorted(avg.items()))

print len(avg), ' col. bx'
print len(lumiPerBxPerLs), ' LS'

for key in avg_ordered.keys():
   avg_ordered[key]/=len(lumiPerBxPerLs)

AVG=0
for key, val in avg_ordered.items():
  AVG+=float(val)
  #print 'LS', key, val
AVG/=len(avg_ordered)
print AVG

for key in avg_ordered.keys():
   avg_ordered[key]/=AVG
   print key, avg_ordered[key]


lumi_vs_bx = TGraph()
i=0
for key, value in avg_ordered.items():
   lumi_vs_bx.SetPoint(i, float(key), float(value))
   i+=1

c1 = TCanvas()
lumi_vs_bx.SetMarkerStyle(20)
#lumi_vs_bx.GetXaxis().SetRangeUser(890, 1000)
lumi_vs_bx.GetXaxis().SetRangeUser(0, 3600)
lumi_vs_bx.Draw('AP')
lumi_vs_bx.SetName("lumi_vs_bx")
c1.Print('lumi_vs_bx.png')
ofile = TFile("lumi_vs_bx.root","RECREATE")
lumi_vs_bx.Write()
c1.Write()
ofile.Write()
ofile.Close()
