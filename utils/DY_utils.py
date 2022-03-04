import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from array import array
from ROOT import kFALSE
import numpy as np
import math
from math import sqrt
from multiprocessing import Queue, Manager
Define_Hists ='''
#include "TH2D.h"
#include "TFile.h"
TFile *f_l1pteta_{0} = TFile::Open("/afs/cern.ch/user/m/melu/public/output.root");
TH2D * h_l1pteta_{0} = (TH2D*) f_l1pteta_{0}->Get("EleIDDataEff");
//TFile *f_l2pteta_{0} = TFile::Open("/afs/cern.ch/user/m/melu/public/output.root");
//TH2D * h_l2pteta_{0} = (TH2D*) f_l1pteta_{0}->Get("EleIDDataEff");
'''




class MyDataFrame(object):
    def __init__(self,settings:dict) -> None:
        '''
        self._channel -> DoubleElectron, DoubleMuon, or ElectronMuon    
        self._Trigger_Condition -> DiLeptons HLT conditions
        self._weight -> Scale Factors for Dileptons
        self._Data(bool) -> Input File(s) is(are) Data/MC
        self._filters -> Offline triggers for Dileptons
        self._File_Paths -> Paths for input Files
        '''
        self._channel = settings.get('channel')
        if self._channel == 'DoubleElectron':
            DY_region = 3 
        elif self._channel == 'DoubleMuon':
            DY_region = 1
        elif self._channel == 'ElectronMuon':
            DY_region = 2 
        else:
            raise ValueError(f'No such channel{self.__channel}')
        
        self._filters = 'DY_region=={0} && DY_z_mass > 60 && DY_z_mass<120 && (DY_l1_pt>30 || DY_l2_pt>30) && DY_drll>0.3'.format(DY_region)    
        self._Data = bool()
        self._df_tree = ROOT.RDataFrame
        self._Hists = Manager().dict()
        
        self._Trigger_Condition = settings.get('Trigger_Condition')
        self._weights = settings.get('weight')
        self._Data = settings.get('Data')
        File_Paths = settings.get('File_Paths')
        

        self._File_Paths = ROOT.std.vector('string')()
        if type(File_Paths) is list :
            for path in File_Paths:
                self._File_Paths.push_back(path)
        else:
            self._File_Paths.push_back(File_Paths)
    @property
    def Tree(self) ->ROOT.RDataFrame.Filter:
        return self._df_tree
    @property
    def Data(self) ->bool:
        return self._Data
    @property
    def channel(self)->str:
        return self._channel
    @channel.setter
    def channel(self,channel:str)->str:
        self._channel = channel
    @property
    def Trigger_Condition(self)->str:
        return self._Trigger_Condition
    @property
    def lepton_weights(self) -> dict:
        return self._weights
    @property
    def File_Paths(self) ->ROOT.std.vector('string')():
        return self._File_Paths
    @property
    def offline_trig(self) -> str:
        return self._filters 
    @Tree.setter
    def Tree(self, Tree:ROOT.RDataFrame.Filter):
        self._df_tree = Tree

    @property
    def Hists(self) ->dict():
        return self._Hists

    @Hists.setter
    def Hists(self, Hists:dict):
        self._Hists =Hists

def Filtering(df:ROOT.RDataFrame,HistsSettings:dict):
    
    Tree= ROOT.RDataFrame('Events',df.File_Paths)
    if not df.Data:
        Tree = Tree.Define('trigger_SF','trigger_sf(h_l1pteta_{0},h_l1pteta_{0},DY_l1_pt,DY_l2_pt,DY_l1_eta,DY_l2_eta)'.format(df.channel))
        lepton_weight = '*'.join([ w + '[DY_l1_id]' for w in df.lepton_weights['l1'] ] +[w + '[DY_l2_id]' for w in df.lepton_weights['l2']])
        Tree = Tree.Define('genweight',f'puWeight*PrefireWeight*{lepton_weight}*trigger_SF*genWeight/abs(genWeight)')

    Tree = Tree.Filter(df.offline_trig)
    df.Tree = Trigger(Tree,df.Trigger_Condition)

    Hists =dict()
    for name in HistsSettings.keys():
        setting = HistsSettings[name]
        if df.Data is not None:
            if df.Data :
                Hists[name] = df.Tree.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'])
            else:
                Hists[name] = df.Tree.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'],'genweight')
        else:
            raise ValueError
    df.Hists = Hists

def overunder_flowbin(h=None):
    h.SetBinContent(1,h.GetBinContent(0)+h.GetBinContent(1))
    h.SetBinError(1,sqrt(h.GetBinError(0)*h.GetBinError(0)+h.GetBinError(1)*h.GetBinError(1)))
    h.SetBinContent(h.GetNbinsX(),h.GetBinContent(h.GetNbinsX())+h.GetBinContent(h.GetNbinsX()+1))
    h.SetBinError(h.GetNbinsX(),sqrt(h.GetBinError(h.GetNbinsX())*h.GetBinError(h.GetNbinsX())+h.GetBinError(h.GetNbinsX()+1)*h.GetBinError(h.GetNbinsX()+1)))
    return h


def set_axis(histo,coordinate:str,title:str,is_energy:bool):

    if coordinate == 'x':
        axis = histo.GetXaxis()
        axis.SetLabelSize(0.0)
        axis.SetTitleOffset(1.15)
        axis.SetTitleSize(0.0)
    elif coordinate  == 'y':
        axis = histo.GetYaxis()
        axis.SetLabelSize(0.03)
        axis.SetTitleSize(0.04)
        axis.SetTitleOffset(1.2)

    else:
        raise ValueError('Only x and y axis is valid')
    axis.SetLabelFont(42)
    axis.SetLabelOffset(0.015)
    axis.SetNdivisions(505)
    axis.SetTitleFont(42)
    
    if is_energy:
        axis.SetTitle(title + ' [GeV]')
    else:
        axis.SetTitle(title)

from collections import OrderedDict
def Plot(Histo:OrderedDict, x_name:str, lumi=int,save_dir='/eos/user/z/zhenggan/ttcbar/DrellYan',channel='DoubleElectron'):

    Histo['MC']['DY'].SetFillColor(ROOT.kRed)
    Histo['MC']['WJets'].SetFillColor(ROOT.kBlue - 7)
    Histo['MC']['VV'].SetFillColor(ROOT.kCyan - 9)
    Histo['MC']['VVV'].SetFillColor(ROOT.kSpring - 9)
    Histo['MC']['SingleTop'].SetFillColor(ROOT.kGray)
    Histo['MC']['ttXorXX'].SetFillColor(ROOT.kViolet-4)
    Histo['MC']['tzq'].SetFillColor(ROOT.kYellow-4)
    Histo['MC']['TT'].SetFillColor(ROOT.kBlue)

    for MC in Histo['MC'].keys():
        Histo['MC'][MC].Scale(lumi)

    Histo['Data'].SetMarkerStyle(20)
    Histo['Data'].SetMarkerSize(0.85)
    Histo['Data'].SetMarkerColor(1)
    Histo['Data'].SetLineWidth(1)

    Yield =dict()
    Yield['MC'] =dict()
    for MC in Histo['MC'].keys():
        Yield['MC'][MC] = round(Histo['MC'][MC].Integral(),1)
    Yield['MC'] = OrderedDict(sorted(Yield['MC'].items(),key = lambda x: x[1],reverse=True))
    Yield['Data'] = round(Histo['Data'].Integral(),1)

    h_stack = ROOT.THStack()

    for MC in  Yield['MC'].keys():
        h_stack.Add(Histo['MC'][MC])
    
    Nbins = h_stack.GetStack().Last().GetNbinsX()
    
    max_yields = 0
    for i in range(1,Nbins+1):
        max_yields_temp = h_stack.GetStack().Last().GetBinContent(i)
        if max_yields_temp>max_yields:max_yields=max_yields_temp


    max_yields_data = 0

    for i in range(1,Nbins+1):
        max_yields_data_temp = Histo['Data'].GetBinContent(i)
        if max_yields_data_temp>max_yields_data:max_yields_data=max_yields_data_temp

    h_stack.SetMaximum(max(max_yields,max_yields_data)*1.8)


    h_error = h_stack.GetStack().Last()
    h_error.SetBinErrorOption(ROOT.TH1.kPoisson)

    binsize = h_error.GetSize()-2
    x = []
    y = []
    xerror = []
    yerror_u = []
    yerror_d = []

    for i in range(0,binsize):
        x.append(h_error.GetBinCenter(i+1))
        y.append(h_error.GetBinContent(i+1))
        xerror.append(0.5*h_error.GetBinWidth(i+1))
        yerror_u.append(0.5*h_error.GetBinErrorUp(i+1))
        yerror_d.append(0.5*h_error.GetBinErrorLow(i+1))

    gr = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y),np.array(xerror),np.array(xerror), np.array(yerror_d), np.array(yerror_u))

    

    from  utils.CMSTDRStyle import setTDRStyle
    T = setTDRStyle()
    T.cd()
    c= ROOT.TCanvas()
    c.cd()
    pad1 = ROOT.TPad('pad1','',0.00,0.22,0.99,0.99)
    pad2 = ROOT.TPad('pad1','',0.00, 0.00, 0.99, 0.22)
    pad1.SetBottomMargin(0.02);
    pad2.SetTopMargin(0.035);
    pad2.SetBottomMargin(0.45);
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    h_stack.Draw('HIST')
    Histo['Data'].Draw("SAME pe")

    gr.SetFillColor(1)
    gr.SetFillStyle(3005)
    gr.Draw("SAME 2")
    if 'DY_l1_pt' in x_name:set_axis(h_stack,'x', 'pt of leading lepton', True)
    if 'DY_l1_eta' in x_name:set_axis(h_stack,'x', '#eta of leading lepton', False)
    if 'DY_l1_phi' in x_name:set_axis(h_stack,'x', 'phi of leading lepton', False)
    if 'DY_l2_pt' in x_name:set_axis(h_stack,'x', 'pt of subleading lepton', True)
    if 'DY_l2_eta' in x_name:set_axis(h_stack,'x', '#eta of subleading lepton', False)
    if 'DY_l2_phi' in x_name:set_axis(h_stack,'x', 'phi of subleading lepton', False)
    if 'DY_z_mass' in x_name:set_axis(h_stack,'x', 'Z mass', True)
    set_axis(h_stack,'y', 'Event/Bin', False)
    
    import utils.CMSstyle as CMSstyle
    CMSstyle.SetStyle(pad1)

   #legend
    leg1 = ROOT.TLegend(0.66, 0.75, 0.94, 0.88)
    leg2 = ROOT.TLegend(0.44, 0.75, 0.64, 0.88)
    leg3 = ROOT.TLegend(0.17, 0.75, 0.40, 0.88)
    leg1.SetMargin(0.4)
    leg2.SetMargin(0.4)
    leg3.SetMargin(0.4)

    
    leg3.AddEntry(Histo['MC']['DY'],'DY ['+str(Yield['MC']['DY'])+']','f')
    leg3.AddEntry(gr,'Stat. unc','f')
    leg3.AddEntry(Histo['Data'],'DY ['+str(Yield['Data'])+']','pe')

    leg2.AddEntry(Histo['MC']['TT'],'TT ['+str(Yield['MC']['TT'])+']','f')
    leg2.AddEntry(Histo['MC']['WJets'],'WJets ['+str(Yield['MC']['WJets'])+']','f')
    leg2.AddEntry(Histo['MC']['VV'],'VV ['+str(Yield['MC']['VV'])+']','f')

    leg1.AddEntry(Histo['MC']['VVV'],'VVV ['+str(Yield['MC']['VVV'])+']','f')
    leg1.AddEntry(Histo['MC']['SingleTop'],'SingleTop ['+str(Yield['MC']['SingleTop'])+']','f')
    leg1.AddEntry(Histo['MC']['ttXorXX'],'ttXorXX ['+str(Yield['MC']['ttXorXX'])+']','f')
    leg1.AddEntry(Histo['MC']['tzq'],'tzq ['+str(Yield['MC']['tzq'])+']','f')

    leg1.SetFillColor(ROOT.kWhite)
    leg1.Draw('same')
    leg2.SetFillColor(ROOT.kWhite)
    leg2.Draw('same')
    leg3.SetFillColor(ROOT.kWhite)
    leg3.Draw('same')

    pad2.cd()

    hMC = h_stack.GetStack().Last()
    hData =Histo['Data'].Clone()
    hData.Divide(hMC)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.85)
    hData.SetMarkerColor(1)
    hData.SetLineWidth(1)

    hData.GetYaxis().SetTitle("Data/MC")
    hData.GetXaxis().SetTitle(h_stack.GetXaxis().GetTitle())
    hData.GetYaxis().CenterTitle()
    hData.SetMaximum(1.5)
    hData.SetMinimum(0.5)
    hData.GetYaxis().SetNdivisions(4,kFALSE)
    hData.GetYaxis().SetTitleOffset(0.3)
    hData.GetYaxis().SetTitleSize(0.14)
    hData.GetYaxis().SetLabelSize(0.1)
    hData.GetXaxis().SetTitleSize(0.14)
    hData.GetXaxis().SetLabelSize(0.1)
    hData.Draw()

    c.Update()
    c.SaveAs(os.path.join(save_dir,channel+x_name+'.pdf'))
    c.SaveAs(os.path.join(save_dir,channel+x_name+'.png'))
    c.Close()
    #pad1.Close()
    #pad2.Close()

    del T
    del c
    del hData
    del hMC
