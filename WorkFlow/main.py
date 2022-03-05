import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',help='Program Modes',choices=['Init','BuildDir','TrigEff_Calc','TrigEff_Plot','TrigSF_Calc'],type=str)

parser.add_argument('-y','--year',help='year',choices=['2017'],type=str)

parser.add_argument('-c','--channels',help='Channels, ex: DoubleElectron DoubleMuon',nargs='+')
parser.add_argument('-i','--channel',choices=['DoubleElectron','DoubleMuon','ElectronMuon'])
parser.add_argument('-o','--DirOut',help="Output Directory's Parent,ex: /eos/user/z/zhenggan",type=str)
parser.add_argument('-t','--task',help="Task",type=str,choices=["TriggerSF","DY_Reconstruction"])
parser.add_argument('-f','--Type',help="MC/Data",type=str,choices=["MC","Data"])


args = parser.parse_args()


if args.mode == 'Init':
    if args.year is None:
        raise ValueError('[year] should be specified, ex: python3 ./WorkFlow/main.py -y 2018')
    from Utils.Init import *
    from Utils.General_Tool import MakeDir
    RootDIR = './'
    MakeDir('./','data') 
    RootDIR = os.path.join(RootDIR,'data')
    MakeDir(RootDIR,'year{}'.format(args.year))
    RootDIR = os.path.join(RootDIR,'year{}'.format(args.year))
    MakeDir(RootDIR,'configuration')
    MakeDir(RootDIR,'path')
    
    GenPaths_HLTTrigger_File(args.year)
    GenPaths_HLTTriggerCondition_ForAnalyzer_File(args.year)
    GenTrigEffInput_File(args.year) 
    GenDataPath_File(args.year)
    GenLeptonIDSF_File(args.year)
    GenVariableNames_File(args.year)
    GenXsValue_File(args.year)
    GenGoodFlag_File(args.year)

elif args.mode == 'BuildDir':
    from Utils.Build_Dir import Build_Dir
    Build_Dir(args) 
elif args.mode == 'TrigEff_Calc':
    from Trigger_SF.Program_Step import * 
    if args.channel == None:
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list.")
    if args.Type == None:
        raise ValueError("Should Specify the type of input file(s)")

    Trig_Calc(year = args.year , channel = args.channel, Type = args.Type)
elif args.mode == 'TrigEff_Plot':
    from Trigger_SF.Program_Step import * 
    if args.channel == 'None':
        raise ValueError('You need to specify [channel]')
    if args.year == 'None':
        raise ValueError('You need to specify [year]')
    
    Plot_efficiency(channel=args.channel,year=args.year)


elif args.mode == 'TrigSF_Calc':
    from Trigger_SF.Program_Step import * 
    if args.channel == 'None':
        raise ValueError('You need to specify [channel]')
    if args.year == 'None':
        raise ValueError('You need to specify [year]')
        
    SF_Calc(channel=args.channel,year=args.year)
else:
    raise ValueError("Mode should be specified or The Specified Mode is Not in the list.")

