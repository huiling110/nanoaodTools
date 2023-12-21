# import CRABClient
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
# from copy import deepcopy
# import os

# !!!needs to be run on python2
def main(): 
    # submitVersion = "crabNanoPost"
    # submitVersion = "crabNanoPost_2022PostEE"
    # submitVersion = "crabNanoPost_2022PostEE_v2" 
    # submitVersion = 'crabNanoPost_2022preEE_v3' 
    submitVersion = 'crabNanoPost_2022postEE_v3' 
    # inputDas = 'DASinputList.txt'
    # inputDas = './input/MC2022Samples.txt'
    inputDas = './input/MC2022PostEESamples.txt'
  
   
    mainOutputDir = '/store/user/hhua/%s' % submitVersion
    dasList = getListFromTxt(inputDas)
    # print(dasList)
    dasDic = generateNamePair(dasList)
    # print(dasDic)
    for idas, name in dasDic:
        print(idas, name)
        submitCrab(idas, name, submitVersion, mainOutputDir)#MC
        print('\n')

 
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



        
        
def submitCrab(dataset, name, submitVersion, mainOutputDir, isData=False):
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
    # conf.JobType.sendPythonFolder = True # seems deprecated
    
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

def getListFromTxt( DatasetTxt ):
    with open(DatasetTxt) as f:
        lines = f.readlines()
        #not including lines starting with #
        lines = [x for x in lines if not x.startswith('#')]
    return [x.strip() for x in lines]


def generateNamePair( datasetList ):
    # generate name pair for each element in datasetList, if name is overlapping, add a number to the end
    name_dict = {}
    for idas in datasetList:
        if not idas.startswith('/'): continue
        name = idas.split('/')[1]
        if name not in name_dict:
            name_dict[name] = 0
        else:
            name_dict[name] += 1
        yield (idas, name if name_dict[name] == 0 else name + str(name_dict[name]))    
    # return name_dict 
    
    
    
    
# def generateNamePair(datasetList):
#     name_dict = {}
#     for name in datasetList:
#         if name not in name_dict:
#             name_dict[name] = 0
#         else:
#             name_dict[name] += 1
#         yield (name, name if name_dict[name] == 0 else name + str(name_dict[name]))
    
    
    
        
        
if __name__ == "__main__":
    main()