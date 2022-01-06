import multiprocessing as mp
import os
import threading  as th

def nworkers():
    cpus = mp.cpu_count()
    print('Number of Wokers :{}'.format(cpus))
    return cpus


class multiprocess:
    def __init__(self):
        self.process_list = []
        self.process_args_list =[]
    def register(self,process,process_args=[]):
        self.process_list.append(process)
        self.process_args_list.append(process_args)

    def run(self):
        for process,args in zip(self.process_list,self.process_args_list):
            p = mp.Process(target=process,args=(args))
            p.start()

class multithread:
    def __init__(self):
        self.thread_list =[]
        self.thread_args_list =[]
    def register(self,thread,thread_args=[]):
        self.thread_list.append(thread)
        self.thread_args_list.append(thread_args)

    def run(self):
        for thread,args in zip(self.thread_list,self.thread_args_list):
            p = th.Thread(target=thread,args=(args))
            p.start()

def calculate(arg):
    print(arg)
    i = 0
    while(True):
        if i == 50:
            break
        print(i)
        i+=1
if __name__ == '__main__':
    nworkers()

