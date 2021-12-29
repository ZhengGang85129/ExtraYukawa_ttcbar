h1_lepcommand ='''
self.h1_{0}{1}{2}{3}{4} = TH1F("{0}{1}{2}{3}{4}","{0}{1}{2}{3}{4}",len(self.{5})-{6},self.{7})
self.h1_{0}{1}{2}{3}{4}.Sumw2()
self.h1_{0}{1}{2}{3}{4}.SetMinimum(0)
self.h1_{0}{1}{2}{3}{4}.GetXaxis().SetTitle('{8}')
self.h1_{0}{1}{2}{3}{4}.GetYaxis().SetTitle('Efficiency')
self.h1_{0}{1}{2}{3}{4}.SetStats(0)'''

del_h1_lepcommand='''self.h1_{0}{1}{2}{3}{4} = None'''

h1_njetcommand ='''
self.h1_{0}njet{1}{2}= TH1F("{0}njet{1}{2}","{0}njet{1}{2}",len(self.jetbin)-1,self.jetbin)
self.h1_{0}njet{1}{2}.Sumw2()
self.h1_{0}njet{1}{2}.SetMinimum(0)
self.h1_{0}njet{1}{2}.GetXaxis().SetTitle('{3}')
self.h1_{0}njet{1}{2}.GetYaxis().SetTitle('Efficiency')
self.h1_{0}njet{1}{2}.SetStats(0)'''

del_h1_njetcommand='''self.h1_{0}njet{1}{2} = None'''

h1_metcommand ='''
self.h1_{0}met{1}{2}= TH1F("{0}met{1}{2}","{0}met{1}{2}",len(self.metbin)-1,self.metbin)
self.h1_{0}met{1}{2}.Sumw2()
self.h1_{0}met{1}{2}.SetMinimum(0)
self.h1_{0}met{1}{2}.GetXaxis().SetTitle('{3}')
self.h1_{0}met{1}{2}.GetYaxis().SetTitle('Efficiency')
self.h1_{0}met{1}{2}.SetStats(0)'''

del_h1_metcommand='''self.h1_{0}met{1}{2} = None'''

h1_pucommand ='''
self.h1_{0}pu{1}= TH1F("{0}pu{1}","{0}pu{1}",40,0,80)
self.h1_{0}pu{1}.Sumw2()
self.h1_{0}pu{1}.SetMinimum(0)
self.h1_{0}pu{1}.SetStats(0)'''

del_h1_pucommand='''self.h1_{0}pu{1} = None'''

h2_lepcommand='''
self.h2_{0}{1}pteta{2}{3}= TH2D("{0}{1}pteta{2}{3}","{0}{1}pteta{2}{3}",6,self.tdl1ptbin,4,self.tdlepetabin)
self.h2_{0}{1}pteta{2}{3}.Sumw2()
self.h2_{0}{1}pteta{2}{3}.SetStats(0)
self.h2_{0}{1}pteta{2}{3}.GetXaxis().SetTitle('{4}')
self.h2_{0}{1}pteta{2}{3}.GetYaxis().SetTitle('{5}')
self.h2_{0}{1}pteta{2}{3}.SetStats(0)'''

del_h2_lepcommand='''self.h2_{0}{1}pteta{2}{3} = None'''

h2_2lepcommand='''
self.h2_{0}l1l2{1}{2}{3}= TH2D("{0}l1l2{1}{2}{3}","{0}l1l2{1}{2}{3}",{4},{5},{6},{7})
self.h2_{0}l1l2{1}{2}{3}.Sumw2()
self.h2_{0}l1l2{1}{2}{3}.SetStats(0)
self.h2_{0}l1l2{1}{2}{3}.GetXaxis().SetTitle('{8}')
self.h2_{0}l1l2{1}{2}{3}.GetYaxis().SetTitle('{9}')
self.h2_{0}l1l2{1}{2}{3}.SetStats(0)'''

del_h2_2lepcommand='''self.h2_{0}l1l2{1}{2}{3} = None'''

fill_histocommand='''
self.all_events1 = TH1F('all_events1','lep_tag',1,0,1)
self.all_events2 = TH1F('all_events2','met_tag',1,0,1)
self.all_events3 = TH1F('all_events3','lepmet_tag',1,0,1)
self.pass_lep_trigger= TH1F('pass_lep_trigger','pass_lep_trigger',1,0,1)
self.pass_met_trigger= TH1F('pass_met_trigger','pass_met_trigger',1,0,1)
self.pass_lepmet_trigger= TH1F('pass_lepmet_trigger','pass_lepmet_trigger',1,0,1)
for ientry in range(0,200000):
    self.tree.GetEntry(ientry)
    if 'TT' in self.infilename:
        met = self.tree.MET_T1Smear_pt
    else:
        met =  self.tree.MET_T1_pt
    if ientry%10000 ==0: print('processing :' +str(ientry))
    if not (self.tree.Flag_goodVertices and self.tree.Flag_globalSuperTightHalo2016Filter and self.tree.Flag_HBHENoiseFilter and self.tree.Flag_HBHENoiseIsoFilter and self.tree.Flag_EcalDeadCellTriggerPrimitiveFilter and self.tree.Flag_BadPFMuonFilter and self.tree.Flag_eeBadScFilter and self.tree.Flag_ecalBadCalibFilter):
        
        if not (self.tree.DY_region == {0} or self.tree.ttc_region == {0}):continue
        if self.tree.DY_region == {0}:
            self.l1p4.SetPtEtaPhiM(self.tree.{1},self.tree.{2},self.tree.{3},self.tree.{4})
            self.l2p4.SetPtEtaPhiM(self.tree.{5},self.tree.{6},self.tree.{7},self.tree.{8})        
            if 'TT' in self.infilename:
                weight = {9} * self.tree.puWeight * self.tree.PrefireWeight
            else:
                weight =1.
        if self.tree.ttc_region == {0}:
            self.l1p4.SetPtEtaPhiM(self.tree.{10},self.tree.{11},self.tree.{12},self.tree.{13})
            self.l2p4.SetPtEtaPhiM(self.tree.{14},self.tree.{15},self.tree.{16},self.tree.{17} )        
            if 'TT' in self.infilename:
                weight = {18} * self.tree.puWeight * self.tree.PrefireWeight
            else:
                weight =1.

        if (self.l1p4+self.l2p4).M() < 20:
            continue
        if not(self.l1p4.Pt() >30 or self.l2p4.Pt() >30):
            continue
        if (self.l1p4.DeltaR(self.l2p4)<0.3):continue
        if met <100:continue

        self.all_events1.Fill(0.5,weight)
        self.all_events2.Fill(0.5,weight)
        self.all_events3.Fill(0.5,weight)
        if({19}):
            self.pass_lep_trigger.Fill(0.5,weight)
        if({20}):
            self.pass_met_trigger.Fill(0.5,weight)
            self.h1_pre_l1pt.Fill(self.l1p4.Pt(),weight)
            self.h1_pre_l1eta.Fill(self.l1p4.Eta(),weight)
            self.h1_pre_l2pt.Fill(self.l2p4.Pt(),weight)
            self.h1_pre_l2eta.Fill(self.l2p4.Eta(),weight)
            self.h1_pre_njet.Fill(self.tree.n_tight_jet,weight)
            self.h1_pre_met.Fill(met,weight)
            self.h2_pre_l1pteta.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
            self.h2_pre_l2pteta.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
            self.h2_pre_l1l2pt.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
            self.h2_pre_l1l2eta.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            if self.tree.n_tight_jet > 3 :
                self.h1_pre_l1pt_highjet.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_highjet.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_highjet.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_highjet.Fill(self.l2p4.Eta(),weight)

                self.h2_pre_l1pteta_highjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_highjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_highjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_highjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            else:
                self.h1_pre_l1pt_lowjet.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_lowjet.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_lowjet.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_lowjet.Fill(self.l2p4.Eta(),weight)
                
                self.h2_pre_l1pteta_lowjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_lowjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_lowjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_lowjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            if (self.tree.PV_npvs) > 30:
                self.h1_pre_l1pt_highpv.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_highpv.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_highpv.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_highpv.Fill(self.l2p4.Eta(),weight)
                
                self.h2_pre_l1pteta_highpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_highpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_highpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_highpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            else:
                self.h1_pre_l1pt_lowpv.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_lowpv.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_lowpv.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_lowpv.Fill(self.l2p4.Eta(),weight)
                
                self.h2_pre_l1pteta_lowpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_lowpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_lowpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_lowpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            if met > 150:
                self.h1_pre_l1pt_highMET.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_highMET.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_highMET.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_highMET.Fill(self.l2p4.Eta(),weight)
                
                self.h2_pre_l1pteta_highMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_highMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_highMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_highMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            else:
                self.h1_pre_l1pt_lowMET.Fill(self.l1p4.Pt(),weight)
                self.h1_pre_l1eta_lowMET.Fill(self.l1p4.Eta(),weight)
                self.h1_pre_l2pt_lowMET.Fill(self.l2p4.Pt(),weight)
                self.h1_pre_l2eta_lowMET.Fill(self.l2p4.Eta(),weight)
                
                self.h2_pre_l1pteta_lowMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_pre_l2pteta_lowMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_pre_l1l2pt_lowMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_pre_l1l2eta_lowMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
            
            if({19}):
                self.pass_lepmet_trigger.Fill(0.5,weight)
                self.h1_l1pt.Fill(self.l1p4.Pt(),weight)
                self.h1_l1eta.Fill(self.l1p4.Eta(),weight)
                self.h1_l2pt.Fill(self.l2p4.Pt(),weight)
                self.h1_l2eta.Fill(self.l2p4.Eta(),weight)
                self.h1_njet.Fill(self.tree.n_tight_jet,weight)
                self.h1_met.Fill(met,weight)
                self.h2_l1pteta.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                self.h2_l2pteta.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                self.h2_l1l2pt.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                self.h2_l1l2eta.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                if self.tree.n_tight_jet > 3 :
                    self.h1_l1pt_highjet.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_highjet.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_highjet.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_highjet.Fill(self.l2p4.Eta(),weight)

                    self.h2_l1pteta_highjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_highjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_highjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_highjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                else:
                    self.h1_l1pt_lowjet.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_lowjet.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_lowjet.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_lowjet.Fill(self.l2p4.Eta(),weight)
                    
                    self.h2_l1pteta_lowjet.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_lowjet.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_lowjet.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_lowjet.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                if (self.tree.PV_npvs) > 30:
                    self.h1_l1pt_highpv.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_highpv.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_highpv.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_highpv.Fill(self.l2p4.Eta(),weight)
                    
                    self.h2_l1pteta_highpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_highpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_highpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_highpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                else:
                    self.h1_l1pt_lowpv.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_lowpv.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_lowpv.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_lowpv.Fill(self.l2p4.Eta(),weight)
                    
                    self.h2_l1pteta_lowpv.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_lowpv.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_lowpv.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_lowpv.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                if met > 150:
                    self.h1_l1pt_highMET.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_highMET.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_highMET.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_highMET.Fill(self.l2p4.Eta(),weight)
                  
                    self.h2_l1pteta_highMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_highMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_highMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_highMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)
                else:
                    self.h1_l1pt_lowMET.Fill(self.l1p4.Pt(),weight)
                    self.h1_l1eta_lowMET.Fill(self.l1p4.Eta(),weight)
                    self.h1_l2pt_lowMET.Fill(self.l2p4.Pt(),weight)
                    self.h1_l2eta_lowMET.Fill(self.l2p4.Eta(),weight)
                    
                    self.h2_l1pteta_lowMET.Fill(self.l1p4.Pt(),abs(self.l1p4.Eta()),weight)
                    self.h2_l2pteta_lowMET.Fill(self.l2p4.Pt(),abs(self.l2p4.Eta()),weight)
                    self.h2_l1l2pt_lowMET.Fill(self.l1p4.Pt(),self.l2p4.Pt(),weight)
                    self.h2_l1l2eta_lowMET.Fill(abs(self.l1p4.Eta()),abs(self.l2p4.Eta()),weight)

#build efficiency for object
for obj in ['njet','met']:
    exec(cmd_str.eff_for_objcommand.format(obj))
#build effiency plot for lepton
for lep,observable,condition,obj in product(['l1','l2'],['pt','eta'],['','_low','_high'],['','jet','pv','MET']):
    if condition == '' and obj !='':continue
    if condition !='' and obj == '': continue
    exec(cmd_str.eff_for_lepcommand.format(lep,observable,condition,obj))

##Variable histogram


print('Single Leption Observables Calculating...')
for lep,condition,obj in product(['l1','l2'],['','_low','_high'],['','jet','pv','MET']):
    if condition =='' and obj != '': continue
    if condition !='' and obj == '': continue
    exec(cmd_str.h2_divide_lepcommand.format(lep,condition,obj))

print('DiLeptions Observables Calculating...')
for obv,condition,obj in product(['pt','eta'],['','_low','_high'],['','jet','pv','MET']):
    if condition =='' and obj != '': continue
    if condition !='' and obj == '': continue
    exec(cmd_str.h2_divide_2lepcommand.format(obv,condition,obj))

##Efficiency Calculating
print('Calculating Trigger Efficiency ...')
for obj,x in zip(['lep','met','lepmet'],[2,1,3]):
    exec(cmd_str.eff_for_trigcommand.format(obj,x))

alpha=(lepeff*meteff)/lepmeteff
alphaerr= sqrt(lepeff_err*lepeff_err*meteff*meteff + lepeff*lepeff*meteff_err*meteff_err + lepeff*lepeff*meteff*meteff*lepmeteff_err*lepmeteff_err/(lepmeteff*lepmeteff))/lepmeteff
print('alpha:{0} +- {1}'.format( alpha,alphaerr))

self.outfile.cd()

#Histogram Write
for obj in ['lepmettrigger','leptrigger','mettrigger','njet','met']: 
    exec(cmd_str.eff_trig_write_command.format(obj))

for lep , obv, condition,obj in product(['l1','l2'],['pt','eta'],['','_low','_high'],['','jet','pv','MET']):
    if condition =='' and obj != '': continue
    if condition !='' and obj == '': continue
    exec(cmd_str.eff_lep_write_command.format(lep,obv,condition,obj))

for obv , condition ,obj in product(['eta','pt'],['','_low','_high'],['','jet','pv','MET']):
    if condition =='' and obj != '': continue
    if condition !='' and obj == '': continue
    exec(cmd_str.h2_2leps_write_command.format(obv,condition,obj))

for lep , condition,obj in product(['l1','l2'],['','_low','_high'],['','jet','pv','MET']):
    if condition =='' and obj != '': continue
    if condition !='' and obj == '': continue
    exec(cmd_str.h2_lep_write_command.format(lep,condition,obj))
self.outfile.Close()
'''

eff_for_lepcommand='''
Eff_{0}{1}{2}{3} = TEfficiency(self.h1_{0}{1}{2}{3}, self.h1_pre_{0}{1}{2}{3})
Eff_{0}{1}{2}{3}.SetTitle('Eff {0}{1}{2}{3}')
Eff_{0}{1}{2}{3}.Write()'''

eff_for_objcommand='''
Eff_{0}=TEfficiency(self.h1_{0}, self.h1_pre_{0})
Eff_{0}.SetTitle('Eff {0}')
Eff_{0}.Write()'''

eff_for_trigcommand='''
Eff_{0}trigger=TEfficiency(self.pass_{0}_trigger, self.all_events{1})
{0}eff=Eff_{0}trigger.GetEfficiency(1)
{0}eff_err=max(Eff_{0}trigger.GetEfficiencyErrorUp(1), Eff_{0}trigger.GetEfficiencyErrorLow(1))
print('{0} trigger eff:'+str({0}eff)+'+-'+str({0}eff_err))'''

h2_divide_lepcommand='''self.h2_{0}pteta{1}{2}.Divide(self.h2_pre_{0}pteta{1}{2})'''

h2_divide_2lepcommand='''self.h2_l1l2{0}{1}{2}.Divide(self.h2_pre_l1l2{0}{1}{2})'''

eff_trig_write_command ='''Eff_{0}.Write()'''

eff_lep_write_command ='''Eff_{0}{1}{2}{3}.Write()'''

h2_2leps_write_command ='''self.h2_l1l2{0}{1}{2}.Write()'''

h2_lep_write_command ='''self.h2_{0}pteta{1}{2}.Write()'''

