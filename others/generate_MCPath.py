import os 
import json
data_dir = '/eos/user/m/melu/TTC_Nanov8_new'

Dileptons_types = ['DoubleMuon','SingleMuon','DoubleElectron','SingleElectron','ElectronMuon']


data_path = dict()
data_path['Data'] = dict()
data_path['MC'] = dict()

for Dileptons_type in  Dileptons_types:
    data_path['Data'][Dileptons_type] =dict()

data_path['Data']['DoubleMuon'] = [os.path.join(data_dir,'DoubleMuon' + postfix + '.root') for postfix in ['B','C','D','E','F']]
data_path['Data']['SingleMuon'] = [os.path.join(data_dir,'SingleMuon' + postfix + '.root') for postfix in ['B','C','D','E','F']]
data_path['Data']['DoubleElectron'] = [os.path.join(data_dir,'DoubleEG' + postfix + '.root') for postfix in ['B','C','D','E','F'] ]
data_path['Data']['SingleElectron'] = [os.path.join(data_dir,'SingleEG' + postfix + '.root') for postfix in ['B','C','D','E','F']]
data_path['Data']['ElectronMuon'] = [os.path.join(data_dir,'MuonEG' + postfix + '.root' ) for postfix in ['B','C','D','E','F'] ]

print(data_path['Data']['ElectronMuon'])

MCname_list = ['DY','WJets','WW','WZ','ZZ','WWW','WWZ','WZZ','ZZZ','tsch','t_tch','tbar_tch','tW','tbarW','ttWtoLNu','ttWtoQQ','ttZ','ttZtoQQ','ttH','ttWW','ttWZ','ttZZ','tzq','TTTo2L','TTTo1L']

for MCname in MCname_list:
    data_path['MC'][MCname] = os.path.join(data_dir,MCname+'.root')

with open('./data/datalist/2017/input.json','wt') as f:
    json.dump(data_path,f)

