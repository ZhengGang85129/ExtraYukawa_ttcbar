import os 
import ROOT
from ROOT import TFile, TTree, TLorentzVector,TH1F
CURRENT_WORKDIR = os.getcwd()

import build_histogram as bh 
import command_string as cmd_str


class analyzer():
    def __init__(self,infilename,outfilename):
        #self.outfile = TFile.Open(outfilename,'RECREATE')
        self.infilename = infilename
        self.infile = TFile.Open(infilename)
        self.tree =  self.infile.Get('Events')
        self.entries = self.tree.GetEntries()
        
        bh._global_definition()
        bh.build_1Dhistogram_for_lep(command=cmd_str.h1_lepcommand)
        bh.build_1Dhistogram_for_njet(command=cmd_str.h1_njetcommand)
        bh.build_1Dhistogram_for_met(command=cmd_str.h1_metcommand)
        bh.build_1Dhistogram_for_pu(command=cmd_str.h1_pucommand)
        bh.build_2Dhistogram_for_lep(command=cmd_str.h2_lepcommand)
        bh.build_2Dhistogram_for_2lep(command=cmd_str.h2_2lepcommand)
        bh.build_tag_histogram()
    def selection(self):
        pass
    def write(self):
        pass
    def deactivate(self):
        bh._global_definition(True)
        bh.build_1Dhistogram_for_lep(True,command=cmd_str.del_h1_lepcommand)
        bh.build_1Dhistogram_for_njet(True,command=cmd_str.del_h1_njetcommand)
        bh.build_1Dhistogram_for_met(True,command=cmd_str.del_h1_metcommand)
        bh.build_1Dhistogram_for_pu(True,command=cmd_str.del_h1_pucommand)
        bh.build_2Dhistogram_for_lep(True,command=cmd_str.del_h2_lepcommand)
        bh.build_2Dhistogram_for_2lep(True,command=cmd_str.del_h2_2lepcommand)
        bh.build_tag_histogram(True)

class ee_analyzer(analyzer):
    def selection(self):
        for ientry in range(0,self.entries):
            self.tree.GetEntry(ientry)
            if 'TT' in self.infilename:
                met = self.tree.MET_T1Smear_pt
            else:
                met =  self.tree.MET_T1_pt
            if ientry%100 ==0: print('processing {0}'.format(ientry))
        
            if ientry ==1:
                print(cmd_str.fill_histocommand.format(3,'DY_l1_pt','DY_l1_eta','DY_l1_phi','DY_l1_mass','DY_l2_pt','DY_l2_eta','DY_l2_phi','DY_l2_mass','self.tree.Electron_RECO_SF[self.tree.DY_l1_id]*self.tree.Electron_RECO_SF[self.tree.DY_l2_id]*self.tree.Electron_CutBased_TightID_SF[self.tree.DY_l1_id]*self.tree.Electron_CutBased_TightID_SF[self.tree.DY_l2_id]','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','self.tree.Electron_RECO_SF[self.tree.ttc_l1_id]*self.tree.Electron_RECO_SF[self.tree.ttc_l2_id]*self.tree.Electron_CutBased_TightID_SF[self.tree.ttc_l1_id]*self.tree.Electron_CutBased_TightID_SF[self.tree.ttc_l2_id]','self.tree.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or self.tree.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or self.tree.HLT_passEle32WPTight or self.tree.HLT_Ele35_WPTight_Gsf','self.tree.HLT_PFMET120_PFMHT120_IDTight or self.tree.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight or self.tree.HLT_PFHT500_PFMET100_PFMHT100_IDTight or self.tree.HLT_PFHT700_PFMET85_PFMHT85_IDTight or self.tree.HLT_PFHT800_PFMET75_PFMHT75_IDTight'))





