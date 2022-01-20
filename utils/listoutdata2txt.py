import os
from os import listdir
from os.path import isfile, join
import glob
import json
import os
import fnmatch

def getFiles(path= '/eos/user/m/melu/TTC_Nanov8_new',fpattern = "MET*.root"):
    ffile_list = []
    pattern = os.path.join(path,fpattern)
    endPaths = glob.glob(pattern)
    ffile_list += endPaths
    return ffile_list

def generatefile(datalistname='./data/trigger.txt',infilepatterns=['MET.root','TTTo2L*.root','TTTo1L*.root'],path_to_data='/eos/user/m/melu/TTC_Nanov8_new'):
    with open(datalistname,'w') as f:
        for pattern in infilepatterns:
            for name in getFiles(path = path_to_data,fpattern = pattern):
                f.write(name+'\n')
def generate_HLT_path():
    HLT_Path =dict()
    data_dir = './others/HLT_2017'
    Json_Path = './data/HLT_2017/HLT_Trigger.json'
    for file in os.listdir(data_dir):
        key_name = file.split("_Trigger.txt")[0]
        file_path = os.path.join(data_dir,file)
        with open(file_path,'r',newline='\n') as f:
            HLT_Path[key_name] =[ element for element in f.read().split("\n") if element != ""]
    with open(Json_Path,'w') as f:
        json.dump(HLT_Path,f)    

