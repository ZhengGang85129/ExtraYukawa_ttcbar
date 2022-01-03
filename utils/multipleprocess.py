import multiprocessing as mp
import os

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

    for i in range(10):
        p = mp.Process(target=calculate ,args=(i,) )
        p.start()

        p.join()
