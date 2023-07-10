# from WMCore.Configuration import Configuration
# from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

from datasetList import datasetList

#where to find the output of code? in the output T2 log dir


def main():
    jobVersion = 'nanoPost_v0'
    for idata in datasetList:
        configOneDataSet(idata)




def configOneDataSet(dataset, version):
    # config = Configuration()
    config = config()

    config.section_("General")
    # config.General.requestName = 'NanoPost1'
    config.General.requestName = version
    config.General.transferLogs = True
    # config.General.workArea = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crabLog/' #The area (full or relative path) where to create the CRAB project directory.
    config.General.workArea = '/afs/cern.ch/work/h/hhua/nanoAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/crab/crabLog/'+ version + '/' #The area (full or relative path) where to create the CRAB project directory.

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe = 'crab_script.sh'
    # hadd nano will not be needed once nano tools are in cmssw
    config.JobType.inputFiles = ['crab_script.py', '../scripts/haddnano.py']
    config.JobType.sendPythonFolder = True
    
    config.section_("Data")
    # config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
    # config.Data.inputDataset = '/TTto4Q_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM'
    config.Data.inputDataset = dataset
    #config.Data.inputDBS = 'phys03'
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'FileBased'
    #config.Data.splitting = 'EventAwareLumiBased'
    config.Data.unitsPerJob = 1
    # config.Data.totalUnits = 10

    # config.Data.outLFNDirBase = '/store/user/%s/NanoPost' % (
        # getUsernameFromSiteDB())
    # config.Data.outLFNDirBase = '/store/user/hhua/'
    config.Data.outLFNDirBase = '/store/user/hhua/'+ version + '/'
    config.Data.publication = False
    # config.Data.outputDatasetTag = 'NanoTestPost'
    config.Data.outputDatasetTag = version
    # config.section_("Site")
    config.section_("User")
    # config.Site.storageSite = "T2_DE_DESY"
    config.Site.storageSite = 'T2_CN_Beijing'
    #config.Site.storageSite = "T2_CH_CERN"
    #config.User.voGroup = 'dcms'
    
    crabSubmit(config)


def crabSubmit(config):
    res = crabCommand('submit', config = config)
    #save crab config for the future
    with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
        fi.write(config.pythonise_())
    


if __name__=='__main__':
    main()