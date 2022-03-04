import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile,TEfficiency
from array import array

from utils.RDataFrame import *
from utils.general_tool import *
from utils.Header import *
import warnings
class TrigRDataFrame(MyDataFrame):
    ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
    etabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
    njetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
    metbin=array('d',[100,110,120,130,140,160,180,200,250])
    abs_etabin=array('d',[0,0.4,0.9,1.5,2.5])
    def __init__(self,settings:dict)->None:
        super().__init__(settings)
        self.__Var_Name = settings.get('Var_Name',None)
        self.__HLT_LEP = settings.get('HLT_LEP',None)
        self.__HLT_MET = settings.get('HLT_MET',None)
        self.__flag = settings.get('Flag',None)
        self.__Year = settings.get('Year',None) 
        self.__LepSF_File = settings.get('LepSF_File',None)
        self.__DirOut = settings.get('DirOut',None)
        self.__Type = settings.get('Type',None)
        self.__Year = settings.get('Year',None)
        self.__channel = settings.get('channel',None)
        self.__channel = settings.get('channel',None)
        self.__FileOutName = self.__DirOut+'/EfficiencyFor'+self.__Type+'.root'
        self.__FileIn = settings.get('FileIn',None)
        self.__FileOut = TFile.Open(self.__FileOutName,"RECREATE")
       
        self.__FileIn_vecstr= ROOT.std.vector('string')()

        for p in self.__FileIn:
            self.__FileIn_vecstr.push_back(p)
        
        if self.__Type == 'Data' :
            self.__isData = 1
        else:
            self.__isData = 0 
        print(self.__FileOutName +' is created.')
        self.__Histogram = dict()
        self.__Histogram['1D'] = dict()
        self.__Histogram['1D']['pt'] = dict()
        self.__Histogram['1D']['eta'] = dict()
        self.__Histogram['1D']['njet'] = dict()
        self.__Histogram['1D']['met'] = dict()
        
        
        self.__Histogram['2D'] = dict()
        self.__Histogram['2D']['pteta'] = dict()
        self.__Histogram['2D']['pt'] = dict()
        self.__Histogram['2D']['eta'] = dict()
        
        self.__Histogram['1D']['HLT'] = dict()
        #print(self.__HLT_LEP)
        print(self.__Var_Name)
        #print(self.__flag)
    @property
    def FileOutName()->str:
        return self.__FileOutName
    def Init_Histogram(self,**args):
        df = args.get('df',None)
        name = args.get('name',None)
        dim = args.get('dim',None)
        tag = args.get('tag',None)
        xtitle = args.get('xtitle',None)
        ytitle = args.get('ytitle',None)
        content = args.get('content',None)
        weight = args.get('weight','weight')
        

        if df == None:
            raise ValueError('Should Specify RDataframe')
        if dim == None:
            raise ValueError('Should Specify Histogram')
        if content == None:
            raise ValueError('Should Specify Filled Value')
        if tag == None:
            raise ValueError('Should Speicify What is the tag of the Histogram.')
        if xtitle == None:
            warnings.warn('Should Speicify xtitle!')
        if ytitle == None:
            warnings.warn('Should Speicify ytitle!')
        if dim == '1D':
            if tag == 'pt':
                xbin = self.ptbin
            elif tag == 'eta':
                xbin = self.etabin
            elif tag == 'njet':
                xbin = self.njetbin
            elif tag == 'met':
                xbin = self.metbin
            else:
                raise ValueError(f'Tag{f} is not in the list.')
            nxbin = len(xbin) -1 
            self.__Histogram[dim][tag][name] = df.Histo1D((name,f"{name};{xtitle};{ytitle}",nxbin,xbin),*content,weight).GetValue()
            self.__Histogram[dim][tag][name].Sumw2()
            self.__Histogram[dim][tag][name].SetMinimum(0)

        if dim == '2D':
            if tag == 'pt':
                xbin = self.ptbin
                ybin = self.ptbin
            elif tag == 'eta':
                xbin = self.abs_etabin
                ybin = self.abs_etabin
            elif tag == 'pteta':
                xbin = self.ptbin
                ybin = self.abs_etabin
            else:
                raise ValueError(f'Tag{tag} is not in the list.')
            nxbin = len(xbin) -1 
            nybin = len(ybin) -1 
            self.__Histogram[dim][tag][name] = df.Histo2D((name,f"{name};{xtitle};{ytitle}",nxbin,xbin,nybin,ybin),*content,weight).GetValue()
            self.__Histogram[dim][tag][name].Sumw2()
        self.__Histogram[dim][tag][name].SetStats(0)
    def Save_Histogram(self,name:str,dim:str,tag:str):
        if name == None:
            raise ValueError('Should Specify Name of Histogram')
        if dim == None:
            raise ValueError('Should Specify Histogram')
        if tag == None:
            raise ValueError('Should Speicify What is the tag of the Histogram.')
        self.__Histogram[dim][tag][name].Write()
    def Merge_Hist(self,dim:str,tag,name:str,name2=None):
        if name2==None:
            name2 = 'pre_'+name

        if dim == '1D':
            if tag != 'HLT':
                eff = TEfficiency(self.__Histogram[dim][tag][name],self.__Histogram[dim][tag][name2])   
            else:
                eff = TEfficiency(self.__Histogram[dim][tag][name],self.__Histogram[dim][tag][name2])
            eff.SetTitle(f'Eff {name}')
            eff.SetName(f'Eff_{name}')
            eff.Write()
        elif dim == '2D':
            self.__Histogram[dim][tag][name].Divide(self.__Histogram[dim][tag][name2])
            self.__Histogram[dim][tag][name].Write()
        else:
            raise ValueError('Dimension {dim} is not in the list.')
    def Correct_VarName(self,name:list,process:str,tag:str)->list:
        
        corrected_name = []
        if process == 'OPS':
            for n in name: 
                corrected_name.append(n+'[OPS_'+tag+'_id]')
        
        return corrected_name

    def Run(self):
        #ROOT.ROOT.EnableImplicitMT()
        #df = ROOT.RDataFrame("Events",self.__FileIn_vecstr).Range(0,10000)
        df = ROOT.RDataFrame("Events",self.__FileIn_vecstr)
        ROOT.gInterpreter.ProcessLine(f'#include "./include/{self.__Year}/Header{self.__channel}.h"')
        print(f'Header File: "./include/{self.__Year}/Header{self.__channel}.h" is loaded')
        df_flag_trig = df.Filter(Trig_Cond(flag = self.__flag,joint = " || " ),"Flag Cut")
        
        if self.__channel == 'DoubleElectron'  :
            RECOWeight_Mul_TTC = 'Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]'
            RECOWeight_Mul_OPS = 'Electron_RECO_SF[OPS_l1_id]*Electron_RECO_SF[OPS_l2_id]'
        elif self.__channel == 'DoubleMuon':
            RECOWeight_Mul_TTC = '1.'
            RECOWeight_Mul_OPS = '1.'
        elif self.__channel == 'ElectronMuon':
            RECOWeight_Mul_TTC = 'Electron_RECO_SF[ttc_l2_id]'
            RECOWeight_Mul_OPS = 'Electron_RECO_SF[OPS_l2_id]'
            self.__Var_Name["OPS_p4"]["l1"]  = self.Correct_VarName(name=self.__Var_Name["OPS_p4"]["l1"],process='OPS',tag='l1')
            self.__Var_Name["OPS_p4"]["l2"]  = self.Correct_VarName(name=self.__Var_Name["OPS_p4"]["l2"],process='OPS',tag='l2')
         
        
        df_region_trig = df_flag_trig\
                .Filter('OPS_region == {0} || ttc_region == {0}'.format(self.__Var_Name["region"]))\
                .Define("isData","bool tag ; if ({0} == 1) tag = true; else tag = false;std::cout<<'1'<<std::endl;return tag".format(self.__isData))\
                .Define("ttc_flag","bool flag=false ; if (ttc_region =={0}) flag = true; return flag".format(self.__Var_Name["region"]))\
                .Define("dy_flag","bool flag=false ; if (OPS_region =={0}) flag = true; return flag".format(self.__Var_Name["region"]))\
                .Define("l1p4","TLorentzVector p4; if(ttc_region == {0}) p4.SetPtEtaPhiM({1},{2},{3},{4}) ;else p4.SetPtEtaPhiM({5},{6},{7},{8});return p4"\
                .format(self.__Var_Name["region"],*self.__Var_Name["ttc_p4"]["l1"],*self.__Var_Name["OPS_p4"]["l1"]))\
                .Define("l2p4","TLorentzVector k4; if(ttc_region == {0}) k4.SetPtEtaPhiM({1},{2},{3},{4}) ;else k4.SetPtEtaPhiM({5},{6},{7},{8});return k4"\
                .format(self.__Var_Name["region"],*self.__Var_Name["ttc_p4"]["l2"],*self.__Var_Name["OPS_p4"]["l2"]))\
                .Define("IDsf","ID_SF(l1p4.Pt(),l2p4.Pt(),l1p4.Eta(),l2p4.Eta())")\
                .Define("l1pt","l1p4.Pt()")\
                .Define("l2pt","l2p4.Pt()")\
                .Define("l1eta","l1p4.Eta()")\
                .Define("l2eta","l2p4.Eta()")\
                .Define("l1_abseta","abs(l1p4.Eta())")\
                .Define("l2_abseta","abs(l2p4.Eta())")
        
        if self.__Type=='Data':
            MET = 'MET_T1_pt'
            df_Offline_DileptonsCut = df_region_trig\
                .Define("met",f"{MET}")\
                .Filter('(l1p4+l2p4).M() >20 && l1p4.Pt() > 30 && l2p4.Pt() && l1p4.DeltaR(l2p4) > 0.3 && met >100','LeptonCut')\
                .Define('no_HLT','0.5')\
                .Define("weight","1.")
        else:
            MET = 'MET_T1Smear_pt'
            df_Offline_DileptonsCut = df_region_trig\
                .Define("met",f"{MET}")\
                .Filter('(l1p4+l2p4).M() >20 && l1p4.Pt() > 30 && l2p4.Pt() && l1p4.DeltaR(l2p4) > 0.3 && met >100','LeptonCut')\
                .Define('no_HLT','0.5')\
                .Define("weight",f"float w ; if (ttc_flag) w = puWeight*PrefireWeight*{RECOWeight_Mul_TTC}*IDsf;\
                else w = puWeight*PrefireWeight*IDsf*{RECOWeight_Mul_OPS};return w ")
        
        df_HLT_LEP = df_Offline_DileptonsCut\
                .Filter(Trig_Cond(flag = self.__HLT_LEP,joint = " || " ),"HLT_LEP_Trig")\
                .Define('HLT_LEP_pass','0.5')


        df_HLT_MET = df_Offline_DileptonsCut\
                .Filter(Trig_Cond(flag = self.__HLT_MET,joint = " || " ),"HLT_MET_Trig")\
                .Define('HLT_MET_pass','0.5')

        df_HLT_MET_highjet = df_HLT_MET\
                .Filter('n_tight_jet >3','pre_high_jet')
        df_HLT_MET_lowjet = df_HLT_MET\
                .Filter('n_tight_jet <3','pre_low_jet')
        df_HLT_MET_highpv = df_HLT_MET\
                .Filter('PV_npvs >30','pre_high_pv')
        df_HLT_MET_lowpv = df_HLT_MET\
                .Filter('PV_npvs <30','pre_low_pv')
        df_HLT_MET_highmet = df_HLT_MET\
                .Filter('met >150','pre_high_met')
        df_HLT_MET_lowmet = df_HLT_MET\
                .Filter('met <150','pre_low_met')
        
        df_HLT_LEPMET = df_HLT_LEP\
                .Filter(Trig_Cond(flag = self.__HLT_MET,joint = " || " ),"HLT_LEPMET_Trig")\
                .Define('HLT_LEPMET_pass','0.5')
        
        df_HLT_LEPMET_highjet = df_HLT_LEPMET\
                .Filter('n_tight_jet >3','high_jet')
        df_HLT_LEPMET_lowjet = df_HLT_LEPMET\
                .Filter('n_tight_jet <3','low_jet')
        df_HLT_LEPMET_highpv = df_HLT_LEPMET\
                .Filter('PV_npvs >30','high_pv')
        df_HLT_LEPMET_lowpv = df_HLT_LEPMET\
                .Filter('PV_npvs <30','low_pv')
        df_HLT_LEPMET_highmet = df_HLT_LEPMET\
                .Filter('met >150','high_met')
        df_HLT_LEPMET_lowmet = df_HLT_LEPMET\
                .Filter('met <150','low_met')
        
        weight_all = df_Offline_DileptonsCut.Sum("weight")
        weight_lep = df_HLT_LEP.Sum("weight")
        weight_met = df_HLT_MET.Sum("weight")
        weight_lepmet = df_HLT_LEPMET.Sum("weight")
        eff_lep =weight_lep.GetValue()/weight_all.GetValue()
        eff_met = weight_met.GetValue()/weight_all.GetValue()
        eff_lepmet= weight_lepmet.GetValue()/weight_all.GetValue()
        print("Total Events: {0}".format(df.Count().GetValue()))
        print("#Events Pass Region Cut: {0}".format(df_region_trig.Count().GetValue()))
        print("#Events Pass Offline DiLeptons Cut: {0}".format(df_Offline_DileptonsCut.Count().GetValue()))
        print("#Events Pass HLT_LEP Cut: {0}".format(df_HLT_LEP.Count().GetValue()))
        print("#Events Pass HLT_MET Cut: {0}".format(df_HLT_MET.Count().GetValue()))
        print("#Events Pass HLT_LEPMET Cut: {0}".format(df_HLT_LEPMET.Count().GetValue()))
        print(f"Efficiency for HLT_LEP: {eff_lep}")
        print(f"Efficiency for HLT_MET: {eff_met}")
        print(f"Efficiency for HLT_LEPMET: {eff_lepmet}")
        print(f"Correlation: {eff_lep*eff_met/eff_lepmet}")

        self.__Histogram['1D']['HLT']['No_HLT'] = df_Offline_DileptonsCut.Histo1D(("No_HLT","No_HLT",1,0,1),"no_HLT","weight").GetValue()
        self.__Histogram['1D']['HLT']['HLT_LEP'] = df_HLT_LEP.Histo1D(("HLT_LEP_pass","HLT_LEP_pass",1,0,1),"HLT_LEP_pass","weight").GetValue()
        self.__Histogram['1D']['HLT']['HLT_MET'] = df_HLT_MET.Histo1D(("HLT_MET_pass","HLT_MET_pass",1,0,1),"HLT_MET_pass","weight").GetValue()
        self.__Histogram['1D']['HLT']['HLT_LEPMET'] = df_HLT_LEPMET.Histo1D(("HLT_LEPMET_pass","HLT_LEPMET_pass",1,0,1),"HLT_LEPMET_pass","weight").GetValue()
        
        ###1D Histogram
    
        ##PT
        self.Init_Histogram(name='pre_l1pt',df=df_HLT_MET,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='pre_l1pt_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        
        self.Init_Histogram(name='l1pt',df=df_HLT_LEPMET,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        self.Init_Histogram(name='l1pt_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'])
        
        
        self.Init_Histogram(name='pre_l2pt',df=df_HLT_MET,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='pre_l2pt_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        
        self.Init_Histogram(name='l2pt',df=df_HLT_LEPMET,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        self.Init_Histogram(name='l2pt_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'])
        
        ##ETA
        self.Init_Histogram(name='pre_l1eta',df=df_HLT_MET,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='pre_l1eta_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        
        self.Init_Histogram(name='l1eta',df=df_HLT_LEPMET,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        self.Init_Histogram(name='l1eta_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
        
        
        self.Init_Histogram(name='pre_l2eta',df=df_HLT_MET,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='pre_l2eta_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        
        self.Init_Histogram(name='l2eta',df=df_HLT_LEPMET,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        self.Init_Histogram(name='l2eta_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
        
        ##others
        self.Init_Histogram(name='pre_njet',df=df_HLT_MET,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='pre_njet_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='pre_njet_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='pre_njet_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='pre_njet_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        
        self.Init_Histogram(name='njet',df=df_HLT_LEPMET,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='njet_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='njet_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='njet_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        self.Init_Histogram(name='njet_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
        
        self.Init_Histogram(name='pre_met',df=df_HLT_MET,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='pre_met_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='pre_met_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='pre_met_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='pre_met_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        
        self.Init_Histogram(name='met',df=df_HLT_LEPMET,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='met_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='met_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='met_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        self.Init_Histogram(name='met_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
        
        ###2D Histogram
        self.Init_Histogram(name='pre_l1l2pt',df=df_HLT_MET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='pre_l1l2pt_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        
        self.Init_Histogram(name='pre_l1l2eta',df=df_HLT_MET,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1eta','l2eta'])
        self.Init_Histogram(name='pre_l1l2eta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='pre_l1l2eta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='pre_l1l2eta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='pre_l1l2eta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='pre_l1l2eta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='pre_l1l2eta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        
        self.Init_Histogram(name='pre_l1pteta',df=df_HLT_MET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='pre_l1pteta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        
        self.Init_Histogram(name='pre_l2pteta',df=df_HLT_MET,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='pre_l2pteta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        #After LEPMET
        self.Init_Histogram(name='l1l2pt',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        self.Init_Histogram(name='l1l2pt_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
        
        self.Init_Histogram(name='l1l2eta',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1eta','l2eta'])
        self.Init_Histogram(name='l1l2eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='l1l2eta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='l1l2eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='l1l2eta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='l1l2eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        self.Init_Histogram(name='l1l2eta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
        
        self.Init_Histogram(name='l1pteta',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        self.Init_Histogram(name='l1pteta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'])
        
        self.Init_Histogram(name='l2pteta',df=df_HLT_LEPMET,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])
        self.Init_Histogram(name='l2pteta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'])


        self.__FileOut.cd()
        for name in ['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_lowmet','l1pt_highmet','l1pt_lowpv','l1pt_highpv'\
                ,'l2pt','l2pt_highjet','l2pt_lowjet','l2pt_lowmet','l2pt_highmet','l2pt_lowpv','l2pt_highpv']:
            self.Merge_Hist(dim='1D',tag='pt',name=name)
        for name in ['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_lowmet','l1eta_highmet','l1eta_lowpv','l1eta_highpv'\
                ,'l2eta','l2eta_highjet','l2eta_lowjet','l2eta_lowmet','l2eta_highmet','l2eta_lowpv','l2eta_highpv']:
            self.Merge_Hist(dim='1D',tag='eta',name=name)
        for name in ['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_lowmet','l1pteta_highmet','l1pteta_lowpv','l1pteta_highpv'\
                ,'l2pteta','l2pteta_highjet','l2pteta_lowjet','l2pteta_lowmet','l2pteta_highmet','l2pteta_lowpv','l2pteta_highpv']:
            self.Merge_Hist(dim='2D',tag='pteta',name=name)
        for name in ['l1l2pt','l1l2pt_highjet','l1l2pt_lowjet','l1l2pt_lowmet','l1l2pt_highmet','l1l2pt_lowpv','l1l2pt_highpv']:
            self.Merge_Hist(dim='2D',tag='pt',name=name)
    
        for name in ['l1l2eta','l1l2eta_highjet','l1l2eta_lowjet','l1l2eta_lowmet','l1l2eta_highmet','l1l2eta_lowpv','l1l2eta_highpv']:
            self.Merge_Hist(dim='2D',tag='eta',name=name)

        for name in ['HLT_MET','HLT_LEP','HLT_LEPMET']:
            self.Merge_Hist(dim='1D',tag='HLT',name=name,name2='No_HLT')
        #for dim in self.__Histogram.keys():
        #    for tag in self.__Histogram[dim].keys():
        #        for name in self.__Histogram[dim][tag].keys():
        #            self.Save_Histogram(name=name,tag=tag,dim=dim)
        
        
        self.__FileOut.Close()
