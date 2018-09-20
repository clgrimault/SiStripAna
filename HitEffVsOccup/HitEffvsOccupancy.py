import math
import ROOT
from ROOT import TFile, TCanvas, TLatex, TLegend, TH1F, TH2F, TF1, TGraph, TGraphErrors

###############################################################
# Read occupancy results
###############################################################

occup_dict = {}
#ListOfRuns = [322317,322319,322322,322324]
#ListOfRuns = [322317,322319,322322]
#ListOfRuns = [322480,322485,322487,322492]
#ListOfRuns = [322317,322319,322322,322480,322492]
#ListOfRuns = [322599,322602,322603,322605,322616,322617]
ListOfRuns = [322605,322616,322617]

for RUN in ListOfRuns:
  ifile = TFile("OccupancyPlotsTest_"+str(RUN)+".root","OPEN")
  graph = ifile.Get("occupancyplots/run_"+str(RUN)+"/aveoccu")
  #graph.Draw()

  #Nomenclature
  # 3(TOB)1(LAYER)NB(NB=01 a 12) -> ex: 3108: module 08 - layer 1 - TOB
  nmodules = 12
  
  print "## RUN ", RUN
  occup = []
  for layer in range(5):
    average = 0
    average2 = 0
    for i in range(nmodules):
       bin_id = 3000+(layer+1)*100+(i+1)
       average+=graph.GetBinContent(bin_id)
       average2+=pow(graph.GetBinContent(bin_id),2)
    average/=nmodules
    average2/=nmodules
    error = math.sqrt(average2-pow(average,2))/nmodules
    print layer+1,average," +/- ", error 
    occup.append((average,error))

  occup_dict[RUN] = occup



###############################################################
# Read hit eff  results
###############################################################


eff_dict = {}
for RUN in ListOfRuns:
   ifile = TFile("/afs/cern.ch/cms/tracker/sistrvalidation/WWW/CalibrationValidation/HitEfficiency/GR18/run_"+str(RUN)+"/withMasking/rootfile/SiStripHitEffHistos_run"+str(RUN)+".root","OPEN")
   graph = ifile.Get("SiStripHitEff/eff_good")
   #canvas.Print()
   #c = TCanvas(canvas)
   #print type(canvas)
   #graph = canvas.GetPrimitive("eff_good")
   #graph = canvas.FindObject("eff_good")
   offset = 4
   eff = []
   for layer in range(5):
	bin_id = offset+layer
	x = ROOT.double(0)
	y = ROOT.double(0)
	#yerr = ROOT.double(0)
	graph.GetPoint(bin_id,x,y)
	yerr = graph.GetErrorY(bin_id)
	print layer+1, x, y
	eff.append((y,yerr))
   eff_dict[RUN] = eff


#iLayer = 1
PlotsLayers = {1:[],2:[],3:[],4:[],5:[]}
for key,value in eff_dict.iteritems():
  #print key, value, occup_dict[key]
  for iLayer in range(len(occup_dict[key])):
    PlotsLayers[iLayer+1].append((occup_dict[key][iLayer],eff_dict[key][iLayer]))

print PlotsLayers

ofile = TFile("eff.root","RECREATE")
c1 = TCanvas("c1")
graphs = []
h = TH1F("h","",10,0,2000)
h.GetXaxis().SetTitle("occupancy")
h.GetYaxis().SetTitle("Hit eff.")
h.GetYaxis().SetRangeUser(0.98,1.)
h.Draw()
leg = TLegend(0.15,0.15,0.35,0.4)
for key, value in PlotsLayers.iteritems():
  graph = TGraphErrors(len(value)) 
  graph.GetXaxis().SetRangeUser(0,2000)
  graph.GetYaxis().SetRangeUser(0.9,1.0)
  graph.SetMarkerStyle(21)
  graph.SetMarkerColor(1+key)
  for i, v in enumerate(value):
    graph.SetPoint(i,v[0][0],v[1][0])
    print key, v[0][0],v[1][0]
  #if key == 1 : graph.Draw("AP")  
  #else: graph.Draw("Psame")
  graph.Draw("Psame")  
  graphs.append(graph)
  leg.AddEntry(graph,"layer "+str(key),"p")
leg.Draw("same")

c1.Print("c1.png")
c1.Print("c1.root")
c1.Write()
ofile.Close()


