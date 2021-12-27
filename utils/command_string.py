h1command ='''
global h1_{0}{1}{2}{3}{4}
h1_{0}{1}{2}{3}{4} = TH1F("{0}{1}{2}{3}{4}","{0}{1}{2}{3}{4}",len({5})-{6},{7})
h1_{0}{1}{2}{3}{4}.Sumw2()
h1_{0}{1}{2}{3}{4}.SetMinimum(0)
h1_{0}{1}{2}{3}{4}.GetXaxis().SetTitle('{8}')
h1_{0}{1}{2}{3}{4}.GetYaxis().SetTitle('Efficiency')
h1_{0}{1}{2}{3}{4}.SetStats(0)
'''
del_h1command='''h1_{0}{1}{2}{3}{4} = None'''
