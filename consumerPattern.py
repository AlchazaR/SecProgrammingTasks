"""
    You have 1000 files with random numbers. When using n threads (n should be possible to adjusted live), filter out only primary numbers when showing real-time statistics:

    Number of threads
    Number of files done
    Last found primary number
    Max found primary number
    Min found primary number

    In this task you must use concurrent collections and producer - consumer pattern.
"""


import glob, os
import sys
import multiprocessing
import time


#rootPath = r'/home/vlad/Documents/Repo/consumerPattern/rand_files/'
rootPath = r'C:/Docs/Mokslai/saugusProgramavimas/SecProgrammingTasks/rand_files/'
searchExt = [".txt"]
os.chdir(rootPath)

"""
    Get file path and filename
"""
def storeFile (fDir, fName):

    return os.path.join(fDir, fName)


"""
    Get list of files
"""
def getFiles(rootPath):
    files=[]
    for dirname, dirnames, filenames in os.walk(rootPath):
        # get path to all found filenames        
        for filename in filenames:
            if filename.endswith(tuple(searchExt)): 
                fPath = storeFile(dirname, filename)
                files.append(fPath)
    return(files)


def getPrimary(n):
    if (n==1):
        return False
    elif (n==2):
        return True
    else:
        for x in range(2,n):
            if(n % x==0):
                return False
        return True       


def calculate(fileName, threadnr):
    print("Thread nr {} started to scan {} file...".format(threadnr, fileName))
    outFile = open('../Thread_{}.txt'.format(threadnr), 'a')
    outFile.write('Parent process:{} \n process id: {} \n'.format(os.getppid(), os.getpid()))
    minNum = 0
    maxNum = 0
    #print('parent process:', os.getppid())
    #print('process id:', os.getpid())
    with open(fileName) as f:
        #print("File: {} in thread {} scanning...".format(fileName,threadname))
        content = f.readlines()
        for num in content:
            num = int(num)
            if getPrimary(num):
                if num > maxNum:
                    maxNum = num
                if minNum == 0:
                    minNum = num
                if num < minNum:
                    minNum = num 
                outFile.write("    ({}) Primary Number: {} \n".format(threadnr, num))
                #print("    ({}) Primary Number: {}".format(threadnr, num))
    outFile.write("{} finished. Max - {}, Min - {} \n".format(threadnr, maxNum, minNum))
    print("Thread nr {} finished scanning file {} ".format(threadnr, fileName))
    outFile.close
    f.close
        


if __name__ == '__main__':
    files = getFiles(rootPath)

    filesScanned = 0

    # get first file from list
    jobs = []
    while filesScanned < len(files):
        
        active = multiprocessing.active_children()
        if len(active) < 4:
            try:
                print("starting file: {}, threads count - ".format(files[filesScanned]), len(active))
                p = multiprocessing.Process(target = calculate, args = (files[filesScanned], filesScanned, ))
                jobs.append(p)
                p.start()              
                filesScanned = filesScanned + 1               
            except:
                print("Error: unable to start thread")
