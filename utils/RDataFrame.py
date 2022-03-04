import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from array import array
from ROOT import kFALSE
import numpy as np


class MyDataFrame:
    def __init__(self,settings:dict):
        '''
        self._channel -> DoubleElectron, DoubleMuon, or ElectronMuon    
        self._Trigger_Condition -> DiLeptons HLT conditions
        self._weight -> Scale Factors for Dileptons
        self._Data(bool) -> Input File(s) is(are) Data/MC
        self._filters -> Offline triggers for Dileptons
        self._File_Paths -> Paths for input Files
        
        '''
        self._channel = settings.get('channel',None)
        self._DirOut = settings.get('DirOut',None)
        self._FileIn = settings.get('FileIn',None)
        self._Type = settings.get('Type')
        if self._Type == None:
            raise ValueError('Need to Speicify Type!')
        elif self._Type == 'Data' :
            
            self._isData = 1
        else:
            self._isData = 0

        if self._channel ==None:
            raise ValueError('Need to specify Argument [channel]')
        if self._FileIn ==None:
            raise ValueError('Need to specify Argument [Filein]')
        if self._DirOut ==None:
            raise ValueError('Need to specify Argument [DirOut]')
        self._FileIn_vecstr = ROOT.std.vector('string')()
        for File in self._FileIn:
            self._FileIn_vecstr.push_back(File)


    
