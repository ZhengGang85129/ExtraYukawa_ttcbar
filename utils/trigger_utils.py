import fnmatch
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)

import ROOT
from ROOT import TFile, TH1F, TH2D, TCanvas, TLegend, TPad, TEfficiency

import utils.analyzer as analyzer
import utils.listoutdata2txt as d2t
import utils.multipleprocess as mp
import utils.CMSTDRStyle as CMSTDRStyle
import utils.CMSstyle as CMSstyle

def trigger_store(create_structure=True,src=''):
    '''
    To decide which stage should be performed in trigger effiency
    when create_structure is set to be True, Only perform make directory
    Otherwise, performing trigger calculation.
    '''
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
                #Use Multiprocess to read files and save histograms into new files.
                MP = mp.multiprocess()
                for channel in ['ee','em','mm']:
                    MP.register(trigger_calc,process_args=[filename[:-1],'./data/trigger_data',channel])
                MP.run()

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
    

def trigger_plot(infiledir = './data/trigger_data',colors=[],png_path ='/eos/user/z/zhenggan/ttcbar/trigger_plot',channels=['mm','em','ee']):
    '''
    plot Trigger histograms to visualize what's in root file respectively.
    '''
    trigger_hist1d(infiledir,colors,png_path,channels)




def create_hist(infile,first_tag,second_tag):
    '''
    A lazy function to get histogram in root file.
    '''
    histotemp = TEfficiency()
    histoname = 'pre_'+first_tag+second_tag+'clone'
    histotemp = infile.Get(histoname)
    histotemp.SetNameTitle(first_tag+second_tag,"")
    return histoname ,histotemp


def trigger_hist1d(infiledir = './data/trigger_data',colors=[],png_path ='/eos/user/z/zhenggan/ttcbar/trigger_plot',channels=['m    m','em','ee']):
    
    '''
    Aiming for plot trigger 1D histos.
    '''
    
    #Tag used in histogram.
    first_tags = ['met_','njet_','l1pt_','l2pt_','l1eta_','l2eta_']
    second_tags = ['','lowjet_','highjet_','lowpv_','highpv_','lowMET_','highMET_']
    
    for channel in channels:
        infilenames =[]     
        histograms_list = []
        outfilenames = []
        infiles =[]
        labels = [] # used for Histogram Legend name
        #Purpose of this block: Match File Pattern
        for file in os.listdir(infiledir):
            if fnmatch.fnmatch(file,'*'+channel+'.root'):
                infilenames.append(os.path.join(infiledir,file))
                labels.append(file)
        
        
        for filename in infilenames:
            infiles.append(TFile.Open(filename))
        
        nfiles = len(infiles)
        
        #Create Histograms and naming histogram.
        for idx ,infile in enumerate(infiles):
            histograms =[]
            histonames =[]
            for first_tag in first_tags:
                for second_tag in second_tags:
                    if first_tag == 'met_' or first_tag == 'njet_':
                        second_tag = ''
                        skip = True
                    else:
                        skip=False
                    name, histogram = create_hist(infile,first_tag,second_tag)
                    histograms.append(histogram)
                    if idx == 0:
                        outfilenames.append(name)
                    print(name)
                    if skip:
                        break
            histograms_list.append(histograms)
        
        #Sorting histogram to be a easy-holding order
        unzip_histograms = zip(*histograms_list)
        sorted_histograms_list = list(unzip_histograms)
        '''
        a = [[1,2,3],[1,2,3]]
        unzip_objects = zip(*a)
        unzip_a_list = list(a)
        unzip_a_list -> [[1,1],[2,2],[3,3]]
        '''

        for histograms,outfilename in zip(sorted_histograms_list,outfilenames):
            TS = CMSTDRStyle.setTDRStyle()
            TS.cd()
            c = TCanvas()
            c.cd()
            pad = TPad()
            pad.Draw()
            leg = TLegend(0.5,0.2,0.65,0.2+0.05*nfiles)
            for idx , (histogram, infilename,label) in enumerate(zip(histograms,infilenames,labels)):
                histogram.SetLineColor(colors[idx])
                histogram.SetMarkerStyle(20)
                histogram.SetMarkerSize(0.5)
                histogram.SetMarkerColor(colors[idx])
                gr = histogram.CreateGraph()
                gr.SetMinimum(0.5)
                gr.SetMaximum(1.0)
                if idx ==0:
                    gr.Draw("AP")
                else:
                    gr.Draw("samep")
                leg.AddEntry(histogram,label[:-5])
            CMSstyle.SetStyle(pad)
            leg.SetFillStyle(0)
            leg.Draw('SAME') 
            c.Update()
            c.SaveAs(os.path.join(png_path,outfilename+'_'+channel+'.png'))
            c.Close()
            pad.Close()
            del c
            del TS
            del pad
            del leg

