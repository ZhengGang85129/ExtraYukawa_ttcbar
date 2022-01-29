import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from utils.DY_utils import Get_SF, Filter, dfHist,overunder_flowbin,Plot
import utils.DY_utils as DY_utils
from Drell_Yan.DY_HistogramSetting import HistSettings
from multiprocessing import Queue, Process


def Analyzer(channel='DoubleElectron'):

    ROOT.gInterpreter.Declare(Get_SF.format('DoubleElectron'))
    NumberOfMCEvents = dict()
    histos = dict()
    histos['MC'] = dict()
    histos['Data'] = dict()
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
    
   
    #Filter For MC

    for MC in Files_Paths['MC'].keys():
        df = Filter(channel,Trigger_Condition = Trigger['All'],File_Paths = Files_Paths['MC'][MC], weight = lepton_weight , Data = False)
        histos['MC'][MC] = dfHist(df,HistSettings,Data=False)

    #dfs = dict()
    #dfs['MC'] = dict()
    #dfs['Data'] = dict()

    #dfs['MC'] = { MC : Process( target = Filter , args = (channel,Trigger['All'],Files_Paths['MC'][MC], lepton_weight , False)) for MC in Files_Paths['MC'].keys()}
    


    #print(dfs['MC'])
    #for p in dfs['MC'].keys():
    #    dfs['MC'][p].start()
    #for p in dfs['MC'].keys():
    #    dfs['MC'][p].join()

    #histos['MC'] = {MC : Process(target = dfHist, args = (dfs['MC'][MC], HistSettings, False)) for MC in Files_Paths['MC'].keys()}
    
    #for p in histos['MC'].keys():
    #    histos['MC'][p].start()
    #for p in histos['MC']:
    #    histos['MC'][p].join()


    

    #Filter For Data
    
    #dfs['Data'] = {dilepton_type: Process(target = Filter, args = (channel, Trigger[channel][dilepton_type], Files_Paths['Data'][dilepton_type],None, True)) for dilepton_type in Trigger[channel].keys()}
    
    #for p in dfs['Data'].keys():
    #    dfs['Data'][p].start()
    #for p in dfs['Data'].keys():
    #    dfs['Data'][p].join()

    #histos['Data'] = {dilepton_type: Process(target = dfHist, args=(dfs['Data'][dilepton_type] ,HistSettings,True)) for dilepton_type in Trigger[channel].keys()}
    
    #for p in histos['Data'].keys():
    #    histos['Data'][p].start()
    #for p in histos['Data'].keys():
    #    histos['Data'][p].join()
    for dilepton_type in Trigger[channel].keys():
        df = Filter(channel, Trigger_Condition = Trigger[channel][dilepton_type], File_Paths= Files_Paths['Data'][dilepton_type],weight=None, Data=True)
        histos['Data'][dilepton_type] = dfHist(df,HistSettings,Data=True)
    
    for histname in HistSettings.keys():
        HistoGrams = dict()
        HistoGrams['MC'] = dict()
        Temps = dict()
        Temps['Data'] = dict()
        Temps['MC'] = dict()
        for MC in histos['MC'].keys():
            h = histos['MC'][MC][histname].GetValue()
            h.Scale(cross_section[MC]/float(numberOfEvents[MC]))
            Temps['MC'][MC] = overunder_flowbin(h)
        for idx ,Data in enumerate(histos['Data'].keys()):
            h= histos['Data'][Data][histname].GetValue()
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

        Plot(HistoGrams,x_name=histname ,lumi=lumi)
