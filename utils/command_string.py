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

