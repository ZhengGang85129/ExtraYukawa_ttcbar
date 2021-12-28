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
            if not (self.tree.Flag_goodVertices and self.tree.Flag_globalSuperTightHalo2016Filter and self.tree.Flag_HBHENoiseFilter and self.tree.Flag_HBHENoiseIsoFilter and self.tree.Flag_EcalDeadCellTriggerPrimitiveFilter and self.tree.Flag_BadPFMuonFilter and self.tree.Flag_eeBadScFilter and self.tree.Flag_ecalBadCalibFilter):
                continue
        
