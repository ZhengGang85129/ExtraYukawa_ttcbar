h1_lepcommand ='''
global h1_{0}{1}{2}{3}{4}
h1_{0}{1}{2}{3}{4} = TH1F("{0}{1}{2}{3}{4}","{0}{1}{2}{3}{4}",len({5})-{6},{7})
h1_{0}{1}{2}{3}{4}.Sumw2()
h1_{0}{1}{2}{3}{4}.SetMinimum(0)
h1_{0}{1}{2}{3}{4}.GetXaxis().SetTitle('{8}')
h1_{0}{1}{2}{3}{4}.GetYaxis().SetTitle('Efficiency')
h1_{0}{1}{2}{3}{4}.SetStats(0)
'''
del_h1_lepcommand='''h1_{0}{1}{2}{3}{4} = None'''

h1_njetcommand ='''
global h1_{0}njet{1}{2}
h1_{0}njet{1}{2}= TH1F("{0}njet{1}{2}","{0}njet{1}{2}",len(jetbin)-1,jetbin)
h1_{0}njet{1}{2}.Sumw2()
h1_{0}njet{1}{2}.SetMinimum(0)
h1_{0}njet{1}{2}.GetXaxis().SetTitle('{3}')
h1_{0}njet{1}{2}.GetYaxis().SetTitle('Efficiency')
h1_{0}njet{1}{2}.SetStats(0)
'''
del_h1_njetcommand='''h1_{0}njet{1}{2} = None'''

h1_metcommand ='''
global h1_{0}met{1}{2}
h1_{0}met{1}{2}= TH1F("{0}met{1}{2}","{0}met{1}{2}",len(metbin)-1,metbin)
h1_{0}met{1}{2}.Sumw2()
h1_{0}met{1}{2}.SetMinimum(0)
h1_{0}met{1}{2}.GetXaxis().SetTitle('{3}')
h1_{0}met{1}{2}.GetYaxis().SetTitle('Efficiency')
h1_{0}met{1}{2}.SetStats(0)
'''
del_h1_metcommand='''h1_{0}met{1}{2} = None'''

h1_pucommand ='''
global h1_{0}pu{1}
h1_{0}pu{1}= TH1F("{0}pu{1}","{0}pu{1}",40,0,80)
h1_{0}pu{1}.Sumw2()
h1_{0}pu{1}.SetMinimum(0)
h1_{0}pu{1}.SetStats(0)
'''
del_h1_pucommand='''h1_{0}pu{1} = None'''

h2_lepcommand='''
global h2_{0}{1}pteta{2}{3}
h2_{0}{1}pteta{2}{3}= TH2D("{0}{1}pteta{2}{3}","{0}{1}pteta{2}{3}",6,tdl1ptbin,4,tdlepetabin)
h2_{0}{1}pteta{2}{3}.Sumw2()
h2_{0}{1}pteta{2}{3}.SetStats(0)
h2_{0}{1}pteta{2}{3}.GetXaxis().SetTitle('{4}')
h2_{0}{1}pteta{2}{3}.GetYaxis().SetTitle('{5}')
h2_{0}{1}pteta{2}{3}.SetStats(0)
'''
del_h2_lepcommand='''
del h2_{0}{1}pteta{2}{3}
'''

h2_2lepcommand='''
global h2_{0}l1l2{1}{2}{3}
h2_{0}l1l2{1}{2}{3}= TH2D("{0}l1l2{1}{2}{3}","{0}l1l2{1}{2}{3}",{4},{5},{6},{7})
h2_{0}l1l2{1}{2}{3}.Sumw2()
h2_{0}l1l2{1}{2}{3}.SetStats(0)
h2_{0}l1l2{1}{2}{3}.GetXaxis().SetTitle('{8}')
h2_{0}l1l2{1}{2}{3}.GetYaxis().SetTitle('{9}')
h2_{0}l1l2{1}{2}{3}.SetStats(0)
'''
del_h2_2lepcommand='''
del h2_{0}l1l2{1}{2}{3}
'''

fill_histocommand='''
if not (self.tree.Flag_goodVertices and self.tree.Flag_globalSuperTightHalo2016Filter and self.tree.Flag_HBHENoiseFilter and self.tree.Flag_HBHENoiseIsoFilter and self.tree.Flag_EcalDeadCellTriggerPrimitiveFilter and self.tree.Flag_BadPFMuonFilter and self.tree.Flag_eeBadScFilter and self.tree.Flag_ecalBadCalibFilter):
    if not(self.tree.DY_region == {0} or self.tree.ttc_region == {0}):
        continue
    if self.tree.DY_region == {0}:
        l1p4.SetPtEtaPhiM(self.tree.{1},self.tree.{2},self.tree.{3},self.{4})
        l2p4.SetPtEtaPhiM(self.tree.{5},self.tree.{6},self.tree.{7},self.tree.{8})        
        if 'TT' in self.infilename:
            weight = {9} * self.tree.puWeight * self.tree.PrefireWeight
        else:
            weight =1.
    if self.tree.ttc_region == {0}:
        l1p4.SetPtEtaPhiM(self.tree.{10},self.tree.{11},self.tree.{12},self.tree.{13})
        l2p4.SetPtEtaPhiM(self.tree.{14},self.tree.{15},self.tree.{16},self.tree.{17} )        
        if 'TT' in self.infilename:
            weight = {18} * self.tree.puWeight * self.tree.PrefireWeight
        else:
            weight =1.

    if (l1p4+l2p4).M() < 20:
        continue
    if not(l1p4.Pt() >30 or l2p4.Pt() >30):
        continue
    if (l1p4.DeltaR(l2p4)<0.3):continue
    if met <100:contiune

    all_events1.Fill(0.5,weight)
    all_events2.Fill(0.5,weight)
    all_events3.Fill(0.5,weight)

    if({19}):
        pass_lep_trigger.Fill(0.5,weight)
    if({20})
        pass_met_trigger.Fill(0.5,weight)
        h1_pre_l1pt.Fill(l1p4.Pt(),weight)
        h1_pre_l1eta.Fill(l1p4.Eta(),weight)
        h1_pre_l2pt.Fill(l2p4.Pt(),weight)
        h1_pre_l2eta.Fill(l2p4.Eta(),weight)
        h1_pre_njet.Fill(self.tree.n_tight_jet,weight)
        h1_pre_met.Fill(met,weight)
        h2_pre_l1pteta.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
        h2_pre_l2pteta.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
        h2_pre_l1l2pt.Fill(l1p4.Pt(),l2p4.Pt(),weight)
        h2_pre_l1l2eta.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        if self.tree.n_tight_jet > 3 :
            h1_pre_l1pt_highjet.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_highjet.Fill(l1p4.Eta(),weight)
            h1_pre_l2_pt_highjet.Fill(l2p4.Pt(),weight)
            h1_pre_l2_eta_highjet.Fill(l2p4.Eta(),weight)

            h2_pre_l1pteta_highjet.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_highjet.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_highjet.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_highjet.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        else:
            h1_pre_l1pt_lowjet.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_lowjet.Fill(l1p4.Eta(),weight)
            h1_pre_l2_pt_lowjet.Fill(l2p4.Pt(),weight)
            h1_pre_l2_eta_lowjet.Fill(l2p4.Eta(),weight)
            
            h2_pre_l1pteta_lowjet.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_lowjet.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_lowjet.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_lowjet.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        if (self.tree.PV_npvs) > 30:
            h1_pre_l1pt_highpv.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_highpv.Fill(l1p4.Eta(),weight)
            h1_pre_l2pt_highpv.Fill(l2p4.Pt(),weight)
            h1_pre_l2eta_highpv.Fill(l2p4.Eta(),weight)
            
            h2_pre_l1pteta_highpv.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_highpv.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_highpv.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_highpv.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        else:
            h1_pre_l1pt_lowpv.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_lowpv.Fill(l1p4.Eta(),weight)
            h1_pre_l2pt_lowpv.Fill(l2p4.Pt(),weight)
            h1_pre_l2eta_lowpv.Fill(l2p4.Eta(),weight)
            
            h2_pre_l1pteta_lowpv.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_lowpv.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_lowpv.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_lowpv.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        if (met > 150):
            h1_pre_l1pt_highMET.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_highMET.Fill(l1p4.Eta(),weight)
            h1_pre_l2pt_highMET.Fill(l2p4.Pt(),weight)
            h1_pre_l2eta_highMET.Fill(l2p4.Eta(),weight)
            
            h2_pre_l1pteta_highMET.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_highMET.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_highMET.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_highMET.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        else:
            h1_pre_l1pt_lowMET.Fill(l1p4.Pt(),weight)
            h1_pre_l1eta_lowMET.Fill(l1p4.Eta(),weight)
            h1_pre_l2pt_lowMET.Fill(l2p4.Pt(),weight)
            h1_pre_l2eta_lowMET.Fill(l2p4.Eta(),weight)
            
            h2_pre_l1pteta_lowMET.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_pre_l2pteta_lowMET.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_pre_l1l2pt_lowMET.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_pre_l1l2eta_lowMET.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
        
        if({19}):
            pass_lepmet_trigger.Fill(0.5,weight)
            h1_l1pt.Fill(l1p4.Pt(),weight)
            h1_l1eta.Fill(l1p4.Eta(),weight)
            h1_l2pt.Fill(l2p4.Pt(),weight)
            h1_l2eta.Fill(l2p4.Eta(),weight)
            h1_njet.Fill(self.tree.n_tight_jet,weight)
            h1_met.Fill(met,weight)
            h2_l1pteta.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
            h2_l2pteta.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
            h2_l1l2pt.Fill(l1p4.Pt(),l2p4.Pt(),weight)
            h2_l1l2eta.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
            if self.tree.n_tight_jet > 3 :
                h1_l1pt_highjet.Fill(l1p4.Pt(),weight)
                h1_l1eta_highjet.Fill(l1p4.Eta(),weight)
                h1_l2_pt_highjet.Fill(l2p4.Pt(),weight)
                h1_l2_eta_highjet.Fill(l2p4.Eta(),weight)

                h2_l1pteta_highjet.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_highjet.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_highjet.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_highjet.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
            else:
                h1_l1pt_lowjet.Fill(l1p4.Pt(),weight)
                h1_l1eta_lowjet.Fill(l1p4.Eta(),weight)
                h1_l2_pt_lowjet.Fill(l2p4.Pt(),weight)
                h1_l2_eta_lowjet.Fill(l2p4.Eta(),weight)
                
                h2_l1pteta_lowjet.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_lowjet.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_lowjet.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_lowjet.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
            if (self.tree.PV_npvs) > 30:
                h1_l1pt_highpv.Fill(l1p4.Pt(),weight)
                h1_l1eta_highpv.Fill(l1p4.Eta(),weight)
                h1_l2pt_highpv.Fill(l2p4.Pt(),weight)
                h1_l2eta_highpv.Fill(l2p4.Eta(),weight)
                
                h2_l1pteta_highpv.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_highpv.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_highpv.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_highpv.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
            else:
                h1_l1pt_lowpv.Fill(l1p4.Pt(),weight)
                h1_l1eta_lowpv.Fill(l1p4.Eta(),weight)
                h1_l2pt_lowpv.Fill(l2p4.Pt(),weight)
                h1_l2eta_lowpv.Fill(l2p4.Eta(),weight)
                
                h2_l1pteta_lowpv.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_lowpv.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_lowpv.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_lowpv.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
           if (met > 150):
                h1_l1pt_highMET.Fill(l1p4.Pt(),weight)
                h1_l1eta_highMET.Fill(l1p4.Eta(),weight)
                h1_l2pt_highMET.Fill(l2p4.Pt(),weight)
                h1_l2eta_highMET.Fill(l2p4.Eta(),weight)
              
                h2_l1pteta_highMET.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_highMET.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_highMET.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_highMET.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)
            else:
                h1_l1pt_lowMET.Fill(l1p4.Pt(),weight)
                h1_l1eta_lowMET.Fill(l1p4.Eta(),weight)
                h1_l2pt_lowMET.Fill(l2p4.Pt(),weight)
                h1_l2eta_lowMET.Fill(l2p4.Eta(),weight)
                
                h2_l1pteta_lowMET.Fill(l1p4.Pt(),abs(l1p4.Eta()),weight)
                h2_l2pteta_lowMET.Fill(l2p4.Pt(),abs(l2p4.Eta()),weight)
                h2_l1l2pt_lowMET.Fill(l1p4.Pt(),l2p4.Pt(),weight)
                h2_l1l2eta_lowMET.Fill(abs(l1p4.Eta()),abs(l2p4.Eta()),weight)

'''
eff_for_lepcommand='''
Eff_{0}{1}{2}{3} = TEfficiency(h1_{0}{1}{2}{3}, h1_pre_{0}{1}{2}{3})
Eff_{0}{1}{2}{3}.SetTitle('Eff {0}{1}{2}{3}')
Eff_{0}{1}{2}{3}.Write()
h2_{0}{1}{2}{3}.Divide(h2_pre_{0}{1}{2}{3})
'''
eff_for_objcommand='''
Eff_{0}=TEfficiency(h1_{0}, h1_pre_{0})
Eff_{0}.SetTitle('Eff {0}')
Eff_{0}.Write()
'''
