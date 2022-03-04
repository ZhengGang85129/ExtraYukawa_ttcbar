import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
import Drell_Yan.DY_utils as utils
import Drell_Yan.DY_Analyzer as DY
import time

Get_SF ='''
#include "TH2D.h"
#include "TFile.h"
float trigger_sf(TH2D * h_l1pteta, TH2D * h_l2pteta, float l1_pt, float l2_pt, float l1_eta , float l2_eta){{

    if (l1_pt >500){{
        l1_pt = 499.;
    }}
    if (l2_pt >500){{
        l2_pt = 499.;
    }}
    float sf_l1 = h_l1pteta->GetBinContent(h_l1pteta->FindBin(l1_pt,fabs(l1_eta)));
    float sf_l2 = h_l2pteta->GetBinContent(h_l2pteta->FindBin(l2_pt,fabs(l2_eta)));

    return sf_l1 * sf_l2;
}}
'''
ROOT.gInterpreter.Declare(Get_SF)
start = time.time()
DY.Analyzer(channel='DoubleElectron')
#DY.Analyzer(channel='DoubleMuon')
#DY.Analyzer(channel='ElectronMuon')

