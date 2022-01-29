import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.program_step as step
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s','--sources',help='path of nano file sources',type=str,default='/eos/user/m/melu/TTC_Nanov8_new')
parser.add_argument('-m','--mode',help='Program Modes',choices=['Init','Trig_Calc','Eff_Plot','SF_Calc'],type=str)



#infilepatterns = ['MET.root','TTTo2L*.root','TTTo1L*.root']
infilepatterns = ['MET.root','TTTo2L*.root']
args = parser.parse_args()
channels = ['DoubleElectron']

if args.mode == 'Init':
    arguments = {
        'infilepatterns': infilepatterns,
        'source': args.sources
    }
    
    step.create_structure(arguments)
elif args.mode =='Trig_Calc':

    step.Trig_Calc(channels=channels)

elif args.mode == 'Eff_Plot':
    step.Plot_efficiency(channels=channels)

elif args.mode == 'SF_Calc':
    settings = dict()
    settings['channel'] = channels[0]
    step.SF_Calc(**settings)
else:
    pass
