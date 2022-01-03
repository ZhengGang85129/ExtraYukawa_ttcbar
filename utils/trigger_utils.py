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

def trigger_calc(filename,outdir,channel = 'ee'):
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
    
    outfilenames = os.path.join(outdir,file_basename+'_'+channel+'.root')
    
    production = analyzer.analyzer(infilename=filename,outfilename=outfilenames,channel=channel)
    production.selection()
    

