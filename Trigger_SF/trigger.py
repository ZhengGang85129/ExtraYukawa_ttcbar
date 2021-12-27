import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.listoutdata2txt as d2t
import utils.trigger_utils as trig_tool 

dir_list = ['./data','./data/trigger_data','./data/datalist']
path_nano = '/eos/user/m/melu/TTC_Nanov8_new'

datalistname = './data/datalist/triggerinput.txt'

def main(create_structure=True):
    if create_structure:
        for d in dir_list:
            if os.path.isdir(d):
                print('Directory: {} exists!'.format(d))
            else:
                print('Directory: {} created!'.format(d))
                os.mkdir(d)
        d2t.generatefile(datalistname='./data/datalist/triggerinput.txt',patterns=['MET.root','TTTo2L*.root','TTTo1L*.root'],path_to_data=path_nano)
    with open(datalistname,'r') as f:
        for idx,filename in enumerate(f.readlines()):
            if idx == 1:
                trig_tool.trigger_calc(filename=filename[:-1],outdir='./data/trigger_data')

main(False)
