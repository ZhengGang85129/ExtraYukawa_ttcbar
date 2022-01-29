import os
import fnmatch 
import json

def dump():
    channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

    property_name = dict()

    for channel in channels:
        property_name[channel] = dict()

    property_name['DoubleElectron']['region']=3
    property_name['DoubleElectron']['weight'] = {'l1':['Electron_RECO_SF','Electron_CutBased_TightID_SF'],'l2':['Electron_RECO_SF','Electron_CutBased_TightID_SF']}

    property_name['DoubleElectron']['DY_p4'] = {'l1':['DY_l1_pt','DY_l1_eta','DY_l1_phi','DY_l1_mass'],'l2':['DY_l2_pt','DY_l2_eta','DY_l2_phi','DY_l2_mass']}

    property_name['DoubleMuon']['region']=1
    property_name['DoubleMuon']['weight'] = {'l1':['Muon_CutBased_TightID_SF','Muon_TightRelIso_TightIDandIPCut_SF'],'l2':['Muon_CutBased_TightID_SF','Muon_TightRelIso_TightIDandIPCut_SF']}
    property_name['DoubleMuon']['DY_p4'] = {'l1':['DY_l1_pt','DY_l1_eta','DY_l1_phi','DY_l1_mass'],'l2':['DY_l2_pt','DY_l2_eta','DY_l2_phi','DY_l2_mass']}


    property_name['ElectronMuon']['region']=2
    property_name['ElectronMuon']['weight'] = {'l1':['Muon_CutBased_TightID_SF','Muon_TightRelIso_TightIDandIPCut_SF'],'l2':['Electron_RECO_SF','Electron_CutBased_TightID_SF']}
    property_name['ElectronMuon']['DY_p4'] = {'l1':['Muon_corrected_pt','Muon_eta','Muon_phi','Muon_mass'],'l2':['Electron_pt','Electron_eta','Electron_phi','Electron_mass']}


    for channel in channels:
        property_name[channel]['ttc_p4'] = {'l1':['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass'],'l2':['ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass']}

    with open('./data/datalist/2017/name.json','wt') as f:
        json.dump(property_name, f)
