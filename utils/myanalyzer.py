import os 
import ROOT
from ROOT import TFile, TTree, TLorentzVector,TH1F,TEfficiency,TH2D
CURRENT_WORKDIR = os.getcwd()
from itertools import product
import math
from array import array
from math import sqrt

class analyzer():
    ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
    etabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
    jetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
    metbin=array('d',[100,110,120,130,140,160,180,200,250])
    abs_etabin=array('d',[0,0.4,0.9,1.5,2.5])
    def __init__(self,setting):
        
        self.infilename = setting.get('infilepath',None)
        self.outputdir = setting.get('outputdir',None)
        self.channel = setting.get('channel',None)
        self.property_name = setting.get('property_name',None)
        self.HLT_LEP = setting.get('HLT_LEP',None)
        self.HLT_MET = setting.get('HLT_MET',None)
        self.outfilename = setting.get('outfilename',None) 
        self.infilebasename = setting.get('infilebasename',None)

        if self.infilename == None :
            raise ValueError
        elif self.outputdir == None:
            raise ValueError
        elif self.channel == None:
            raise ValueError
        elif self.property_name == None:
            raise ValueError
        elif self.HLT_MET == None:
            raise ValueError
        elif self.HLT_LEP == None:
            raise ValueError
        elif self.outfilename == None:
            raise ValueError
        elif self.infilebasename == None:
            raise ValueError
        else:
            self.infile = TFile.Open(self.infilename)
            self.tree =  self.infile.Get('Events')
            self.entries = self.tree.GetEntries()
            print('Input File: {0}, total events: {1}, Channel: {2}'.format(self.infilebasename,self.entries,self.channel))
            self.outfile = TFile.Open(self.outfilename,"RECREATE")
            print('File: {0} created.'.format(self.outfilename))
            leptonSF =[]
            for weight_l1,weight_l2 in zip(self.property_name['weight']['l1'],self.property_name['weight']['l2']):
                leptonSF.append('self.tree.'+weight_l1+'[self.tree.{0}_l1_id]')
                leptonSF.append('self.tree.'+weight_l2+'[self.tree.{0}_l2_id]')
            #print('*'.join(leptonSF).format('ttc')) #could print this to see what is it.
            self.leptonSF ='*'.join(leptonSF) 
    def build_hist1d(self,name:str,bintype:str,xtitle:str,forlep:bool):
        
        command = '''self.h1_{0} = TH1F("{0}","{0}",len(self.{1})-1,self.{1})
        \nself.h1_{0}.Sumw2()
        \nself.h1_{0}.SetMinimum(0)
        \nself.h1_{0}.GetXaxis().SetTitle('{2}')
        \nself.h1_{0}.GetYaxis().SetTitle('Efficiency')
        \nself.h1_{0}.SetStats(0)'''
        if forlep:
            exec(command.format('l1'+name,bintype,'Leading '+xtitle)) #pass MET&LEP trigger for leading lepton
            exec(command.format('pre_l1'+name,bintype,'Leading '+xtitle)) #before LEP trigger for leading lepton

            exec(command.format('l2'+name,bintype,'Subleading '+xtitle)) #pass MET&LEP trigger for leading lepton
            exec(command.format('pre_l2'+name,bintype,'Subleading '+xtitle)) #before LEP trigger for leading lepton
        #for observables, MET and nJet
        else:
            exec(command.format(name,bintype,xtitle)) #pass MET&LEP trigger
            exec(command.format('pre_'+name,bintype,xtitle)) #before LEP trigger 

    def build_hist2d(self,name:str,xbintype:str,ybintype:str,xtitle:str,ytitle:str,forlep:bool):
        
        command = '''self.h2_{0} = TH2D("{0}","{0}",len(self.{1})-1,self.{1},len(self.{2})-1,self.{2})
        \nself.h2_{0}.Sumw2()
        \nself.h2_{0}.SetMinimum(0)
        \nself.h2_{0}.GetXaxis().SetTitle('{2}')
        \nself.h2_{0}.GetYaxis().SetTitle('{3}')
        \nself.h2_{0}.SetStats(0)'''
        
        if forlep:
            exec(command.format('l1'+name,xbintype,ybintype,'Leading '+xtitle,'Leading '+ytitle)) #pass MET&LEP trigger for leading lepton
            exec(command.format('pre_l1'+name,xbintype,ybintype,'Leading '+xtitle,'Leading '+ytitle)) #before LEP trigger for leading lepton

            exec(command.format('l2'+name,xbintype,ybintype,'Subleading '+xtitle,'Subleading '+ytitle)) #pass MET&LEP trigger for leading lepton
            exec(command.format('pre_l2'+name,xbintype,ybintype,'Subleading '+xtitle,'Subleading '+ytitle)) #before LEP trigger for leading lepton
        else:
            exec(command.format(name,xbintype,ybintype,xtitle,ytitle)) #pass MET&LEP trigger 
            exec(command.format('pre_'+name,xbintype,ybintype,xtitle,ytitle)) #before MET&LEP trigger 

    def lepton_property_register(self,process:str):

        #To regsiter 2 Leptons four momentum
        self.l1p4.SetPtEtaPhiM(eval('self.tree.'+self.property_name[process+'_p4']['l1'][0]),eval('self.tree.'+self.property_name[process+'_p4']['l1'][1]),eval('self.tree.'+self.property_name[process+'_p4']['l1'][2]),eval('self.tree.'+self.property_name[process+'_p4']['l1'][3]))
        
        self.l2p4.SetPtEtaPhiM(eval('self.tree.'+self.property_name[process+'_p4']['l2'][0]),eval('self.tree.'+self.property_name[process+'_p4']['l2'][1]),eval('self.tree.'+self.property_name[process+'_p4']['l2'][2]),eval('self.tree.'+self.property_name[process+'_p4']['l2'][3]))
        if  'TT' in self.infilebasename: 
            self.weight = eval(self.leptonSF.format(process))*self.tree.puWeight * self.tree.PrefireWeight
        else :
            self.weight=1.

    def eff_save(self,name:str):
        '''
        Save Efficiency for 2 1D hist
        '''
        command='''
        \nself.Eff_{0} = TEfficiency(self.h1_{0},self.h1_pre_{0})
        \nself.Eff_{0}.SetTitle('Eff {0}')
        \nself.Eff_{0}.SetName('Eff_{0}')
        \nself.Eff_{0}.Write()
        \nself.h1_{0}.Write()
        '''
        exec(command.format(name))
    def eff_2dsave(self,name:str):
    
        command ='''
        \nself.h2_{0}.Divide(self.h2_pre_{0})
        \nself.h2_{0}.Write()
        '''
        exec(command.format(name))
    def analyze(self):
        
        ####1D histogram
        ###For lep
        ##pt 
        self.build_hist1d(name='pt',bintype = 'ptbin',xtitle ='Lepton P_{T} [GeV]',forlep=True)
        # jet criteria
        self.build_hist1d(name='pt_lowjet',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        self.build_hist1d(name='pt_highjet',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        # pv criteria
        self.build_hist1d(name='pt_lowpv',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        self.build_hist1d(name='pt_highpv',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        # met criteria
        self.build_hist1d(name='pt_lowMET',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        self.build_hist1d(name='pt_highMET',bintype='ptbin',xtitle='Lepton P_{T} [GeV]',forlep=True)
        ##

        ##eta
        self.build_hist1d(name='eta',bintype = 'etabin',xtitle ='Lepton #eta',forlep=True)
        # jet criteria
        self.build_hist1d(name='eta_lowjet',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        self.build_hist1d(name='eta_highjet',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        # pv criteria
        self.build_hist1d(name='eta_lowpv',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        self.build_hist1d(name='eta_highpv',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        # MET
        self.build_hist1d(name='eta_lowMET',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        self.build_hist1d(name='eta_highMET',bintype='etabin',xtitle='Lepton #eta',forlep=True)
        ##
        
        ###For observable
        ##jet and met
        self.build_hist1d(name='njet',bintype='jetbin',xtitle='N_{jets}',forlep=False)
        self.build_hist1d(name='met',bintype='metbin',xtitle='MET [GeV]',forlep=False)
        # pv criteria
        self.build_hist1d(name='njet_lowpv',bintype='jetbin',xtitle='N_{jets}',forlep=False)
        self.build_hist1d(name='njet_highpv',bintype='jetbin',xtitle='N_{jets}',forlep=False)
        self.build_hist1d(name='met_lowpv',bintype='metbin',xtitle='MET [GeV]',forlep=False)
        self.build_hist1d(name='met_highpv',bintype='metbin',xtitle='MET [GeV]',forlep=False)
        # met criteria
        self.build_hist1d(name='njet_lowMET',bintype='jetbin',xtitle='N_{jets}',forlep=False)
        self.build_hist1d(name='njet_highMET',bintype='jetbin',xtitle='N_{jets}',forlep=False)
        self.build_hist1d(name='met_lowjet',bintype='metbin',xtitle='MET [GeV]',forlep=False)
        self.build_hist1d(name='met_highjet',bintype='metbin',xtitle='MET [GeV]',forlep=False)
        # jet criteria
        ##
        ###
        ####
        
        ####2D histogram
        ###For lepton
        ##pt_eta
        #
        self.build_hist2d(name='pteta',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
        #jet criteria
        self.build_hist2d(name='pteta_highjet',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
        self.build_hist2d(name='pteta_lowjet',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
    
        #MET criteria
        self.build_hist2d(name='pteta_highMET',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
        self.build_hist2d(name='pteta_lowMET',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)

        #pv criteria
        self.build_hist2d(name='pteta_highpv',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
        self.build_hist2d(name='pteta_lowpv',xbintype='ptbin',ybintype='abs_etabin',xtitle='Lepton P_{T} [GeV]',ytitle='Lepton |#eta|',forlep=True)
        ##
        ###For Two lepton 
        ##pt
        #
        self.build_hist2d(name='l1l2pt',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #jet criteria
        self.build_hist2d(name='l1l2pt_lowjet',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2pt_highjet',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #MET criteria
        self.build_hist2d(name='l1l2pt_lowMET',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2pt_highMET',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #pv criteria
        self.build_hist2d(name='l1l2pt_lowpv',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2pt_highpv',xbintype='ptbin',ybintype='ptbin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)

        ##eta
        self.build_hist2d(name='l1l2eta',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #jet criteria
        self.build_hist2d(name='l1l2eta_lowjet',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2eta_highjet',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #MET criteria
        self.build_hist2d(name='l1l2eta_lowMET',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2eta_highMET',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        #pv criteria
        self.build_hist2d(name='l1l2eta_lowpv',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        self.build_hist2d(name='l1l2eta_highpv',xbintype='abs_etabin',ybintype='abs_etabin',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Subleading Lepton P_{T} [GeV]',forlep=False)
        
        self.l1p4=TLorentzVector()
        self.l2p4=TLorentzVector()
        self.all_events = TH1F('all_events','tag',1,0,1)
        self.pass_lep_trigger= TH1F('pass_lep_trigger','pass_lep_trigger',1,0,1)
        self.pass_met_trigger= TH1F('pass_met_trigger','pass_met_trigger',1,0,1)
        self.pass_lepmet_trigger= TH1F('pass_lepmet_trigger','pass_lepmet_trigger',1,0,1)
        
        if 'TT' in self.infilebasename:
            self.entries=1500000
            print('File total events -> {}'.format(self.entries))
        for ientry in range(0,self.entries):
            self.tree.GetEntry(ientry)
            if 'TT' in self.infilebasename:
                met = self.tree.MET_T1Smear_pt #
            else:
                met =  self.tree.MET_T1_pt
            if ientry%15000 == 0: 
                print('Process Progress for '+self.outfilename+' :' +str(round(ientry/self.entries,4)*100)+'%\n')
            if not (self.tree.Flag_goodVertices and self.tree.Flag_globalSuperTightHalo2016Filter and self.tree.Flag_HBHENoiseFilter and self.tree.Flag_HBHENoiseIsoFilter and self.tree.Flag_EcalDeadCellTriggerPrimitiveFilter and self.tree.Flag_BadPFMuonFilter and self.tree.Flag_eeBadScFilter and self.tree.Flag_ecalBadCalibFilter) :
                continue
            
            if not (self.tree.DY_region == self.property_name['region'] or self.tree.ttc_region == self.property_name['region']):
                continue

            if self.tree.DY_region == self.property_name['region']:
                self.lepton_property_register(process = 'DY')
            else: #ttc process
                self.lepton_property_register(process = 'ttc')
          
            #Offline Selection
            if (self.l1p4+self.l2p4).M() < 20 : continue
            if not (self.l1p4.Pt() > 30 or self.l2p4.Pt() > 30) : continue
            if (self.l1p4.DeltaR(self.l2p4)<0.3) : continue
            if met < 100 : continue
            self.all_events.Fill(0.5,self.weight)

            if eval(self.HLT_LEP) :
                self.pass_lep_trigger.Fill(0.5,self.weight)
            if eval(self.HLT_MET):
                ##HLT_MET: -> Trigger
                ###Without Criteria
                self.pass_met_trigger.Fill(0.5,self.weight)
                self.h1_pre_l1pt.Fill(self.l1p4.Pt(),self.weight)
                self.h1_pre_l1eta.Fill(self.l1p4.Eta(),self.weight)
                self.h1_pre_l2pt.Fill(self.l2p4.Pt(),self.weight)
                self.h1_pre_l2eta.Fill(self.l2p4.Eta(),self.weight)
                self.h1_pre_njet.Fill(self.tree.n_tight_jet,self.weight)
                self.h1_pre_met.Fill(met,self.weight)
                self.h2_pre_l1pteta.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                self.h2_pre_l2pteta.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                self.h2_pre_l1l2pt.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                self.h2_pre_l1l2eta.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                
                if self.tree.n_tight_jet>3: #criteria for njet
                    self.h1_pre_l1pt_highjet.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_highjet.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_highjet.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_highjet.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_highjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_highjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_highjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_highjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                else: 
                    
                    self.h1_pre_l1pt_lowjet.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_lowjet.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_lowjet.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_lowjet.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_lowjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_lowjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_lowjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_lowjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                if self.tree.PV_npvs > 30:
                    
                    self.h1_pre_l1pt_highpv.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_highpv.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_highpv.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_highpv.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_highpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_highpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_highpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_highpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                
                else:
                
                    self.h1_pre_l1pt_lowpv.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_lowpv.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_lowpv.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_lowpv.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_lowpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_lowpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_lowpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_lowpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                if met > 150: 

                    self.h1_pre_l1pt_highMET.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_highMET.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_highMET.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_highMET.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_highMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_highMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_highMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_highMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                
                else:
                
                    self.h1_pre_l1pt_lowMET.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_pre_l1eta_lowMET.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_pre_l2pt_lowMET.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_pre_l2eta_lowMET.Fill(self.l2p4.Eta(),self.weight)
                    
                    self.h2_pre_l1pteta_lowMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_pre_l2pteta_lowMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_pre_l1l2pt_lowMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_pre_l1l2eta_lowMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                if(eval(self.HLT_LEP)):
                    # Pass LEP & MET trigger
                    self.pass_lepmet_trigger.Fill(0.5,self.weight)
                    self.h1_l1pt.Fill(self.l1p4.Pt(),self.weight)
                    self.h1_l1eta.Fill(self.l1p4.Eta(),self.weight)
                    self.h1_l2pt.Fill(self.l2p4.Pt(),self.weight)
                    self.h1_l2eta.Fill(self.l2p4.Eta(),self.weight)
                    self.h1_njet.Fill(self.tree.n_tight_jet,self.weight)
                    self.h1_met.Fill(met,self.weight)
                    self.h2_l1pteta.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                    self.h2_l2pteta.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                    self.h2_l1l2pt.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                    self.h2_l1l2eta.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                    
                    if self.tree.n_tight_jet>3: #criteria for njet
                        self.h1_l1pt_highjet.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_highjet.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_highjet.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_highjet.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_highjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_highjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_highjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_highjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                    else: 
                        
                        self.h1_l1pt_lowjet.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_lowjet.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_lowjet.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_lowjet.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_lowjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_lowjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_lowjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_lowjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                    if self.tree.PV_npvs > 30:
                        
                        self.h1_l1pt_highpv.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_highpv.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_highpv.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_highpv.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_highpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_highpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_highpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_highpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                    
                    else:
                    
                        self.h1_l1pt_lowpv.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_lowpv.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_lowpv.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_lowpv.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_lowpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_lowpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_lowpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_lowpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)

                    if met > 150: 

                        self.h1_l1pt_highMET.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_highMET.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_highMET.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_highMET.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_highMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_highMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_highMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_highMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)
                    
                    else:
                    
                        self.h1_l1pt_lowMET.Fill(self.l1p4.Pt(),self.weight)
                        self.h1_l1eta_lowMET.Fill(self.l1p4.Eta(),self.weight)
                        self.h1_l2pt_lowMET.Fill(self.l2p4.Pt(),self.weight)
                        self.h1_l2eta_lowMET.Fill(self.l2p4.Eta(),self.weight)
                        
                        self.h2_l1pteta_lowMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),self.weight)
                        self.h2_l2pteta_lowMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),self.weight)
                        self.h2_l1l2pt_lowMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),self.weight)
                        self.h2_l1l2eta_lowMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),self.weight)



        Eff_mettrigger = TEfficiency(self.pass_met_trigger,self.all_events)
        Eff_leptrigger = TEfficiency(self.pass_lep_trigger,self.all_events)
        Eff_lepmettrigger = TEfficiency(self.pass_lepmet_trigger, self.all_events)

        lepeff = Eff_leptrigger.GetEfficiency(1)
        lepeff_err = max(Eff_leptrigger.GetEfficiencyErrorUp(1),Eff_leptrigger.GetEfficiencyErrorLow(1))

        meteff = Eff_mettrigger.GetEfficiency(1)
        meteff_err = max(Eff_mettrigger.GetEfficiencyErrorUp(1),Eff_mettrigger.GetEfficiencyErrorLow(1))

        lepmeteff = Eff_lepmettrigger.GetEfficiency(1)
        lepmeteff_err = max(Eff_lepmettrigger.GetEfficiencyErrorUp(1),Eff_lepmettrigger.GetEfficiencyErrorLow(1))

        alpha = (lepeff*meteff)/lepmeteff

        alphaerr=sqrt((lepeff_err**2)*(meteff**2)+(lepeff**2)*(meteff_err**2)+lepeff*lepeff*meteff*meteff*lepmeteff_err*lepmeteff_err)/lepmeteff


        print("\nFile: {} // Efficiency & Alpha ".format(self.infilename))
        print("lep trigger eff: {} +- {}".format(lepeff,lepeff_err))
        print("met trigger eff: {} +- {}".format(meteff,meteff_err))
        print("lepmet trigger eff: {} +- {}".format(lepmeteff,lepmeteff_err))
        print("Alpha: {} +- {}\n".format(alpha,alphaerr))
        
        self.outfile.cd()

        Eff_mettrigger.SetName('Eff_mettrigger')
        Eff_leptrigger.SetName('Eff_leptrigger')
        Eff_lepmettrigger.SetName('Eff_lepmettrigger')
        #self.eff_save(name='njet')
        #self.eff_save(name='met')
        Eff_mettrigger.Write() 
        Eff_leptrigger.Write() 
        Eff_lepmettrigger.Write() 
        self.eff_save(name='l1pt') 
        self.eff_save(name='l1pt_lowjet') 
        self.eff_save(name='l1pt_highjet') 
        self.eff_save(name='l1pt_lowpv') 
        self.eff_save(name='l1pt_highpv') 
        self.eff_save(name='l1pt_lowMET') 
        self.eff_save(name='l1pt_highMET')


        self.eff_save(name='l1eta') 
        self.eff_save(name='l1eta_lowjet') 
        self.eff_save(name='l1eta_highjet') 
        self.eff_save(name='l1eta_lowpv') 
        self.eff_save(name='l1eta_highpv') 
        self.eff_save(name='l1eta_lowMET') 
        self.eff_save(name='l1eta_highMET') 


        self.eff_save(name='l2pt') 
        self.eff_save(name='l2pt_lowjet') 
        self.eff_save(name='l2pt_highjet') 
        self.eff_save(name='l2pt_lowpv') 
        self.eff_save(name='l2pt_highpv') 
        self.eff_save(name='l2pt_lowMET') 
        self.eff_save(name='l2pt_highMET')


        self.eff_save(name='l2eta') 
        self.eff_save(name='l2eta_lowjet') 
        self.eff_save(name='l2eta_highjet') 
        self.eff_save(name='l2eta_lowpv') 
        self.eff_save(name='l2eta_highpv') 
        self.eff_save(name='l2eta_lowMET') 
        self.eff_save(name='l2eta_highMET') 


        self.eff_2dsave(name='l1l2pt')
        self.eff_2dsave(name='l1l2pt_lowjet')
        self.eff_2dsave(name='l1l2pt_highjet')
        self.eff_2dsave(name='l1l2pt_lowpv')
        self.eff_2dsave(name='l1l2pt_highpv')
        self.eff_2dsave(name='l1l2pt_lowMET')
        self.eff_2dsave(name='l1l2pt_highMET')

        self.eff_2dsave(name='l1l2eta')
        self.eff_2dsave(name='l1l2eta_lowjet')
        self.eff_2dsave(name='l1l2eta_highjet')
        self.eff_2dsave(name='l1l2eta_lowpv')
        self.eff_2dsave(name='l1l2eta_highpv')
        self.eff_2dsave(name='l1l2eta_lowMET')
        self.eff_2dsave(name='l1l2eta_highMET')


        self.eff_2dsave(name='l1pteta')
        self.eff_2dsave(name='l1pteta_lowjet')
        self.eff_2dsave(name='l1pteta_highjet')
        self.eff_2dsave(name='l1pteta_lowpv')
        self.eff_2dsave(name='l1pteta_highpv')
        self.eff_2dsave(name='l1pteta_lowMET')
        self.eff_2dsave(name='l1pteta_highMET')


        self.eff_2dsave(name='l2pteta')
        self.eff_2dsave(name='l2pteta_lowjet')
        self.eff_2dsave(name='l2pteta_highjet')
        self.eff_2dsave(name='l2pteta_lowpv')
        self.eff_2dsave(name='l2pteta_highpv')
        self.eff_2dsave(name='l2pteta_lowMET')
        self.eff_2dsave(name='l2pteta_highMET')

        self.outfile.Close()
