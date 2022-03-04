import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from utils.DY_utils import Define_Hists, overunder_flowbin,Plot, MyDataFrame, Filtering
import utils.DY_utils as DY_utils
from Drell_Yan.DY_HistogramSetting import HistSettings
import multiprocessing
from multiprocessing import Queue, Process, Manager, Pool
from collections import OrderedDict

def Analyzer(channel='DoubleElectron'):
    ROOT.gInterpreter.Declare(Define_Hists.format(channel))
    ROOT.ROOT.EnableImplicitMT(multiprocessing.cpu_count())
    NumberOfMCEvents = dict()
    histos = OrderedDict()
    histos['MC'] = OrderedDict()
    histos['Data'] = OrderedDict()
    data_name = list()


    #Trigger Condition
    with open('./data/HLT_2017/Trigger.json','rb') as f:
        Trigger = json.load(f)
    
    #Paths to MC or Data.
    with open('./data/datalist/2017/input.json' , 'rb') as f:
        Files_Paths = json.load(f)
    
    #Cross_Section and Number of Events for MC data
    with open('./data/datalist/2017/data_xs.json','rb') as f:
        Event = json.load(f)
    with open('./data/datalist/2017/name.json','rb') as f:
        lepton_weight = json.load(f)[channel]['weight']
    
    cross_section = Event['xs']
    numberOfEvents = Event['NumberOfEvents']
    lumi = Event['xs']['lumi']
    
    dfs = OrderedDict()
    dfs['MC'] = OrderedDict()
    dfs['Data'] = OrderedDict()
   
    for MC in Files_Paths['MC'].keys():
        settings ={
                'channel': channel,
                'Data' : False,
                'Trigger_Condition': Trigger['All'],
                'weight' : lepton_weight,
                'File_Paths' : Files_Paths['MC'][MC],
                }
        dfs['MC'][MC]= MyDataFrame(settings)
    
    
    for dilepton_type in Trigger[channel].keys():
        settings = {
                'channel': channel,
                'Trigger_Condition' : Trigger[channel][dilepton_type],
                'weight' : None,
                'Data': True,
                'File_Paths' : Files_Paths['Data'][dilepton_type],
                }
        dfs['Data'][dilepton_type]= MyDataFrame(settings)

    for MC in Files_Paths['MC'].keys():
        Filtering(dfs['MC'][MC],HistSettings)
    
    for dilepton_type in Trigger[channel].keys():
        Filtering(dfs['Data'][ dilepton_type] , HistSettings)


    for histname in HistSettings.keys():
        HistoGrams = OrderedDict()
        HistoGrams['MC'] = OrderedDict()
        Temps = OrderedDict()
        Temps['Data'] = OrderedDict()
        Temps['MC'] = OrderedDict()
        for MC in dfs['MC'].keys():
            h = dfs['MC'][MC].Hists[histname].GetValue()
            h.Scale(cross_section[MC]/float(numberOfEvents[MC]))
            Temps['MC'][MC] = overunder_flowbin(h)
        for idx ,Data in enumerate(dfs['Data'].keys()):
            h= dfs['Data'][Data].Hists[histname].GetValue()
            h = overunder_flowbin(h)
            Temps['Data'][Data] = overunder_flowbin(h)
            if idx == 0:
                HistoGrams['Data'] = Temps['Data'][Data]
            else:
                HistoGrams['Data'].Add(Temps['Data'][Data])

        ####
        HistoGrams['MC']['DY'] = Temps['MC']['DY']
        HistoGrams['MC']['WJets'] = Temps['MC']['WJets']
        
        HistoGrams['MC']['VV'] = Temps['MC']['WW']
        HistoGrams['MC']['VV'].Add(Temps['MC']['WZ'])
        HistoGrams['MC']['VV'].Add(Temps['MC']['ZZ'])
        
        HistoGrams['MC']['VVV'] = Temps['MC']['WWW']
        HistoGrams['MC']['VVV'].Add(Temps['MC']['WWZ'])
        HistoGrams['MC']['VVV'].Add(Temps['MC']['WZZ'])
        HistoGrams['MC']['VVV'].Add(Temps['MC']['ZZZ'])
        
        HistoGrams['MC']['SingleTop'] = Temps['MC']['tsch']
        HistoGrams['MC']['SingleTop'].Add(Temps['MC']['t_tch'])
        HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbar_tch'])
        HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tW'])
        HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbarW'])

        HistoGrams['MC']['ttXorXX'] = Temps['MC']['ttWtoLNu']
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWtoQQ'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZ'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZtoQQ'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttH'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWW'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWZ'])
        HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZZ'])
   
        HistoGrams['MC']['tzq'] = Temps['MC']['tzq']

        HistoGrams['MC']['TT'] = Temps['MC']['TTTo1L']
        HistoGrams['MC']['TT'].Add(Temps['MC']['TTTo2L'])

        Plot(HistoGrams,x_name=histname ,lumi=lumi,channel=channel)
