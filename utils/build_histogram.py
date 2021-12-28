from itertools import product
from  array import array
from ROOT import TFile,TTree,TH2D, TH1F, TCanvas,TLegend, TEfficiency, TLorentzVector
import command_string as cmd_str
def _global_definition(deactivate=False):
    '''
    Give Global Definition for bins
    '''
    if not deactivate:
        global l1ptbin
        global l2ptbin
        global lepetabin
        global jetbin
        #metbin=array('d',[0,20,40,60,80,100,130,160,200])
        global metbin
        global tdlepetabin
        global tdl1ptbin
        global tdl2ptbin
        global l1p4
        global l2p4

        l1ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        l2ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        lepetabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
        jetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
        #metbin=array('d',[0,20,40,60,80,100,130,160,200])
        metbin=array('d',[100,110,120,130,140,160,180,200,250])
        tdlepetabin=array('d',[0,0.4,0.9,1.5,2.5])
        tdl1ptbin=array('d',[20,40,50,65,80,100,200])
        tdl2ptbin=array('d',[20,40,50,65,80,100,200])
        
        l1p4 = TLorentzVector()
        l2p4 = TLorentzVector()

    else:
        del l1ptbin
        del l2ptbin
        del lepetabin
        del jetbin
        #metbin=array('d',[0,20,40,60,80,100,130,160,200])
        del metbin
        del tdlepetabin
        del tdl1ptbin
        del tdl2ptbin
        del l1p4
        del l2p4


def build_1Dhistogram_for_lep(deactivate=False,command=''):
    states = ['pre','']
    lep_orders = ['l1','l2']
    observables =['eta','pt']
    conditions =['','_low','_high']
    objects = ['','jet','pv','MET']
    for state,order,observable,condition,obj in product(states,lep_orders,observables,conditions,objects):
        if obj == '' and condition != ''  :
            continue
        elif condition =='' and obj != '':
            continue
        if not deactivate:
            x_title = ''
            if order == 'l1':
                x_title +='Leading Lepton'
            else:
                x_title +='Subleading Lepton'
            
            if observable =='pt':
                x_title += ' P_{T} GeV'
            else:
                x_title += ' #eta'
            Bin = order+observable+'bin'
            if observable == 'eta':
                Bin = 'lepetabin'
            c =command.format(state,order,observable,condition,obj,Bin,1,Bin,x_title)
        else:
            c =command.format(state,order,observable,condition,obj)
        exec(c)

def build_1Dhistogram_for_njet(deactivate=False,command=''):
    states = ['','pre_']
    conditions = ['','_low','_high']
    objects = ['','pv','MET']
    xtitle = 'N_{jets}'
    for state,condition,obj in product(states,conditions,objects):
        if condition == '' and obj != '' : continue
        elif condition != '' and obj == '': continue
        if not deactivate:
            c =command.format(state,condition,obj,xtitle)
        else:
            c =command.format(state,condition,obj)
        exec(c)

def build_1Dhistogram_for_met(deactivate=False,command=''):
    states = ['','pre_']
    conditions = ['','_low','_high']
    objects = ['','pv','jet']
    xtitle = 'MET [GeV]'
    for state,condition,obj in product(states,conditions,objects):
        if condition == '' and obj != '' : continue
        elif condition != '' and obj == '': continue
        if not deactivate:
            c =command.format(state,condition,obj,xtitle)
        else:
            c =command.format(state,condition,obj)
        #print(c)
        exec(c)

def build_1Dhistogram_for_pu(deactivate=False,command=''):
    states = ['','pre_']
    conditions = ['','true']
    for state,condition in product(states,conditions):
        if not deactivate:
            c =command.format(state,condition)
        else:
            c =command.format(state,condition)
        #print(c)
        exec(c)
    
def build_2Dhistogram_for_lep(deactivate=False,command=''):
    states = ['','pre']
    leps = ['l1','l2']
    conditions = ['','_low','_high']
    objects = ['','pv','jet','MET']
    _xtitle = 'Leading Lepton P_{T} [GeV]'
    _ytitle = 'Leading Lepton #||{#eta}'
    for state,lep,condition,obj in product(states,leps,conditions,objects):
        if condition == '' and obj != '' : continue
        elif condition != '' and obj == '': continue
        if not deactivate:
            if lep == 'l2':
                xtitle = 'Sub'+_xtitle
                ytitle = 'Sub'+_ytitle
            else:
                xtitle = _xtitle
                ytitle = _ytitle

            c =command.format(state,lep,condition,obj,xtitle,ytitle)
        else:
            c =command.format(state,lep,condition,obj)
        exec(c)


def build_2Dhistogram_for_2lep(deactivate = False,command=''):
    states = ['','pre_']
    observables = ['pt','eta']
    conditions = ['','_low','_high']
    objects = ['','pv','jet','MET']
    _xtitle = 'Leading Lepton #||'
    _ytitle = 'SubLeading Lepton #||' 
    
    for state,observable,condition,obj in product(states,observables,conditions,objects):
        if condition == '' and obj != '' : continue
        elif condition != '' and obj == '': continue
        if not deactivate:
            if observable == 'pt':
                xtitle = _xtitle+'P_{T} [GeV]'
                ytitle = _ytitle+'P_{T} [GeV]'
                xbin = 'tdl1ptbin'
                ybin = 'tdl2ptbin'
                nxbin = 'len(tdl1ptbin)-1'
                nybin = 'len(tdl2ptbin)-1'
            else:
                xtitle = _xtitle+'{#eta}'
                ytitle = _ytitle+'{#eta}'
                xbin = 'tdlepetabin'
                ybin = 'tdlepetabin'
                nxbin = 'len(tdlepetabin)-1'
                nybin = 'len(tdlepetabin)-1'

            c =command.format(state,observable,condition,obj,nxbin,xbin,nybin,ybin,xtitle,ytitle)
        else:
            c =command.format(state,observable,condition,obj)
        exec(c)

def build_tag_histogram(deactivate=False):
    if not deactivate:
        global all_events1
        global all_events2
        global all_events3
        global pass_lep_trigger
        global pass_met_trigger
        global pass_lepmet_trigger

        all_events1 = TH1F('all_events1','lep_tag',1,0,1)
        all_events2 = TH1F('all_events2','met_tag',1,0,1)
        all_events3 = TH1F('all_events3','lepmet_tag',1,0,1)
        pass_lep_trigger= TH1F('pass_lep_trigger','pass_lep_trigger',1,0,1)
        pass_met_trigger= TH1F('pass_met_trigger','pass_met_trigger',1,0,1)
        pass_lepmet_trigger= TH1F('pass_lepmet_trigger','pass_lepmet_trigger',1,0,1)

    else:

        del all_events1
        del all_events2
        del all_events3
        del pass_lep_trigger
        del pass_met_trigger
        del pass_lepmet_trigger



def main():
    _global_definition(False)
    #build_2Dhistogram_for_2lep(False,cmd_str.h2_2lepcommand)
    #build_2Dhistogram_for_2lep(True,cmd_str.del_h2_2lepcommand)
    build_tag_histogram 
    _global_definition(True)
main()
