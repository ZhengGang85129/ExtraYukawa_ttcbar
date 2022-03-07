import fnmatch
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
from array import array
import Utils.CMSTDRStyle as CMSTDRStyle
import Utils.CMSstyle as CMSstyle
import Utils.mypalette as mypalette
import json
from Trigger_SF.Trig_DataFrame import *
import Trigger_SF.Trigger_Utils as TrigUtils
from Utils.General_Tool import *
import Utils.plot_settings as plt_set

def Trig_Calc(year:str,channel:str,Type:str,nevents:int):
    if year is None:
        raise ValueError('Arguments [year] must be speicified.')
    with open(f'./data/year{year}/configuration/HLTTrigger.json','rb') as f:
        HLT_Path = json.load(f)
    with open(f'./data/year{year}/configuration/name.json','rb') as f :
        Var_Name = json.load(f)
    with open(f'./data/year{year}/configuration/flag.json','rb') as f :
        Flag = json.load(f)

    with open(f'./data/year{year}/path/filein.json','rb') as f:
        FileIn = json.load(f)

    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    
    with open(f'./data/year{year}/path/LeptonsID_SF.json','rb') as f:
        LepSF_File = json.load(f)[channel]

    setting={
        'HLT_MET': HLT_Path['MET'],
        'HLT_LEP': HLT_Path[channel],
        'Var_Name' : Var_Name[channel],
        'channel' : channel,
        'DirOut' : User['DirOut'][channel]['files'],
        'FileIn' : FileIn[Type],
        'Flag':Flag,
        'Type':Type,
        'LepSF_File':LepSF_File,
        'Year':'year'+year,
        'nevents':nevents
    }
    A = TrigRDataFrame(setting)
    A.Run()


def Plot_efficiency(channel:str,year:str):
    '''
    plot Trigger histograms to visualize what's in root file respectively.
    '''
    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    user_settings={
            'channel':channel,
            'DirIn':User['DirOut'][channel]['files'],
            'DirOut':User['DirOut'][channel]['plots'],
            'colors' : {'Data':1,'MC':4}
            }
    tags = {
            'l1':{
                'pt':['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_highpv','l1pt_lowpv','l1pt_highmet','l1pt_lowmet'] ,
                'eta':['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_highpv','l1eta_lowpv','l1eta_highmet','l1eta_lowmet'],
                'pteta':['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_highpv','l1pteta_lowpv','l1pteta_highmet','l1pteta_lowmet']
            },
            'l2':{
                'pt':['l2pt','l2pt_highjet','l2pt_lowjet','l2pt_highpv','l2pt_lowpv','l2pt_highmet','l2pt_lowmet'] ,
                'eta':['l2eta','l2eta_highjet','l2eta_lowjet','l2eta_highpv','l2eta_lowpv','l2eta_highmet','l2eta_lowmet'],
                'pteta':['l2pteta','l2pteta_highjet','l2pteta_lowjet','l2pteta_highpv','l2pteta_lowpv','l2pteta_highmet','l2pteta_lowmet']
            },
        }

    print('Plotting 1D histograms for channel :{}'.format(channel))
    
    user_settings['Type'] = 'Trigger Efficiency 1D Histogram'
    for tag in  tags['l1']['pt']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l1']['eta']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pt']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['eta']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    
    print('Plotting 2D histograms for channel :{}'.format(channel))
    user_settings['Type'] = 'Trigger Efficiency 2D Histogram'
    for tag in  tags['l1']['pteta']:
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pteta']:
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['pt']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['eta']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)

def SF_Calc(channel:str,year:str):
    '''
    MC -> TTTo2L
    data -> MET
    '''
    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    settings={
            'channel':channel,
            'DirIn':User['DirOut'][channel]['files'],
            'DirOut':User['DirOut'][channel]['plots'],
            }
    
    nominal_names =['l1pteta','l2pteta']

    
    print('Producing TriggerSF...')
    for nominal_name in nominal_names:
        TrigUtils.ScaleFactors(nominal_name,**settings)
    

