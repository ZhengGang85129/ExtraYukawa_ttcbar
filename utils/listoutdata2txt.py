import os
from os import listdir
from os.path import isfile, join

import glob


def getFiles(path= '/eos/user/m/melu/TTC_Nanov8_new',fpattern = "MET*.root"):
    ffile_list = []
    pattern = os.path.join(path,fpattern)
    endPaths = glob.glob(pattern)
    ffile_list += endPaths
    return ffile_list

def generatefile(datalistname='./data/trigger.txt',patterns=['MET.root','TTTo2L*.root','TTTo1L*.root'],path_to_data='/eos/user/m/melu/TTC_Nanov8_new'):
    with open(datalistname,'w') as f:
        for pattern in patterns:
            for name in getFiles(path = path_to_data,fpattern = pattern):
                f.write(name+'\n')
