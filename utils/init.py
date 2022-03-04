import os,sys 
import json
import fnmatch 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from utils.general_tool import get_NumberOfEvent


def GenPaths_HLTTrigger_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels.
    
    '''
    trigger = dict()
    
    trigger['DoubleElectron'] = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_passEle32WPTight", "HLT_Ele35_WPTight_Gsf"]
    trigger['DoubleMuon'] = ["HLT_IsoMu27", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]
    trigger["ElectronMuon"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_IsoMu27", "HLT_passEle32WPTight", "HLT_passEle32WPTight"]
    trigger['MET'] = ["HLT_PFMET120_PFMHT120_IDTight", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", "HLT_PFHT500_PFMET100_PFMHT100_IDTight", "HLT_PFHT700_PFMET85_PFMHT85_IDTight", "HLT_PFHT800_PFMET75_PFMHT75_IDTight"]

    with open(f'./data/year{year}/configuration/HLTTrigger.json','w')  as f:
        json.dump(trigger,f,indent=4)

def GenPaths_HLTTriggerCondition_ForAnalyzer_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels used in Analyzer condition.
    
    '''

    trigger =dict()

    trigger['All'] = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf'

    trigger['DoubleElectron'] =dict()

    trigger['DoubleElectron']['DoubleElectron'] = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
    trigger['DoubleElectron']['SingleElectron'] = '!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'

    trigger['DoubleMuon'] = dict()
    trigger['DoubleMuon']['DoubleMuon'] = '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)'
    trigger['DoubleMuon']['SingleMuon'] = '!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27'

    trigger['ElectronMuon'] = dict()
    trigger['ElectronMuon']['SingleElectron'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'
    trigger['ElectronMuon']['SingleMuon'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27'
    trigger['ElectronMuon']['ElectronMuon'] = '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)'

    with open(f'./data/year{year}/configuration/HLTTriggerCondition.json','wt')  as f:
        json.dump(trigger,f,indent=4)

def GenDataPath_File(year:str):
    '''
    
    Build JSON file to record MC/Data paths.
    
    '''
    data_dir = '/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/'

    Dileptons_types = ['DoubleMuon','SingleMuon','DoubleElectron','SingleElectron','ElectronMuon']


    data_path = dict()
    data_path['Data'] = dict()
    data_path['MC'] = dict()

    for Dileptons_type in  Dileptons_types:
        data_path['Data'][Dileptons_type] =dict()

    data_path['Data']['DoubleMuon'] = [os.path.join(data_dir,'DoubleMuon' + postfix + '.root') for postfix in ['B','C','D','E','F']]
    data_path['Data']['SingleMuon'] = [os.path.join(data_dir,'SingleMuon' + postfix + '.root') for postfix in ['B','C','D','E','F']]
    data_path['Data']['DoubleElectron'] = [os.path.join(data_dir,'DoubleEG' + postfix + '.root') for postfix in ['B','C','D','E','F'] ]
    data_path['Data']['SingleElectron'] = [os.path.join(data_dir,'SingleEG' + postfix + '.root') for postfix in ['B','C','D','E','F']]
    data_path['Data']['ElectronMuon'] = [os.path.join(data_dir,'MuonEG' + postfix + '.root' ) for postfix in ['B','C','D','E','F'] ]


    MCname_list = ['DY','WJets','WWdps','WZ_ew','WZ_qcd','ZZ','WWW','WWZ','WZZ','ZZZ','tsch','t_tch','tbar_tch','tW','tbarW','ttWtoLNu','ttWtoQQ','ttZ','ttZtoQQ','ttH','ttWW','ttWZ','ttZZ','tzq','TTTo2L','TTTo1L']

    for MCname in MCname_list:
        data_path['MC'][MCname] = os.path.join(data_dir,MCname+'.root')

    with open(f'./data/year{year}/path/datapath.json','wt') as f:
        json.dump(data_path,f,indent=4)

def GenTrigEffInput_File(year:str):
    '''
    
    Build JSON file to record Input path for TriggerEfficiency Calculation Stage.
    
    '''
    path = {
            "Data":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METB.root'
                ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METC.root'
                ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METD.root'
                ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METE.root'
                ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METF.root'],
            "MC":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/TTTo2L.root']
            }
    with open(f'./data/year{year}/path/filein.json','w') as f:
        json.dump(path,f,indent=4)

def GenLeptonIDSF_File(year:str):
    path = {
            'DoubleElectron':{ 
                'path':'/afs/cern.ch/user/m/melu/public/output.root',
                    'name':'EleIDDataEff'},
            'DoubleMuon':{
                'path':'/eos/user/t/tihsu/share/muonID_SF/2018UL/muonIdSF_2018UL.root',
                'name':'muIDSF'
                },
            'ElectronMuon':{
                'path':{
                    'Muon':'/eos/user/t/tihsu/share/muonID_SF/2018UL/muonIdSF_2018UL.root',
                    'Electron':'/afs/cern.ch/user/m/melu/public/output.root'
                },
                'name':{
                    'Muon':'muIDSF',
                    'Electron':'EleIDDataEff'
                    }

                }
    }
    with open(f'./data/year{year}/path/LeptonsID_SF.json','w') as f:
        json.dump(path,f,indent=4)

def GenXsValue_File(year:str):
    '''
    
    Build JSON file to record xs values for associated physics process.
    
    '''
    Event =dict()
    Event['xs'] = dict()
    Event['NumberOfEvents'] = dict()
    Event['xs']['lumi'] = 41480.
    Event['xs']['DY'] = 6077.22
    Event['xs']['WJets'] = 61526.7
    Event['xs']['WWdps'] = 118.7
    Event['xs']['WZ'] = 65.5443
    Event['xs']['ZZ'] = 15.8274
    Event['xs']['WWW'] = 0.2086
    Event['xs']['WWZ'] = 0.1707
    Event['xs']['WZZ'] = 0.05709
    Event['xs']['ZZZ'] = 0.01476
    Event['xs']['TTTo2L'] = 88.3419
    Event['xs']['TTTo1L'] = 365.4574
    Event['xs']['ttH'] = 0.5269
    Event['xs']['ttWtoLNu']  = 0.1792
    Event['xs']['ttWtoQQ'] = 0.3708
    Event['xs']['ttZ'] = 0.2589
    Event['xs']['ttZtoQQ'] = 0.6012
    Event['xs']['ttWW'] = 0.007003
    Event['xs']['ttWZ'] = 0.002453
    Event['xs']['ttZZ'] = 0.001386
    Event['xs']['tzq'] = 0.07561
    Event['xs']['tW'] = 35.85
    Event['xs']['tbarW'] = 35.85
    Event['xs']['tsch'] = 3.36
    Event['xs']['t_tch'] = 136.02
    Event['xs']['tbar_tch'] = 80.95

    with open(f'./data/year{year}/path/datapath.json' , 'rb') as f:
        MC_Paths = json.load(f)['MC']

    for MC in MC_Paths.keys():
        Event['NumberOfEvents'][MC] = get_NumberOfEvent(MC_Paths[MC])

    with open(f'./data/year{year}/configuration/data_xs.json','wt') as f:
        json.dump(Event,f,indent=4)


def GenVariableNames_File(year:str):
    '''
    
    Build JSON file to record Variable names.
    
    '''
    channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

    property_name = dict()

    for channel in channels:
        property_name[channel] = dict()

    property_name['DoubleElectron']['region']=3
    property_name['DoubleElectron']['weight'] = {'l1':'Electron_RECO_SF','l2':'Electron_RECO_SF'}

    property_name['DoubleElectron']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}

    property_name['DoubleMuon']['region']=1
    property_name['DoubleMuon']['weight'] = {'l1':None,'l2':None}
    property_name['DoubleMuon']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}


    property_name['ElectronMuon']['region']=2
    property_name['ElectronMuon']['weight'] = {'l1':None,'l2':['Electron_RECO_SF']}
    property_name['ElectronMuon']['OPS_p4'] = {'l1':['Muon_corrected_pt','Muon_eta','Muon_phi','Muon_mass'],'l2':['Electron_pt','Electron_eta','Electron_phi','Electron_mass']}


    for channel in channels:
        property_name[channel]['ttc_p4'] = {'l1':['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass'],'l2':['ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass']}

    with open(f'./data/year{year}/configuration/name.json','wt') as f:
        json.dump(property_name, f,indent=4)

def GenGoodFlag_File(year:str):
    '''
    Build Json file which contents Flag Name.
    '''

    Flags = ['Flag_goodVertices','Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter', 'Flag_eeBadScFilter', 'Flag_ecalBadCalibFilter']
    with open(f'./data/year{year}/configuration/flag.json','wt') as f :
        json.dump(Flags,f,indent=4)


