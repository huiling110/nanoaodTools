# import CRABClient
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
# from copy import deepcopy
# import os

# needs to be run on python2

 
def submit(config):
    res = crabCommand('submit', config = config)
    #save crab config for the future
    with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
        fi.write(config.pythonise_())

samples = [
    # ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM', 
    #  'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL16NanoAODAPV'),
    ('/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/NANOAODSIM', 'TTto2L2Nu'),
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
        # conf.JobType.allowUndistributedCMSSW = True
        
        conf.section_("Data")
        # conf.Data.allowNonValidInputDataset = True
        conf.Data.inputDBS = 'global'
        conf.Data.publication = False
        conf.Data.splitting     = 'FileBased'
        conf.Data.unitsPerJob   = 1
        conf.Data.inputDataset = dataset
        conf.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
        
        conf.section_("User")
        conf.Site.storageSite = "T2_CN_Beijing"
        submit(conf)