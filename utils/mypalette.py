from ROOT import gStyle, TColor,gROOT,TStyle
import ROOT
from array import array
def colorPalette():
    NRGBs = 5
    NCont = 256
    stops = [0.00,0.30,0.61,0.84,1.00]
    red = [0.00,0.00,0.57,0.90,0.51]
    green = [0.00,0.65,0.95,0.20,0.00]
    blue = [ 0.51,0.55,0.15,0.00,0.10]
    stopsArray = array('d',stops)
    redArray = array('d',red)
    greenArray = array('d',green)
    blueArray = array('d',blue)
    TColor.CreateGradientColorTable(NRGBs,stopsArray,redArray,greenArray,blueArray,NCont)
    gStyle.SetNumberContours(NCont)
