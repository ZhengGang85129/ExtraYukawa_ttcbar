import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
import numpy as np

from ROOT import kFALSE

import utils.CMSTDRStyle as CMSTDRStyle

import utils.CMSstyle as CMSstyle
from array import array
lumi =41480.



def draw_plots(hist_array:dict(), draw_data:bool, x_name:str, isem:int):

