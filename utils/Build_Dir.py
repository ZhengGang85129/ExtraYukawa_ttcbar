import sys
import os,json 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
#import utils.listoutdata2txt as d2t
from utils.general_tool import MakeDir


def Build_Dir(setting):
    '''
    Build Necessary Directories For Saving Trigger Efficiency/Scale Factors Calculation, e.t.c
    
    '''
    YEAR = setting.year
    DirParName = setting.DirOut
    Channels = setting.channels
    Task = setting.task
    
    if YEAR is None:
        raise ValueError('Argument: [year] must be specified.')
    if DirParName is None:
        raise ValueError('Argument: [DirOut] must be specified.')
    if Channels is None:
        raise ValueError('Argument: [Channels] must be specified.')
    if Task is None:
        raise ValueError('Argument: [Task] must be specified.')
    
    MakeDir(Root = DirParName,ChildName = 'ExtraYukawa')
    DirParName = os.path.join(DirParName,'ExtraYukawa')
    MakeDir(Root = DirParName,ChildName = Task)
    DirParName = os.path.join(DirParName,Task)
    MakeDir(Root = DirParName,ChildName = 'year'+YEAR)
    DirParName = os.path.join(DirParName,'year'+YEAR)
    User = dict()
    User['DirOut'] = dict()
    for channel in Channels:
        User['DirOut'][channel] = dict()
        MakeDir(Root = DirParName, ChildName = channel)
        DirParName_tmp = os.path.join(DirParName,channel)
        MakeDir(Root = DirParName_tmp, ChildName = 'files')
        MakeDir(Root = DirParName_tmp, ChildName = 'plots')
        User['DirOut'][channel]['files'] = os.path.join(DirParName_tmp,'files')
        User['DirOut'][channel]['plots'] = os.path.join(DirParName_tmp,'plots')
    User['UserName'] = DirParName.split("/")[4]
    PrivateFile = f'data/year{setting.year}/User.json'
    print(f'Your Out put file will store here: {PrivateFile}')
    with open(PrivateFile,'w') as f:
        json.dump(User,f,indent=4)


    #Create txt file:"datalistname" in which to save paths of data/MC.
    #datalistname = './data/datalist/triggerinput.txt'
    #d2t.generatefile(datalistname,infilepatterns=infilepatterns,path_to_data=source)
    
    #Create HLT Trigger Json File.
    #d2t.generate_HLT_path()

    #Create names of property for leptons, ex: weights, p4.
    #property_name.dump()




