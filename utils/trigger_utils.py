import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import math
from math import sqrt
import importlib
from ROOT import TFile
import utils.analyzer as analyzer 

def trigger_calc(filename,outdir):
    '''
    If filename is not a path, raise an error.
    '''
    try:
        if os.path.isfile(filename):
            print('Processing {}'.format(filename))
        else: 
            raise ValueError
    except ValueError as exc:
         raise RuntimeError('No such File :{}'.format(filename)) 
    
    file_basename = os.path.basename(filename).split(".root")[0] #Take out filename from its path
    
    outfilenames = [os.path.join(outdir,file_basename+subname+'.root') for subname in ['_ee','_em','_mm']]
    
    ee_analyzer = analyzer.ee_analyzer(infilename=filename,outfilename=outfilenames[0])
    ee_analyzer.selection()
    #ee_analyzer.deactivate()
    

