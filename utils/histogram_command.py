from itertools import product
from  array import array
from ROOT import TFile,TTree,TH2D, TH1F, TCanvas,TLegend, TEfficiency, TLorentzVector
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
        
        l1ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        l2ptbin=array('d',[20, 40, 50, 65, 80, 100, 200])
        lepetabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
        jetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
        #metbin=array('d',[0,20,40,60,80,100,130,160,200])
        metbin=array('d',[100,110,120,130,140,160,180,200,250])
        tdlepetabin=array('d',[0,0.4,0.9,1.5,2.5])
        tdl1ptbin=array('d',[20,40,50,65,80,100,200])
        tdl2ptbin=array('d',[20,40,50,65,80,100,200])
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

def build_histogram_for_lep(deactivate=False,command=''):
    _global_definition()
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
    _global_definition(True)

def main():
    build_histogram_for_lep(False,h1command)
    build_histogram_for_lep(True,del_h1command)
