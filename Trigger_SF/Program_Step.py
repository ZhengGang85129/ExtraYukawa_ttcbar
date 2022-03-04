import fnmatch
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
from ROOT import TFile, TH1F, TH2D, TCanvas, TLegend, TPad, TEfficiency
from array import array
import utils.CMSTDRStyle as CMSTDRStyle
import utils.CMSstyle as CMSstyle
import utils.mypalette as mypalette
import others.property_name as property_name
import json
from Trigger_SF.Trig_DataFrame import *
from utils.general_tool import *

def Trig_Calc(year:str,channel:str,Type:str):
    if year is None:
        raise ValueError('Arguments [year] must be speicified.')
    with open(f'./data/year{year}/configuration/HLTTrigger.json','rb') as f:
        HLT_Path = json.load(f)
    with open(f'./data/year{year}/configuration/name.json','rb') as f :
        Var_Name = json.load(f)
    with open(f'./data/year{year}/configuration/flag.json','rb') as f :
        Flag = json.load(f)

    with open(f'./data/year{year}/path/filein.json','rb') as f:
        FileIn = json.load(f)

    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    
    with open(f'./data/year{year}/path/LeptonsID_SF.json','rb') as f:
        LepSF_File = json.load(f)[channel]

    setting={
        'HLT_MET': HLT_Path['MET'],
        'HLT_LEP': HLT_Path[channel],
        'Var_Name' : Var_Name[channel],
        'channel' : channel,
        'DirOut' : User['DirOut'][channel]['files'],
        'FileIn' : FileIn[Type],
        'Flag':Flag,
        'Type':Type,
        'LepSF_File':LepSF_File,
        'Year':'year'+year
    }
    A = TrigRDataFrame(setting)
    A.Run()
    #setting['infilebasename'] = os.path.basename(setting['infilepath']).split(".root")[0]
    #setting['outfilename'] = os.path.join(setting['outputdir'],setting['infilebasename']+'_'+setting['channel']+'.root')


def Plot_efficiency(channel:str,year:str):
    '''
    plot Trigger histograms to visualize what's in root file respectively.
    '''
    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    user_settings={
            'channel':channel,
            'DirIn':User['DirOut'][channel]['files'],
            'DirOut':User['DirOut'][channel]['plots'],
            'colors' : {'Data':1,'MC':4}
            }
    tags = {
            'l1':{
                'pt':['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_highpv','l1pt_lowpv','l1pt_highmet','l1pt_lowmet'] ,
                'eta':['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_highpv','l1eta_lowpv','l1eta_highmet','l1eta_lowmet'],
                'pteta':['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_highpv','l1pteta_lowpv','l1pteta_highmet','l1pteta_lowmet']
            },
            'l2':{
                'pt':['l2pt','l2pt_highjet','l2pt_lowjet','l2pt_highpv','l2pt_lowpv','l2pt_highmet','l2pt_lowmet'] ,
                'eta':['l2eta','l2eta_highjet','l2eta_lowjet','l2eta_highpv','l2eta_lowpv','l2eta_highmet','l2eta_lowmet'],
                'pteta':['l2pteta','l2pteta_highjet','l2pteta_lowjet','l2pteta_highpv','l2pteta_lowpv','l2pteta_highmet','l2pteta_lowmet']
            },
        #    'l1l2':{
        #        'pt':['l1l2pt','l1l2pt_highjet','l1l2pt_lowjet','l1l2pt_highpv','l1l2pt_lowpv','l1l2pt_highMET','l1l2pt_lowMET'],
        #        'eta':['l1l2eta','l1l2eta_highjet','l1l2eta_lowjet','l1l2eta_highpv','l1l2eta_lowpv','l1l2eta_highMET','l1l2eta_lowMET']
        #        }
        }

    print('Plotting 1D histograms for channel :{}'.format(channel))
    
    user_settings['Type'] = 'Trigger Efficiency 1D Histogram'
    for tag in  tags['l1']['pt']:
        Plot(plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l1']['eta']:
        Plot(plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pt']:
        Plot(plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['eta']:
        Plot(plot_eff1d,**user_settings)(tag=tag)
    
    user_settings['Type'] = 'Trigger Efficiency 2D Histogram'
    for tag in  tags['l1']['pteta']:
        Plot(plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pteta']:
        Plot(plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['pt']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['eta']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)


def Plot(func,**user_settings):
    def decorator(tag):
        return func(tag=tag,**user_settings)
    return decorator


def plot_eff1d(tag:str,**settings):
    
    FileIn = {
            'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData.root'),"READ"),
                'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC.root'),"READ")
            }
    
    TS = CMSTDRStyle.setTDRStyle()
    TS.cd()
    c = TCanvas()
    c.cd()
    pad = TPad()
    pad.Draw()
    leg = TLegend(0.5,0.2,0.65,0.2+0.05*2)
    
    for Type in ['MC','Data']:
        name, Histogram = create_hist(FileIn[Type],tag)
        Histogram.SetLineColor(settings['colors'][Type])
        Histogram.SetMarkerStyle(20)
        Histogram.SetMarkerSize(0.5)
        Histogram.SetMarkerColor(settings['colors'][Type])
        gr = Histogram.CreateGraph()
        gr.SetMinimum(0.5)
        gr.SetMaximum(1.0)
        if Type =='MC':
            gr.Draw("AP")
        else:
            gr.Draw("samep")
        leg.AddEntry(Histogram,Type)
    CMSstyle.SetStyle(pad)
    leg.SetFillStyle(0)
    leg.Draw('SAME') 
    c.Update()
    c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_1D_'+tag+'.png'))
    c.Close()
    pad.Close()
    del c
    del TS
    del pad
    del leg

def create_hist(infile:TFile,tag:str):
    '''
    A lazy function to get histogram in root file.
    '''
    histoname = 'Eff_'+tag
    print(histoname)
    histotemp = infile.Get(histoname)
    histotemp.SetNameTitle(tag,"")
    
    return histoname ,histotemp

def plot_eff2d(tag:str,**settings):
    FileIn = {
            'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData.root'),"READ"),
                'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC.root'),"READ")
            }
    for Type in ['MC','Data']: 
        TS = CMSTDRStyle.setTDRStyle()
        TS.cd()
        c = TCanvas()
        pad = TPad()
        pad.Draw()
        CMSstyle.SetStyle(pad)
        histo2d = TH2D()
        histo2d = FileIn[Type].Get(tag)
        histo2d.SetNameTitle("","")
        #mypalette.colorPalette()
        histo2d.Draw('COLZ TEXT E')
        c.SetGridx(False)
        c.SetGridy(False)
        pad.SetRightMargin(0.15)
        c.Update()
        c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_2D_'+Type+'_'+tag+'.png'))
        pad.Close()
        c.Close()
        del c 
        del TS
        del pad
        del histo2d
        FileIn[Type].Close()

import numpy as np

def SF_Calc(channel:str,year:str):
    '''
    MC -> TTTo2L
    data -> MET
    '''
    with open(f'./data/year{year}/User.json','rb') as f:
        User = json.load(f)
    settings={
            'channel':channel,
            'DirIn':User['DirOut'][channel]['files'],
            'DirOut':User['DirOut'][channel]['plots'],
            }
    
    nominal_names =['l1pteta','l2pteta']

    
    print('Producing TriggerSF...')
    for nominal_name in nominal_names:
        ScaleFactors(nominal_name,**settings)
    
    
def ScaleFactors(nominal_name:str,**settings):

    '''
    Calculate ScaleFactor for a single certain nominal variable.
    '''
    
    FileIn = dict()
    FileIn['Data'] = ROOT.TFile.Open(os.path.join(settings['DirIn'],"EfficiencyForData.root"),"READ")
    FileIn['MC'] = ROOT.TFile.Open(os.path.join(settings['DirIn'],"EfficiencyForMC.root"),"READ")
    
    data_types = ['MC','Data']

    args = {
            'FileIn':FileIn,
            'nominal_name':nominal_name
            }
    
    etabin = array('d',[0,0.4,0.9,1.5,2.5])
    ptbin=array('d',[20,40,50,65,80,100,200])
    
    SF_Central = Get_SF_Central(File=FileIn,nominal_name=nominal_name)
    SF_Corr_SystUncertainty = Get_SystematicUncertainty('Correlation Type',nominal_name)(Correlation_Err_Calc,**args)
    SF_Diff_SystUncertainty = Get_SystematicUncertainty('Criteria Difference Type',nominal_name)(CriteriaDiff_Err_Calc,**args)

    SF_SystematicUncertainty = np.sqrt((SF_Corr_SystUncertainty * SF_Central)**2+ (SF_Diff_SystUncertainty* SF_Central)**2)
    
    
    SF_hist = TH2D(nominal_name,nominal_name,len(ptbin)-1,ptbin,len(etabin)-1,etabin)
    SF_hist.SetStats(0) 
    SF_hist.SetTitle('')
    if 'l1' in args['nominal_name']:
        SF_hist.GetXaxis().SetTitle('Leading Lepton P_{T}[GeV]')
        SF_hist.GetYaxis().SetTitle('Leading Lepton |#eta|')
    else:
        SF_hist.GetXaxis().SetTitle('Subleading Lepton P_{T}[GeV]')
        SF_hist.GetYaxis().SetTitle('Subleading Lepton |#eta|')
    for i in range(SF_hist.GetNbinsX()):
        for j in range(SF_hist.GetNbinsY()):
            SF_hist.SetBinContent(i+1,j+1,SF_Central[i][j])
            SF_hist.SetBinError(i+1,j+1,SF_SystematicUncertainty[i][j])

    
    f = TFile.Open(os.path.join(settings['DirIn'],'SF'+'_'+nominal_name+'.root'),'RECREATE')
    f.cd()
    SF_hist.Write()
    f.Close()
    TS = CMSTDRStyle.setTDRStyle()
    TS.cd()
    c = TCanvas()
        
    pad = TPad()
    pad.Draw()
    mypalette.colorPalette()
    SF_hist.Draw('COLZ TEXT E')
    CMSstyle.SetStyle(pad)
    c.SetGridx(False)
    c.SetGridy(False)
    pad.SetRightMargin(0.15)
    c.Update()
    c.SaveAs(os.path.join(settings['DirOut'],'SF'+'_'+nominal_name+'.png'))
    pad.Close()
    c.Close()
    del c 
    del TS
    del pad
    del SF_hist

def Get_SystematicUncertainty(Uncertainty_type:str,nominal_name:str):
    def SF_syst_type(func,**args) ->float:
        print('Calculating Systematic Uncertainty: {} for {}'.format(Uncertainty_type,nominal_name))
        return func(**args)
    return SF_syst_type

def Get_SF_Central(File:dict(),nominal_name:str) -> np.ndarray:
    eff_hist2D = dict()
    
    for Type in ['Data','MC']:
        eff_hist2D[Type] = File[Type].Get(nominal_name)

    eff_hist2D['Data'].Divide(eff_hist2D['MC'])
    
    SF_hist2D = eff_hist2D['Data']
    
    SF_Central = np.zeros(shape=(SF_hist2D.GetNbinsX(),SF_hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(SF_hist2D.GetNbinsX()):
        for j in range(SF_hist2D.GetNbinsY()):
            SF_Central[i][j] = SF_hist2D.GetBinContent(i+1,j+1)
    return SF_Central


def Correlation_Err_Calc(**args) -> np.ndarray:
    
    hist2D =  args['FileIn']['Data'].Get(args['nominal_name'])
    
    mettrigger = TEfficiency()
    leptrigger = TEfficiency()
    lepmettrigger = TEfficiency()

    mettrigger = args['FileIn']['Data'].Get('Eff_HLT_MET')
    leptrigger = args['FileIn']['Data'].Get('Eff_HLT_LEP')
    lepmettrigger = args['FileIn']['Data'].Get('Eff_HLT_LEPMET')
    
    alpha = mettrigger.GetEfficiency(1)*leptrigger.GetEfficiency(1)/lepmettrigger.GetEfficiency(1)

    err_array = np.zeros(shape=(hist2D.GetNbinsX(),hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(hist2D.GetNbinsX()):
        for j in range(hist2D.GetNbinsY()):
            err_array[i][j] = 1 -alpha
    return err_array

def CriteriaDiff_Err_Calc(**args) -> np.ndarray:
    
    tags = ['jet','pv']
    eff_hist2D = dict()
    eff_hist2D['Data'] = dict()
    eff_hist2D['MC'] = dict()

    
    for Type in ['Data','MC']:
        eff_hist2D[Type]=dict()
        for tag in ['jet','pv']:
        
            eff_hist2D[Type]['nominal'] = TH2D()
            eff_hist2D[Type]['nominal'] =args['FileIn'][Type].Get(args['nominal_name'])
            eff_hist2D[Type][tag] = dict()
            for criteria in ['low','high']:
                eff_hist2D[Type][tag][criteria] = TH2D()
                eff_hist2D[Type][tag][criteria] = args['FileIn'][Type].Get(args['nominal_name']+'_'+criteria+tag)
    
      
    SF_hist2D = dict()
    
    SF_hist2D['nominal'] = TH2D()
    eff_hist2D['Data']['nominal'].Divide(eff_hist2D['MC']['nominal'])
    SF_hist2D['nominal'] = eff_hist2D['Data']['nominal']
    SF_hist2D['jet'] = dict()
    SF_hist2D['pv'] = dict()

    for tag in ['jet','pv']:
        for criteria in ['low','high']:
            SF_hist2D[tag][criteria] = TH2D()
            eff_hist2D['Data'][tag][criteria].Divide(eff_hist2D['MC'][tag][criteria])
            SF_hist2D[tag][criteria] = eff_hist2D['Data'][tag][criteria]
            
            
    SF_Uncertainty = dict() 
    SF_Uncertainty['jet'] = np.zeros(shape=(SF_hist2D['nominal'].GetNbinsX(),SF_hist2D['nominal'].GetNbinsY()),dtype=np.float32) 
    SF_Uncertainty['pv'] = np.zeros(shape=(SF_hist2D['nominal'].GetNbinsX(),SF_hist2D['nominal'].GetNbinsY()),dtype=np.float32) 

    for tag in ['jet','pv']:
        for i in range(SF_hist2D['nominal'].GetNbinsX()):
            for j in range(SF_hist2D['nominal'].GetNbinsY()):
                uncertainty = abs(SF_hist2D[tag]['low'].GetBinContent(i+1,j+1) - SF_hist2D[tag]['high'].GetBinContent(i+1,j+1))
                uncertainty /= SF_hist2D['nominal'].GetBinContent(i+1,j+1)*2.
                SF_Uncertainty[tag][i][j] += uncertainty
    SF_Uncertainty['nominal'] =np.sqrt(SF_Uncertainty['jet']**2 + SF_Uncertainty['pv']**2)
    
    

    return SF_Uncertainty['nominal']


