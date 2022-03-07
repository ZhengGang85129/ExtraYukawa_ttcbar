import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
from ROOT import TFile, TH1F, TH2D, TCanvas, TLegend, TPad, TEfficiency
import Utils.CMSTDRStyle as CMSTDRStyle
import Utils.CMSstyle as CMSstyle
File = '/eos/user/z/zhenggan/ExtraYukawa/TriggerSF/year2017/DoubleElectron/files/EfficiencyForMC.root'

f = ROOT.TFile.Open(File)
TS = CMSTDRStyle.setTDRStyle()
TS.cd()
h = f.Get('l2pteta_highjet')

nx = h.GetXaxis().GetNbins()
ny = h.GetYaxis().GetNbins()
xmax = h.GetXaxis().GetXmax()
ymax = h.GetYaxis().GetXmax()
xmin = h.GetXaxis().GetXmin()
ymin = h.GetYaxis().GetXmin()

xtitle = h.GetXaxis().GetTitle()
ytitle = h.GetXaxis().GetTitle()
new_h = TH2D("new_l2pteta_highjet","",nx,xmin,xmax,ny,ymin,ymax)
new_h.GetXaxis().SetTitle(xtitle)
new_h.GetYaxis().SetTitle(ytitle)
arr = [20,40,50,65,80,100,200]

c = ROOT.TCanvas()
c.cd()
#ROOT.gStyle.SetPalette(1)
pad = TPad()
pad.Draw()
pad.cd()
for i in range(1,nx+1):
    for j in range(1,ny+1):
        BinContent= h.GetBinContent(i,j)
        BinError = h.GetBinError(i,j)
        new_h.SetBinContent(i,j,BinContent)
        new_h.SetBinError(i,j,BinError)
        tick = int(arr[i-1])
new_h.Draw('COLZ TEXT E')


new_h.GetXaxis().SetLabelOffset(999)
label = ROOT.TText()
label.SetTextFont(42)
label.SetTextSize(0.04)
label.SetTextAlign(22)
ylabel = new_h.GetYaxis().GetBinLowEdge(1) - 0.15*new_h.GetYaxis().GetBinWidth(1)
new_h.SetEntries(h.GetEntries())

for i in range(nx+1):
    xlow = h.GetXaxis().GetBinUpEdge(i)
    xnew = new_h.GetXaxis().GetBinLowEdge(i+1)
    label.DrawText(xnew,ylabel,f"{int(xlow)}")


CMSstyle.SetStyle(pad)
c.SetGridx(False)
c.SetGridy(False)
c.Update()
c.SaveAs('/eos/user/z/zhenggan/test.png')
c.Close()


