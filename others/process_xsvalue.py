import json
import os,sys
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from utils.DY_utils import get_NumberOfEvent


Event =dict()
Event['xs'] = dict()
Event['NumberOfEvents'] = dict()

Event['xs']['lumi'] = 41480.
Event['xs']['DY'] = 6077.22
Event['xs']['WJets'] = 61526.7
Event['xs']['WW'] = 118.7
Event['xs']['WZ'] = 65.5443
Event['xs']['ZZ'] = 15.8274
Event['xs']['WWW'] = 0.2086
Event['xs']['WWZ'] = 0.1707
Event['xs']['WZZ'] = 0.05709
Event['xs']['ZZZ'] = 0.01476
Event['xs']['TTTo2L'] = 88.3419
Event['xs']['TTTo1L'] = 365.4574
Event['xs']['ttH'] = 0.5269
Event['xs']['ttWtoLNu']  = 0.1792
Event['xs']['ttWtoQQ'] = 0.3708
Event['xs']['ttZ'] = 0.2589
Event['xs']['ttZtoQQ'] = 0.6012
Event['xs']['ttWW'] = 0.007003
Event['xs']['ttWZ'] = 0.002453
Event['xs']['ttZZ'] = 0.001386
Event['xs']['tzq'] = 0.07561
Event['xs']['tW'] = 35.85
Event['xs']['tbarW'] = 35.85
Event['xs']['tsch'] = 3.36
Event['xs']['t_tch'] = 136.02
Event['xs']['tbar_tch'] = 80.95

with open('./data/datalist/2017/input.json' , 'rb') as f:
    MC_Paths = json.load(f)['MC']

for MC in MC_Paths.keys():
    Event['NumberOfEvents'][MC] = get_NumberOfEvent(MC_Paths[MC])

with open('./data/datalist/2017/data_xs.json','wt') as f:
    json.dump(Event,f)
