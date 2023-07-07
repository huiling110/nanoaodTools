# import CRABClient
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from copy import deepcopy
import os
 
def submit(config):
    res = crabCommand('submit', config = config)
    #save crab config for the future
    with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
        fi.write(config.pythonise_())

samples = [
    ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM', 
     'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL16NanoAODAPV'),
    # ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM', 
    #  'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL16NanoAOD'),
    # ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM', 
    #  'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL17NanoAOD'),
    # ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM', 
    #  'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL18NanoAOD')
]


submitVersion = "crabNanoPost"
# mainOutputDir = '/store/user/akapoor/%s' % submitVersion
mainOutputDir = '/store/user/hhua/%s' % submitVersion

if __name__ == "__main__":
    for dataset, name in samples:
        conf = config()
        conf.section_("General")
        conf.General.transferLogs = True        
        conf.General.workArea = 'crab_%s' % submitVersion
        conf.General.transferOutputs = True
        conf.General.requestName = name
        conf.section_("JobType")
        conf.JobType.pluginName  = 'Analysis'
        conf.JobType.psetName = 'PSet.py'
        conf.JobType.scriptExe = 'crab_script.sh'
        conf.JobType.inputFiles = ['crab_script.py', '../scripts/haddnano.py']
        conf.JobType.sendPythonFolder = True
        conf.JobType.allowUndistributedCMSSW = True
        conf.JobType.maxJobRuntimeMin = 5
        conf.section_("Data")
        conf.Data.allowNonValidInputDataset = True
        conf.Data.inputDBS = 'global'
        conf.Data.publication = False
        conf.Data.splitting     = 'FileBased'
        # conf.Data.splitting = 'Automatic'
        conf.Data.unitsPerJob   = 1
        # conf.Data.unitsPerJob = 2
        # conf.Data.totalUnits = 10
        # conf.Data.unitsPerJob   = 200
        conf.Data.inputDataset = dataset
        conf.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
        conf.section_("User")
        conf.Site.storageSite = "T2_CN_Beijing"
        submit(conf)