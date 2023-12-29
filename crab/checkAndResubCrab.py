import os
import subprocess

def main():
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022PostEE/'
 #   crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022PostEE_v2/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022preEE_v3/'
    crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022postEE_v3/'
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_data_v3/'
    ifResubmit = False
   
    
    for ipro in os.listdir(crabDir):
        print('i job: ', ipro)
        iJob = crabDir+ipro
        checkStatus(iJob, ifResubmit)
   
def checkStatus(jobDir, ifResubmit=False):
    command = 'crab status -d ' + jobDir 
    print('command: ', command)
    run = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(run.stdout)
    if ifResubmit:
        for iline in run.stdout.splitlines():
            if 'Status on the CRAB server:' in iline:
                status = iline.split('Status on the CRAB server:')[1]
                print('status: ', status)
                if 'FAILED' in status:
                    resubmit(jobDir, False)
            elif 'Jobs status:' in iline:
                status = iline.split('Jobs status:')[1]
                print('Jobs status: ', status) 
                if 'failed' in status:
                    resubmit(jobDir)
    print('\n')
    
def resubmit(jobDir, ifRe=True):
    print('!!!resubmitting...')
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
