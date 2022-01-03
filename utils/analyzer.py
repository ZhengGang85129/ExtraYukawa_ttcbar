import os 
import ROOT
from ROOT import TFile, TTree, TLorentzVector,TH1F,TEfficiency,TH2D
CURRENT_WORKDIR = os.getcwd()
from itertools import product
import utils.command_string as cmd_str
import math
from array import array
from math import sqrt

class analyzer():
    def __init__(self,infilename,outfilename,channel='ee'):
        self.infilename = infilename
        self.infilebasename = os.path.basename(infilename).split('root')[0]
        self.infile = TFile.Open(infilename)
        self.tree =  self.infile.Get('Events')
        self.entries = self.tree.GetEntries()
        print('Input File: {0}, total events: {1}, Channel: {2}'.format(self.infilename,self.entries,channel))
        self.outfile = TFile.Open(outfilename,"RECREATE")
        print('File: {0} created.'.format(outfilename))
        self.l1ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        self.l2ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        self.lepetabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
        self.jetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
        self.metbin=array('d',[100,110,120,130,140,160,180,200,250])
        self.tdlepetabin=array('d',[0,0.4,0.9,1.5,2.5])
        self.tdl1ptbin=array('d',[20,40,50,65,80,100,200])
        self.tdl2ptbin=array('d',[20,40,50,65,80,100,200])
        self.l1p4 = TLorentzVector()
        self.l2p4 = TLorentzVector()
        #Initialize Histograms
        self.build_1Dhistogram_for_lep()
        self.build_1Dhistogram_for_njet()
        self.build_1Dhistogram_for_met()
        #self.build_1Dhistogram_for_pu()
        self.build_2Dhistogram_for_lep()
        self.build_2Dhistogram_for_2lep()
        try:
            if channel == 'ee' or channel == 'mm':
                self.DY_l1_pt = 'DY_l1_pt'
                self.DY_l1_eta = 'DY_l1_eta'
                self.DY_l1_phi = 'DY_l1_phi'
                self.DY_l1_mass = 'DY_l1_mass'
                
                self.DY_l2_pt = 'DY_l2_pt'
                self.DY_l2_eta = 'DY_l2_eta'
                self.DY_l2_phi = 'DY_l2_phi'
                self.DY_l2_mass = 'DY_l2_mass'
                if channel =='ee':
                    self.region = 3
                    weight = 'self.tree.Electron_RECO_SF[{0}]*self.tree.Electron_RECO_SF[{1}]*self.tree.Electron_CutBased_TightID_SF[{0}]*self.tree.Electron_CutBased_TightID_SF[{1}]'
                    self.HLT_path1 = 'self.tree.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or self.tree.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or self.tree.HLT_passEle32WPTight or self.tree.HLT_Ele35_WPTight_Gsf'
                else:
                    self.region = 1
                    weight ='self.tree.Muon_CutBased_TightID_SF[{0}]*self.tree.Muon_CutBased_TightID_SF[{1}]*self.tree.Muon_TightRelIso_TightIDandIPCut_SF[{0}]*self.tree.Muon_TightRelIso_TightIDandIPCut_SF[{1}]'
                    self.HLT_path1 = 'self.tree.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 or self.tree.HLT_IsoMu27'
            
            elif channel == 'em':
                self.DY_l1_pt = 'Muon_corrected_pt[self.tree.DY_l1_id]'
                self.DY_l1_eta = 'Muon_eta[self.tree.DY_l1_id]'
                self.DY_l1_phi = 'Muon_phi[self.tree.DY_l1_id]'
                self.DY_l1_mass = 'Muon_mass[self.tree.DY_l1_id]'
               
                self.DY_l2_pt = 'Electron_pt[self.tree.DY_l2_id]'
                self.DY_l2_eta = 'Electron_eta[self.tree.DY_l2_id]'
                self.DY_l2_phi = 'Electron_phi[self.tree.DY_l2_id]'
                self.DY_l2_mass = 'Electron_mass[self.tree.DY_l2_id]'
                self.region = 2
                weight = 'self.tree.Muon_CutBased_TightID_SF[{0}]*self.tree.Muon_TightRelIso_TightIDandIPCut_SF[{0}]*self.tree.Electron_RECO_SF[{1}]*self.tree.Electron_CutBased_TightID_SF[{1}]'
                self.HLT_path1 = 'self.tree.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or self.tree.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or self.tree.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or self.tree.HLT_IsoMu27 or self.tree.HLT_passEle32WPTight or self.tree.HLT_Ele35_WPTight_Gsf'
            else:
                raise ValueError
        except ValueError as exc:
            raise RuntimeError('No such channel :{}'.format(channel))
        
        self.ttc_l1_pt = 'ttc_l1_pt'
        self.ttc_l1_eta = 'ttc_l1_eta'
        self.ttc_l1_phi = 'ttc_l1_phi'
        self.ttc_l1_mass = 'ttc_l1_mass'
    
        self.ttc_l2_pt = 'ttc_l2_pt'
        self.ttc_l2_eta = 'ttc_l2_eta'
        self.ttc_l2_phi = 'ttc_l2_phi'
        self.ttc_l2_mass = 'ttc_l2_mass'
        
        self.HLT_path2 = 'self.tree.HLT_PFMET120_PFMHT120_IDTight or self.tree.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight or self.tree.HLT_PFHT500_PFMET100_PFMHT100_IDTight or self.tree.HLT_PFHT700_PFMET85_PFMHT85_IDTight or self.tree.HLT_PFHT800_PFMET75_PFMHT75_IDTight'
        self.DYweight = weight.format('self.tree.DY_l1_id','self.tree.DY_l2_id') 
        self.TTCweight = weight.format('self.tree.ttc_l1_id','self.tree.ttc_l2_id') 

    def build_1Dhistogram_for_lep(self,deactivate=False,command=cmd_str.h1_lepcommand):
        states = ['pre_','']
        lep_orders = ['l1','l2']
        observables =['eta','pt']
        conditions =['','_low','_high']
        objects = ['','jet','pv','MET']
        for state,order,observable,condition,obj in product(states,lep_orders,observables,conditions,objects):
            if obj == '' and condition != ''  :
                continue
            if condition =='' and obj != '':
                continue
        
            if not deactivate:
                x_title = ''
                if order == 'l1':
                    x_title +='Leading Lepton'
                else:
                    x_title +='Subleading Lepton'
                
                if observable =='pt':
                    x_title += ' P_{T} GeV'
                else:
                    x_title += ' #eta'
                Bin = order+observable+'bin'
                if observable == 'eta':
                    Bin = 'lepetabin'
                c =command.format(state,order,observable,condition,obj,Bin,1,Bin,x_title)
            else:
                c = command.format(state,order,observable,condition,obj)
            exec(c)
    def build_1Dhistogram_for_njet(self,deactivate=False,command=cmd_str.h1_njetcommand):
        xtitle = 'N_{jets}'
        states = ['','pre_']
        conditions = ['','_low','_high']
        objects = ['','pv','MET']
        xtitle = 'N_{jets}'
        for state,condition,obj in product(states,conditions,objects):
            if condition == '' and obj != '' : continue
            if condition != '' and obj == '': continue
            if not deactivate:
                c =command.format(state,condition,obj,xtitle)
            else:
                c =command.format(state,condition,obj)
            exec(c)
    def build_1Dhistogram_for_met(self ,deactivate=False,command=cmd_str.h1_metcommand):
        states = ['','pre_']
        conditions = ['','_low','_high']
        objects = ['','pv','jet']
        xtitle = 'MET [GeV]'
        for state,condition,obj in product(states,conditions,objects):
            if condition == '' and obj != '' : continue
            elif condition != '' and obj == '': continue
            if not deactivate:
                c =command.format(state,condition,obj,xtitle)
            else:
                c =command.format(state,condition,obj)
            exec(c)
    def build_1Dhistogram_for_pu(self,deactivate=False,command=cmd_str.h1_pucommand):
        states = ['','pre_']
        conditions = ['','true']
        for state,condition in product(states,conditions):
            if not deactivate:
                c =command.format(state,condition)
            else:
                c =command.format(state,condition)
            exec(c)
    def build_2Dhistogram_for_lep(self,deactivate=False,command=cmd_str.h2_lepcommand):
        states = ['','pre_']
        leps = ['l1','l2']
        conditions = ['','_low','_high']
        objects = ['','pv','jet','MET']
        _xtitle = 'Leading Lepton P_{T} [GeV]'
        _ytitle = 'Leading Lepton #||{#eta}'
        for state,lep,condition,obj in product(states,leps,conditions,objects):
            if condition == '' and obj != '' : continue
            elif condition != '' and obj == '': continue
            if not deactivate:
                if lep == 'l2':
                    xtitle = 'Sub'+_xtitle
                    ytitle = 'Sub'+_ytitle
                else:
                    xtitle = _xtitle
                    ytitle = _ytitle

                c =command.format(state,lep,condition,obj,xtitle,ytitle)
            else:
                c =command.format(state,lep,condition,obj)
            exec(c)
    def build_2Dhistogram_for_2lep(self,deactivate = False,command=cmd_str.h2_2lepcommand):
        states = ['','pre_']
        observables = ['pt','eta']
        conditions = ['','_low','_high']
        objects = ['','pv','jet','MET']
        _xtitle = 'Leading Lepton #||'
        _ytitle = 'SubLeading Lepton #||' 
        for state,observable,condition,obj in product(states,observables,conditions,objects):
            if condition == '' and obj != '' : continue
            elif condition != '' and obj == '': continue
            
            if not deactivate:
                if observable == 'pt':
                    xtitle = _xtitle+'P_{T} [GeV]'
                    ytitle = _ytitle+'P_{T} [GeV]'
                    xbin = 'self.tdl1ptbin'
                    ybin = 'self.tdl2ptbin'
                    nxbin = 'len(self.tdl1ptbin)-1'
                    nybin = 'len(self.tdl2ptbin)-1'
                else:
                    xtitle = _xtitle+'{#eta}'
                    ytitle = _ytitle+'{#eta}'
                    xbin = 'self.tdlepetabin'
                    ybin = 'self.tdlepetabin'
                    nxbin = 'len(self.tdlepetabin)-1'
                    nybin = 'len(self.tdlepetabin)-1'

                c =command.format(state,observable,condition,obj,nxbin,xbin,nybin,ybin,xtitle,ytitle)
            else:
                c =command.format(state,observable,condition,obj)
            exec(c)
        
    def selection(self):
        
        exec(cmd_str.fill_histocommand.format(self.region,self.DY_l1_pt,self.DY_l1_eta,self.DY_l1_phi,self.DY_l1_mass,self.DY_l2_pt,self.DY_l2_eta,self.DY_l2_phi,self.DY_l2_mass,self.DYweight,self.ttc_l1_pt,self.ttc_l1_eta,self.ttc_l1_phi,self.ttc_l1_mass,self.ttc_l2_pt,self.ttc_l2_eta,self.ttc_l2_phi,self.ttc_l2_mass,self.TTCweight,self.HLT_path1,self.HLT_path2))

