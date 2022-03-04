import os,sys,json
import ROOT
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)


def get_NumberOfEvent(filename:str) -> int:
    ftemp = ROOT.TFile.Open(filename)
    htemp = ftemp.Get('nEventsGenWeighted')
    return  htemp.GetBinContent(1)

def MakeDir(Root:str,ChildName:str):

    if not os.path.isdir(Root):
        raise ValueError(f'No such Root Directory: {Root}!')
    else:
        DIR = os.path.join(Root,ChildName)
    if os.path.isdir(DIR):
        print(DIR + ' exist')
    else:
        print('Create '+ DIR)
        os.mkdir(DIR)

def Trigger(df:ROOT.RDataFrame,Trigger_condition:str) -> ROOT.RDataFrame.Filter:
    '''
    Trigger_conidtion -> Trigger For Leptons
    return dataframe with triggered condition
    '''
    return df.Filter(Trigger_condition)

def Trig_Cond(flag:str,joint:str) -> str:
    '''
    Return Trig_Condition
    '''
    return joint.join(flag)


