import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.program_step as step
import argparse
from utils.Build_Dir import Build_Dir



parser = argparse.ArgumentParser()
parser.add_argument('-i','--Filein',help='Text File names which contain the information of input files',type=str,default='./data/year2018/ForEfficiency/InputPath.txt')
parser.add_argument('-m','--mode',help='Program Modes',choices=['BuildDir','TrigEff_Calc','TrigEff_Plot','TrigSF_Calc'],type=str)

parser.add_argument('-y','--year',help='year',choices=['2018'],type=str)

parser.add_argument('-c','--channels',help='Channel',nargs='+',default=["DoubleElectron","DoubleMuon","ElectronMuon"])
parser.add_argument('-o','--DirOut',help="Output Directory's Parent",type=str,default='/eos/user/z/zhenggan')
parser.add_argument('-t','--Task',help="Task",type=str,default='Trigger',choices=["Trigger","DY_Reconstruction"])


#infilepatterns = ['MET.root','TTTo2L*.root','TTTo1L*.root']
infilepatterns = ['MET.root','TTTo2L*.root']
args = parser.parse_args()
#channels = ['DoubleElectron','DoubleMuon']

#channels = ['ElectronMuon','DoubleElectron','DoubleMuon']

channels = ['DoubleElectron']
if args.mode == 'BuildDir':
    Build_Dir(args) 
    
    
    #step.create_structure(arguments)




#elif args.mode =='Trig_Calc':
#    step.Trig_Calc(channels=channels)

#elif args.mode == 'Eff_Plot':
#    step.Plot_efficiency(channels=channels)

#elif args.mode == 'SF_Calc':
#    for channel in channels:
#        settings = dict()
#        settings['channel'] = channel
        
#        step.SF_Calc(**settings)
#else:
#    pass
