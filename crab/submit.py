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
    # ('/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/NANOAODSIM', 'TTto2L2Nu'),
    # ('/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/NANOAODSIM', 'TTto4Q'),
    # ('/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM', 'TTtoLNu2Q'),
    # ('/JetHT/Run2022C-ReRecoNanoAODv11-v1/NANOAOD', 'JetHT2022C'),
    # ('/JetMET/Run2022C-ReRecoNanoAODv11-v1/NANOAOD', 'JetMet2022C'),
    # ('/JetMET/Run2022D-ReRecoNanoAODv11-v1/NANOAOD', 'JetMet2022D'),
    #postEE
    # ('/JetMET/Run2022E-ReRecoNanoAODv11-v1/NANOAOD', 'JetMet2022E'),
    # ('/JetMET/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD', 'JetMet2022F'),
    # ('/JetMET/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD', 'JetMet2022G'),
    #mc
    ('/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM', 'TTtoL2Nu2Q'),
    # ('/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM', 'TTto4Q'),
    ('/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM', 'TTto2L2Nu'),
]


# submitVersion = "crabNanoPost"
# submitVersion = "crabNanoPost_2022PostEE"
submitVersion = "crabNanoPost_2022PostEE_v2"
mainOutputDir = '/store/user/hhua/%s' % submitVersion

        
        
def submitCrab(dataset, submitVersion, isData=False):
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
    
    conf.section_("Data")
    conf.Data.inputDBS = 'global'
    conf.Data.publication = False
    conf.Data.splitting     = 'FileBased'
    conf.Data.unitsPerJob   = 1
    conf.Data.inputDataset = dataset
    if not isData:
        outDir = '%s/%s/' % (mainOutputDir,'mc')
    else:
        outDir = '%s/%s/' % (mainOutputDir,'data')
    conf.Data.outLFNDirBase = outDir
    
    conf.section_("User")
    conf.Site.storageSite = "T2_CN_Beijing"
    submit(conf)
        
        
        
if __name__ == "__main__":
    for dataset, name in samples:
        # submitCrab(dataset, submitVersion)
        submitCrab(dataset, submitVersion, True)