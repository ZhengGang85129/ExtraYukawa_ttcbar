import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import utils.analyzer as analyzer
import utils.listoutdata2txt as d2t
import utils.multipleprocess as mp


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
    
def trigger_store(create_structure=True,src=''):
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
                MP = mp.multiprocess()
                for channel in ['ee','em','mm']:
                    MP.register(trigger_calc,process_args=[filename[:-1],'./data/trigger_data',channel])
                MP.run()


