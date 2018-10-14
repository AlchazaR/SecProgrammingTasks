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
import _thread
import time


rootPath = r'/home/vlad/Documents/Repo/consumerPattern/rand_files/'
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
                print("!!! NOT Primary {}".format(n))
                return False
        return True       


def calculate(files, filesScanned, maxNum, minNum, threadname):
    print("{} started...".format(threadname))
    with open(files[filesScanned]) as f:
        print("File: {} in thread {} scanning...".format(files[filesScanned],threadname))
        content = f.readlines()
        for num in content:
            num = int(num)
            if getPrimary(num):
                if num > maxNum:
                    maxNum = num
                if num < minNum:
                    minNum = num 
                print("    ({}) Primary Number: {}".format(threadname, num))
    #f.close
        


if __name__ == '__main__':
    files = getFiles(rootPath)

    filesScanned = 0
    minNum = 0
    maxNum = 0

    # get first file from list
    ##for fName in files:
    while filesScanned < len(files):
        try:
            _thread.start_new_thread(calculate,(files,filesScanned,maxNum, minNum, "Thread-1"))
            filesScanned = filesScanned + 1
            _thread.start_new_thread(calculate,(files,filesScanned,maxNum, minNum, "Thread-2"))
            filesScanned = filesScanned + 1
            _thread.start_new_thread(calculate,(files,filesScanned,maxNum, minNum, "Thread-3"))
            filesScanned = filesScanned + 1
            _thread.start_new_thread(calculate,(files,filesScanned,maxNum, minNum, "Thread-4"))
            filesScanned = filesScanned + 1
        except:
            print("Error: unable to start thread")
        """with open(files[filesScanned]) as f:
            print("File: {}".format(files[filesScanned]))
            filesScanned = filesScanned + 1
            content = f.readlines()
            for num in content:
                num = int(num)
                if getPrimary(num):
                    if num > maxNum:
                        maxNum = num
                    if num < minNum:
                        minNum = num 
                    print("     Primary Number: {}".format(num))
            f.close
        """
                
        # start thread 1
        # remove first file from list
        # scan file for primary numbers and show output 
