import os
import subprocess

def main():
    # crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost/'
    crabDir = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crab_crabNanoPost_2022PostEE/'
    
    for ipro in os.listdir(crabDir):
        print('i job: ', ipro)
        iJob = crabDir+ipro
        checkStatus(iJob)
   
def checkStatus(jobDir):
    command = 'crab status -d ' + jobDir 
    print('command: ', command)
    run = subprocess.run(command, shell=True)
    print(run.stdout)
    
    
    
if __name__=='__main__':
    main()