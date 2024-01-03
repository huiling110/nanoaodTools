import os
import subprocess

def main():
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022PostEE/'
 #   crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022PostEE_v2/'
    crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022preEE_v3/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022postEE_v3/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_data_v3/'
    # ifResubmit = False
    ifResubmit = True
   
    
    failedList = []
    submitFailList = []
    finishedList = []
    for ipro in os.listdir(crabDir):
        print('i job: ', ipro)
        iJob = crabDir+ipro
        ifFinished = checkStatus(iJob, ifResubmit)
        if ifFinished == 0:
            failedList.append(ipro)
        elif ifFinished == 1:
            submitFailList.append(ipro)
        elif ifFinished == 2: 
            finishedList.append(ipro)
    print('submitFailed: ', submitFailList)
    print('failed: ',failedList)    
    print('finished: ', finishedList)
   
def checkStatus(jobDir, ifResubmit=False):
    command = 'crab status -d ' + jobDir 
    print('command: ', command)
    run = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(run.stdout)
    ifFinished = -1 #0=fail, 1=subfail, 2=finished
    for iline in run.stdout.splitlines():
        if 'Status on the CRAB server:' in iline:
            status = iline.split('Status on the CRAB server:')[1]
            print('status: ', status)
            if 'FAILED' in status:
                resubmit(jobDir, False)
                ifFinished = 1
        if 'Jobs status:' in iline:
            status = iline.split('Jobs status:')[1]
            print('Jobs status: ', status) 
            if 'failed' in status:
                ifFinished = 0
                if ifResubmit:
                    resubmit(jobDir)
            elif 'finished' in status and '100.0%' in status:
                #remove spaces in status
                ifFinished = 2
    print('\n')
    return ifFinished
    
def resubmit(jobDir, ifRe=True):
    print('!!!resubmitting......')
    if ifRe:
        command = 'crab resubmit -d ' + jobDir 
    else:
        command = 'crab submit -d ' + jobDir
    print('command: ', command)
    run = subprocess.run(command, shell=True)
    print(run.stdout)
    print('\n')
    
if __name__=='__main__':
    main()
