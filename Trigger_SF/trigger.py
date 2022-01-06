import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.trigger_utils as trig_tool 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s','--sources',help='path of nano file sources',type=str,default='/eos/user/m/melu/TTC_Nanov8_new')
parser.add_argument('-m','--mode',help='Program Modes',choices=['Init','Prod','Plot'],type=str)

args = parser.parse_args()

if args.mode == 'Init':
    trig_tool.trigger_store(True)
elif args.mode =='Prod':
    trig_tool.trigger_store(False,args.sources)
elif args.mode == 'Plot':
    print('Plot Hisogram')
