import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.listoutdata2txt as d2t
import utils.trigger_utils as trig_tool 
import argparse
import utils.multipleprocess as mp

parser = argparse.ArgumentParser()

parser.add_argument('-c','--create',help='Create Directary for storing histogram files if specify.',action='store_true')
parser.add_argument('-s','--sources',help='path of nano file sources',type=str,default='/eos/user/m/melu/TTC_Nanov8_new')
args = parser.parse_args()


def trigger_store(create_structure=True,src=''):
    dir_list = ['./data','./data/trigger_data','./data/datalist']
    datalistname = './data/datalist/triggerinput.txt'
    if create_structure:
        for d in dir_list:
            if os.path.isdir(d):
                print('Directory: {} exists!'.format(d))
            else:
                print('Directory: {} created!'.format(d))
                os.mkdir(d)
        d2t.generatefile(datalistname,patterns=['MET.root','TTTo2L*.root','TTTo1L*.root'],path_to_data=src)
    else:
        with open(datalistname,'r') as f:
            for idx,filename in enumerate(f.readlines()):
                MP = mp.multiprocess()
                for channel in ['ee','em','mm']:
                    MP.register(trig_tool.trigger_calc,process_args=[filename[:-1],'./data/trigger_data',channel])
                MP.run()

trigger_store(args.create,args.sources)
