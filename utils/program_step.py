import fnmatch
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
from ROOT import TFile, TH1F, TH2D, TCanvas, TLegend, TPad, TEfficiency
from array import array
import utils.myanalyzer as analyzer
import utils.listoutdata2txt as d2t
import utils.multipleprocess as mp
import utils.CMSTDRStyle as CMSTDRStyle
import utils.CMSstyle as CMSstyle
import utils.mypalette as mypalette
import others.property_name as property_name
import json


def create_structure(setting):
    '''
    To decide which stage should be performed in trigger effiency
    when create_structure is set to be True, Only perform make directory
    Otherwise, performing trigger calculation.
    '''
    dir_list = ['./data','./data/trigger_data','./data/datalist','./data/HLT_2017','./others','./others/property_name']
    
    #Create Specific Structure for this Study
    
    infilepatterns = setting.get('infilepatterns',None)
    source  = setting.get('source',None)
    

    for d in dir_list:
        if os.path.isdir(d):
            print('Directory: {} exists!'.format(d))
        else:
            print('Directory: {} created!'.format(d))
            os.mkdir(d)
    
    #Create txt file:"datalistname" in which to save paths of data/MC.
    datalistname = './data/datalist/triggerinput.txt'
    d2t.generatefile(datalistname,infilepatterns=infilepatterns,path_to_data=source)
    
    #Create HLT Trigger Json File.
    d2t.generate_HLT_path()

    #Create names of property for leptons, ex: weights, p4.
    property_name.dump()

def Trig_Calc(datalistname = './data/datalist/triggerinput.txt',channels=['DoubleElectron','DoubleMuon','ElectronMuon']):
    with open('./data/HLT_2017/HLT_Trigger.json','rb') as f:
        HLT_Path = json.load(f)
    with open('./others/property_name/name.json','rb') as f :
        property_name = json.load(f)

    HLT_MET = ' or '.join(['self.tree.'+p for p in HLT_Path['MET']])
    with open(datalistname,'r') as f:
            # To calculate Trigger Efficiency for Each channel
            for idx,filename in enumerate(f.readlines()):
                MP = mp.multiprocess()
                for channel in channels:
                    setting={
                        'HLT_MET': HLT_MET,
                        'HLT_LEP': ' or '.join(['self.tree.'+p for p in HLT_Path[channel]]),
                        'property_name' : property_name[channel],
                        'channel' : channel,
                        'outputdir' : './data/trigger_data',
                        'infilepath' : filename[:-1],
                    }
                    setting['infilebasename'] = os.path.basename(setting['infilepath']).split(".root")[0]
                    setting['outfilename'] = os.path.join(setting['outputdir'],setting['infilebasename']+'_'+setting['channel']+'.root')
                    MP.register(Calc_efficiency,process_args=[setting])
                MP.run()


def Calc_efficiency(setting):
    '''
    Calculating trigger efficiency.
    infilename : input file path, one of file path listed in datalist/triggerinput.txt
    outdirpath : naming output directory name.
    channel : Specify Channel Name : option ['DoubleElectron','DoubleMuon','ElectronMuon']
    '''
    
    production = analyzer.analyzer(setting)
    production.analyze()


def Plot_efficiency(channels):
    '''
    plot Trigger histograms to visualize what's in root file respectively.
    '''
    user_settings=dict()
    tags = {
            'l1':{
                'pt':['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_highpv','l1pt_lowpv','l1pt_highMET','l1pt_lowMET'] ,
                'eta':['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_highpv','l1eta_lowpv','l1eta_highMET','l1eta_lowMET'],
                'pteta':['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_highpv','l1pteta_lowpv','l1pteta_highMET','l1pteta_lowMET']
            },
            'l2':{
                'pt':['l2pt','l2pt_highjet','l2pt_lowjet','l2pt_highpv','l2pt_lowpv','l2pt_highMET','l2pt_lowMET'] ,
                'eta':['l2eta','l2eta_highjet','l2eta_lowjet','l2eta_highpv','l2eta_lowpv','l2eta_highMET','l2eta_lowMET'],
                'pteta':['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_highpv','l1pteta_lowpv','l1pteta_highMET','l1pteta_lowMET']
            },
            'l1l2':{
                'pt':['l1l2pt','l1l2pt_highjet','l1l2pt_lowjet','l1l2pt_highpv','l1l2pt_lowpv','l1l2pt_highMET','l1l2pt_lowMET'],
                'eta':['l1l2eta','l1l2eta_highjet','l1l2eta_lowjet','l1l2eta_highpv','l1l2eta_lowpv','l1l2eta_highMET','l1l2eta_lowMET']
                }
        }

    for channel in channels:
        print('Plotting 1D histograms for channel :{}'.format(channel))
        user_settings['channel'] = channel
        
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
        for tag in  tags['l1l2']['pt']:
            Plot(plot_eff2d,**user_settings)(tag=tag)
        for tag in  tags['l1l2']['eta']:
            Plot(plot_eff2d,**user_settings)(tag=tag)


def Plot(func,**user_settings):
    settings ={
    'Type': user_settings.get('Type','NULL'),
    'colors' : user_settings.get('colors',[1,4]),
    'infiledir' : user_settings.get('infiledir','./data/trigger_data'),
    'channel' :user_settings.get('channel','ee'),
    'outfiledir'  : user_settings.get('outfilename','/eos/user/z/zhenggan/ttcbar/trigger_plot')
    }
    def decorator(tag):
        print(f'Type: {settings["Type"]}\n')
        return func(tag=tag,**settings)
    return decorator


def plot_eff1d(tag:str,**settings):
    infilenames = []
    histograms_list =[]
    infiles = []
    data_names =[] # used in Legend name
    for file in os.listdir(settings['infiledir']):
        if fnmatch.fnmatch(file,'*'+settings['channel']+'.root'):
            infilenames.append(os.path.join(settings['infiledir'],file))
            data_names.append(file.split('.root')[0])
    for filename in infilenames:
        infiles.append(TFile.Open(filename))
    nfiles = len(infiles)
    
    for idx ,infile in enumerate(infiles):
        name, histogram = create_hist(infile,tag)
        histograms_list.append(histogram)
        data_names.append(name) 
    TS = CMSTDRStyle.setTDRStyle()
    TS.cd()
    c = TCanvas()
    c.cd()
    pad = TPad()
    pad.Draw()
    leg = TLegend(0.5,0.2,0.65,0.2+0.05*nfiles)
    for idx , (histogram, label) in enumerate(zip(histograms_list,data_names)):
        histogram.SetLineColor(settings['colors'][idx])
        histogram.SetMarkerStyle(20)
        histogram.SetMarkerSize(0.5)
        histogram.SetMarkerColor(settings['colors'][idx])
        gr = histogram.CreateGraph()
        gr.SetMinimum(0.5)
        gr.SetMaximum(1.0)
        if idx ==0:
            gr.Draw("AP")
        else:
            gr.Draw("samep")
        leg.AddEntry(histogram,label)
    CMSstyle.SetStyle(pad)
    leg.SetFillStyle(0)
    leg.Draw('SAME') 
    c.Update()
    c.SaveAs(os.path.join(settings['outfiledir'],tag+'_'+settings['channel']+'.png'))
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
    histotemp = TEfficiency()
    histoname = 'pre_'+tag+'_clone'
    histotemp = infile.Get(histoname)
    histotemp.SetNameTitle(tag,"")
    
    return histoname ,histotemp

def plot_eff2d(tag:str,**settings):
    file_patterns =[]
    infilenames = [] 
    infiles = []

    for file in os.listdir(settings['infiledir']):
        if fnmatch.fnmatch(file,'*'+settings['channel']+'.root'):
            infilenames.append(os.path.join(settings['infiledir'],file))
            file_patterns.append(file.split('.root')[0])
    for filename in infilenames:
        infiles.append(TFile.Open(filename))
    
    for infile,infilename,fpattern in zip(infiles,infilenames,file_patterns):
        histo2d = TH2D()
        histo2d = infile.Get(tag)
        histo2d.SetNameTitle("","")
        TS = CMSTDRStyle.setTDRStyle()
        TS.cd()
        c = TCanvas()
        pad = TPad()
        pad.Draw()
        mypalette.colorPalette()
        histo2d.Draw('COLZ TEXT E')
        CMSstyle.SetStyle(pad)
        c.SetGridx(False)
        c.SetGridy(False)
        pad.SetRightMargin(0.15)
        c.Update()
        c.SaveAs(os.path.join(settings['outfiledir'],'eff2d_'+fpattern+'_'+tag+'.png'))
        pad.Close()
        c.Close()
        del c 
        del TS
        del pad
        del histo2d

import numpy as np

def SF_Calc(**user_settings):
    '''
    MC -> TTTo2L
    data -> MET
    '''
    settings={
            'channel': user_settings.get('channel','ee'),
            'infiledir': user_settings.get('infiledir','./data/trigger_data'),
            'outfiledir': user_settings.get('outfiledir','/eos/user/z/zhenggan/ttcbar/SF_plot'),
            }
    
    settings['Data'] = dict()
    settings['MC'] = dict()
    nominal_names =['l1pteta','l2pteta']
    
    for file in os.listdir(settings['infiledir']):
        if fnmatch.fnmatch(file,'*_'+settings['channel']+'.root'):
            basename = file.split('_'+settings['channel']+'.root')[0]
            if basename == 'MET':
                data_type = 'Data'
            elif basename =='TTTo2L':
                data_type = 'MC'
            else:
                print(f'Wring Basename {basename}')
                raise ValueError
            
            settings[data_type]['basename'] = basename
            settings[data_type]['infilename'] = os.path.join(settings['infiledir'],file)
            settings[data_type]['infile'] = TFile.Open(settings[data_type]['infilename'])
    
    for nominal_name in nominal_names:
        ScaleFactors(nominal_name,**settings)
    
    
def ScaleFactors(nominal_name:str,**settings):

    '''
    Calculate ScaleFactor for a single certain nominal variable.
    '''
    
    args = dict()
    
    data_types = ['MC','Data']
    for data_type in data_types:
        args[data_type] = settings[data_type]['infile']
    
    args['nominal_name'] = nominal_name
    etabin = array('d',[0,0.4,0.9,1.5,2.5])
    ptbin=array('d',[20,40,50,65,80,100,200])
    
    SF_Central = Get_SF_Central(**args)
    SF_Corr_SystUncertainty = Get_SystematicUncertainty('Correlation Type',nominal_name)(Correlation_Err_Calc,**args)
    SF_Diff_SystUncertainty = Get_SystematicUncertainty('Criteria Difference Type',nominal_name)(CriteriaDiff_Err_Calc,**args)

    SF_SystematicUncertainty = np.sqrt((SF_Corr_SystUncertainty* SF_Central)**2+ (SF_Diff_SystUncertainty* SF_Central)**2)
    
    
    SF_hist = TH2D(args['nominal_name'],args['nominal_name'],len(ptbin)-1,ptbin,len(etabin)-1,etabin)
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
    c.SaveAs(os.path.join(settings['outfiledir'],'sf'+'_'+nominal_name+'_'+settings['channel']+'.png'))
    
    f = TFile.Open(os.path.join(settings['outfiledir'],'sf'+'_'+nominal_name+'_'+settings['channel']+'.root'),'recreate')
    f.cd()
    SF_hist.Write()
    f.Close()
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

def Get_SF_Central(**args) -> np.ndarray:
    eff_hist2D = dict()
    
    for data_type in ['Data','MC']:
        eff_hist2D[data_type] = args[data_type].Get(args['nominal_name'])

    eff_hist2D['Data'].Divide(eff_hist2D['MC'])
    
    SF_hist2D = eff_hist2D['Data']
    
    SF_Central = np.zeros(shape=(SF_hist2D.GetNbinsX(),SF_hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(SF_hist2D.GetNbinsX()):
        for j in range(SF_hist2D.GetNbinsY()):
            SF_Central[i][j] = SF_hist2D.GetBinContent(i+1,j+1)
    return SF_Central


def Correlation_Err_Calc(**args) -> np.ndarray:
    Args ={
            'Data': args.get('Data'),
            'nominal_name': args.get('nominal_name')
    }
    
    hist2D =  Args['Data'].Get(Args['nominal_name'])
    err_array = np.zeros(shape=(hist2D.GetNbinsX(),hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(hist2D.GetNbinsX()):
        for j in range(hist2D.GetNbinsY()):
            err_array[i][j] = 0.0022
    return err_array

def CriteriaDiff_Err_Calc(**Args) -> np.ndarray:
    
    tags = ['jet','pv']
    eff_hist2D = dict()
    eff_hist2D['Data'] = dict()
    eff_hist2D['MC'] = dict()

    
    for data_type in ['Data','MC']:
        eff_hist2D[data_type]=dict()
        for tag in ['jet','pv']:
        
            eff_hist2D[data_type]['nominal'] = TH2D()
            eff_hist2D[data_type]['nominal'] = Args[data_type].Get(Args['nominal_name'])
            eff_hist2D[data_type][tag] = dict()
            for criteria in ['low','high']:
                eff_hist2D[data_type][tag][criteria] = TH2D()
                eff_hist2D[data_type][tag][criteria] = Args[data_type].Get(Args['nominal_name']+'_'+criteria+tag)
    
      
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


