import ROOT
from ROOT import TFile, TCanvas, TLatex, TLegend, TH1F, TH2F, TF1
#ROOT.gROOT.Reset()
#ROOT.gROOT.SetBatch()
#ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TGaxis.SetMaxDigits(3)

import sys
#import collections
from optparse import OptionParser

xtitle = "inst. luminosity [10^{30} cm^{2}.s^{-1}]"

ymin = 375
ymax = 400
ymin_rms = 25
ymax_rms = 45
ymin_mpv = 290
ymax_mpv = 320
ytitle = "mean norm. charge [ADC]"
ytitle_rms = "landau fit: rms"
ytitle_mpv = "landau fit: mpv"
xtitle = "inst. luminosity [10^{30} cm^{2}.s^{-1}]"

##################################################
# Parse options
##################################################

def_workdir = "/afs/cern.ch/work/e/echabert/private/SiStrip/StoN"
def_tree="std_bunch"
def_runnumber = "321305"

parser = OptionParser()

#define the options
parser.add_option("-d","--workdir", dest="workdir", help="working directory path where output of jobs will be stored", default=def_workdir)
parser.add_option("-t","--tree", dest="tree", help="choose input tree(s) - 3 options:\n std_bunch, aag, both", default=def_tree)
parser.add_option("-r","--runs", dest="runs", help="list of run numbers - has to be written in quotes or separated with comma without space ", default=def_runnumber)


(options, args) = parser.parse_args()


runs = [el for el in options.runs.replace(',',' ').split(' ') if el !=str() ]
filename = options.workdir+"/"+options.tree+"_"+"_".join(runs)+".root"


#ifile = TFile("rescalibTree.root","READ");
#ifile = TFile("rescalibTree_AAG.root","READ");
ifile = TFile(filename,"READ");
ofilenamebase = "plots_"+options.tree+"_"+"_".join(runs)

#list of layers
layers = {(3,1):"TIB_L1",(3,2):"TIB_L2",(3,3):"TIB_L3",(3,4):"TIB_L4",(5,1):"TOB_L1",(5,2):"TOB_L2",(5,3):"TOB_L3",(5,4):"TOB_L4",(5,5):"TOB_L5",(5,6):"TOB_L6",(4,1):"TID_W1",(4,2):"TID_W2",(4,3):"TID_W3",(6,1):"TEC_W1",(6,2):"TEC_W2",(6,3):"TEC_W3",(6,4):"TEC_W4",(6,5):"TEC_W5",(6,6):"TEC_W6",(6,7):"TEC_W7",(6,8):"TEC_W8",(6,9):"TEC_W9"}
colors = {"TIB_L1":41,"TIB_L2":41,"TIB_L3":43,"TIB_L4":44,"TOB_L1":71,"TOB_L2":72,"TOB_L3":73,"TOB_L4":74,"TOB_L5":75,"TOB_L6":76,"TID_W1":51,"TID_W2":52,"TID_W3":53,"TEC_W1":91,"TEC_W2":92,"TEC_W3":93,"TEC_W4":94,"TEC_W5":95,"TEC_W6":96,"TEC_W7":97,"TEC_W8":98,"TEC_W9":99}
order = {"TIB_L1":1,"TIB_L2":2,"TIB_L3":3,"TIB_L4":4,"TOB_L1":5,"TOB_L2":6,"TOB_L3":7,"TOB_L4":8,"TOB_L5":9,"TOB_L6":10,"TID_W1":11,"TID_W2":12,"TID_W3":13,"TEC_W1":14,"TEC_W2":15,"TEC_W3":16,"TEC_W4":17,"TEC_W5":18,"TEC_W6":19,"TEC_W7":20,"TEC_W8":21,"TEC_W9":22}
order = { value:key for key, value in order.iteritems()}

plot2DNames = {val: "NormChargeVsLumi_"+val  for key, val in layers.iteritems() }
plot2D = { key: ifile.Get(name) for key, name in plot2DNames.iteritems() }

ofile = TFile(ofilenamebase+".root","RECREATE")
#ofile = TFile("plots_AAG.root","RECREATE")

fitPlot = TH1F("fitPlot","", len(plot2D),0,len(plot2D))

## Superimpose plots

plot_all_layers = plot2D["TIB_L1"]
for key, plot in plot2D.iteritems():
   if key is not "TIB_L1":
     plot_all_layers.Add(plot)

nplots = 4
cSup = TCanvas("cSupShape")
legShape = TLegend(0.6,0.6,0.8,0.85)
for i in range(nplots):
	ibin = int(plot_all_layers.GetNbinsX()*1./(nplots+1)*(i+1))
	p = plot_all_layers.ProjectionY("_py"+str(i),ibin,ibin)
	p.SetLineColor(i+1)
	#print plot_all_layers.GetXaxis().GetBinCenter(ibin)
	legShape.AddEntry(p,"L = "+str(int(plot_all_layers.GetXaxis().GetBinCenter(ibin)))+"e^{30}","l")
	if i == 0 :
		cSup.cd()
		p.Scale(1./p.Integral())
		p.GetXaxis().SetTitle("norm. charge [ADC]")
		p.Draw()
	else:
		cSup.cd()
		p.Scale(1./p.Integral())
		p.Draw("same")
	
legShape.Draw("same")
cSup.Write()
cSup.Print(ofilenamebase+"cSupShape.png")


## Overlay the layers
c = TCanvas("cOverlay")
indice = 1
leg = TLegend(0.13,0.45,0.3,0.87)
#for key, plot in plot2D.iteritems():
#for key, plot in collections.OrderedDict(plot2D.iteritems()):
for key in sorted(plot2D.keys()):
  plot = plot2D[key]
  prof = plot.ProfileX()
  #fitres = prof.Fit("pol1","S")
  #print fitres.Get().GetParams()[1]
  #fitPlot.SetBinContent(indice,fitres.Get().GetParams()[1])
  #fitPlot.SetBinError(indice,fitres.Get().GetErrors()[1])
  #fitPlot.GetXaxis().SetBinLabel(indice,key)
  prof.Write()
  prof.SetLineColor(colors[key])
  if indice == 1:
    prof.GetYaxis().SetRangeUser(ymin,ymax)
    prof.GetXaxis().SetTitle(xtitle)
    prof.GetYaxis().SetTitle(ytitle)
    prof.Draw()
  else:
    prof.Draw("same")
  leg.AddEntry(prof,key)
  indice+=1
leg.Draw("same")
c.Write()
c.Print(ofilenamebase+"+cLayer_NormQvsLumi.png")


## perform the landau fits
cLandau_mpv = TCanvas("landau_mpv")
cLandau_rms = TCanvas("landau_rms")
indice = 1
for key in sorted(plot2D.keys()):
  plot = plot2D[key]
  func = TF1("l","landau",0,1000)
  #plot2D["TIB_L1"].FitSlicesY(func,0,-1,0,"QNR")
  plot.FitSlicesY(func,0,-1,0,"QNR")
  h2_1 = ROOT.gDirectory.Get(plot2D[key].GetName()+"_1")
  h2_2 = ROOT.gDirectory.Get(plot2D[key].GetName()+"_2")
  h2_1.SetLineColor(colors[key])
  h2_2.SetLineColor(colors[key])
  if indice == 1:
    h2_1.GetYaxis().SetRangeUser(ymin_mpv,ymax_mpv)
    h2_1.GetXaxis().SetTitle(xtitle)
    h2_1.GetYaxis().SetTitle(ytitle_mpv)
    cLandau_mpv.cd()
    h2_1.Draw()
    h2_2.GetYaxis().SetRangeUser(ymin_rms,ymax_rms)
    h2_2.GetXaxis().SetTitle(xtitle)
    h2_2.GetYaxis().SetTitle(ytitle_rms)
    cLandau_rms.cd()
    h2_2.Draw()
  else:
    cLandau_mpv.cd()
    h2_1.Draw("same")
    cLandau_rms.cd()
    h2_2.Draw("same")
  indice+=1
cLandau_rms.cd()
leg.Draw("same")
cLandau_rms.Write()
cLandau_rms.Print(ofilenamebase+"+cLayer_Landau_rms.png")
cLandau_mpv.cd()
leg.Draw("same")
cLandau_mpv.Write()
cLandau_mpv.Print(ofilenamebase+"+cLayer_Landau_mpv.png")

#############################

## perform the fits
#indice = 1
for indice in order.keys():
#for key in sorted(plot2D.keys()):
  plot =  plot2D[order[indice]]
  #plot = plot2D[key]
  prof = plot.ProfileX()
  fitres = prof.Fit("pol1","S")
  fitPlot.SetBinContent(indice,fitres.Get().GetParams()[1])
  fitPlot.SetBinError(indice,fitres.Get().GetErrors()[1])
  fitPlot.GetXaxis().SetBinLabel(indice,order[indice])
  #indice+=1
#fitPlot.GetYaxis().SetMaxDigits(3)
fitPlot.GetYaxis().SetTitle("Norm. charge vs lumi slope")
fitPlot.GetYaxis().SetTitleOffset(1.4)
cFit = TCanvas("fitSlope")
cFit.cd()
fitPlot.Draw()
cFit.Print(ofilenamebase+"_fitSlope.png")
cFit.Write()

ofile.Write()
fitPlot.Write()

