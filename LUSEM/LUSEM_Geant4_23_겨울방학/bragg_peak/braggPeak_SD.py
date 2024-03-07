from geant4_pybind import *

import math
import sys


######################################################
######## Mandatory for all Geant4 simulations ########
######################################################

class baseHit(G4VHit):

    def __init__(self, trackID, detectorNb, edep, pos):
        super().__init__()
        self.fTrackID = trackID
        self.fdectorNb = detectorNb
        self.fEdep = edep
        self.fPos = pos

    def Draw(self):
        return


class baseHitsCollection(G4VHitsCollection):

    def __init__(self, detName, colNam):
        super().__init__(detName, colNam)
        self.collection = []

    def __getitem__(self, i):
        return self.collection[i]

    def insert(self, item):
        self.collection.append(item)

    def GetHit(self, i):
        return self.collection[i]

    def GetSize(self):
        return len(self.collection)


class baseSensitiveDetector(G4VSensitiveDetector):

    def __init__(self, name, hitsCollectionName):
        super().__init__(name)
        self.collectionName.insert(hitsCollectionName)

    def Initialize(self, hce):
        self.fHitsCollection = baseHitsCollection(
            self.SensitiveDetectorName, self.collectionName[0])

        hcID = G4SDManager.GetSDMpointer().GetCollectionID(
            self.collectionName[0])
        hce.AddHitsCollection(hcID, self.fHitsCollection)

    def ProcessHits(self, aStep, aHistory):
        edep = aStep.GetTotalEnergyDeposit()
        if edep == 0:
            return False

        newHit = baseHit(aStep.GetTrack().GetTrackID(),
                         aStep.GetPreStepPoint().GetTouchable().GetCopyNumber(),
                         edep,
                         aStep.GetPreStepPoint().GetPosition())

        self.fHitsCollection.insert(newHit)

        return True

    def EndOfEvent(self, hce):
        if self.verboseLevel > 1:
            hitNum = self.fHitsCollection.GetSize()


class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        # Setting fScoringVolume
        # If you want to set the scoring for every each volume,
        # you can use the following code.

        # self.fScoringVolume = None

        # you need to set the scoring volume in Construct() method

    def Construct(self):
        # Solid volume -> Logical volume -> Physical volume
        #
        # 1. Set solid volume
        # Choose shape from G4VSolid and size
        world_sizeXY = 5*cm
        world_sizeZ = 10*cm
        solidWorld = G4Box("World",
                           0.5 * world_sizeXY,
                           0.5 * world_sizeXY,
                           0.5 * world_sizeZ)

        # 2. Set logical volume
        # Choose material from G4NistManager
        nist = G4NistManager.Instance()
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        logicWorld = G4LogicalVolume(solidWorld,
                                     world_mat,
                                     "World")

        # 3. Set physical volume
        physWorld = G4PVPlacement(None,
                                  G4ThreeVector(),
                                  logicWorld,
                                  "World",
                                  None,
                                  False,
                                  0,
                                  True)


        # Detector
              
        detector_sizeXY = 1*cm
        detector_sizeZ = 0.01*cm
        solidDetector = G4Box("Detector",
                              0.5 * detector_sizeXY,
                              0.5 * detector_sizeXY,
                              0.5 * detector_sizeZ)
        
        detector_mat = nist.FindOrBuildMaterial("G4_AIR")
        logicDetector = G4LogicalVolume(solidDetector,
                                        detector_mat,
                                        "Detector")
        
        for i in range(498):
            G4PVPlacement(None,
                          G4ThreeVector(0, 0, (i+1)*0.01*cm),
                          logicDetector,
                          "Detector"+str(i+1),
                          logicWorld,
                          False,
                          i+1,
                          True)
        
        # Can be multiple placements
        # But only one mother volume -> name it "physWorld"
        logicDetector.SetVisAttributes(G4VisAttributes.GetInvisible())
        
        return physWorld
    
    def ConstructSDandField(self):
        # Sensitive detector
        detectorSD = baseSensitiveDetector(
            "DetectorSD", "DetectorHitsCollection")
        G4SDManager.GetSDMpointer().AddNewDetector(detectorSD)
        self.SetSensitiveDetector("Detector", detectorSD)

class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        # 1. Set particle gun
        self.fParticleGun = G4ParticleGun(1)

        # 2. Set particle properties

        # a) set particle table and find particle
        ParticleTable = G4ParticleTable.GetParticleTable()
        particle = ParticleTable.FindParticle("alpha")

        self.fParticleGun.SetParticleDefinition(particle)

        # b) set particle energy and momentum direction
        self.fParticleGun.SetParticleEnergy(5.49*MeV)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, 1))

    def GeneratePrimaries(self, anEvent):
        # this function is called at the begining of each event
        # this function specify particles of positions every event

        # 3. Set particle position
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, 0))

        # 4. Generate primary particles
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class baseActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(baseRunAction())

    def Build(self):
        # initialization of actions
        self.SetUserAction(basePrimaryGeneratorAction())
        self.SetUserAction(baseRunAction())
        self.SetUserAction(baseEventAction())
        # self.SetUserAction(baseStackingAction())
        # self.SetUserAction(baseTrackingAction())
        #self.SetUserAction(baseSteppingAction())

######################
###### Optional ######
######################


class baseRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("SD.csv")
        
        AnalysisManager.CreateNtuple("Hit", "Hit information")
        AnalysisManager.CreateNtupleIColumn("VolumeID")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        
        AnalysisManager.FinishNtuple()

    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()


class baseEventAction(G4UserEventAction):

    def __init__(self):
        super().__init__()

    def BeginOfEventAction(self, anEvent):
        return

    def EndOfEventAction(self, anEvent):
        hc = anEvent.GetHCofThisEvent().GetHC(0)
        hitNum = hc.GetSize()
        AnalysisManager = G4AnalysisManager.Instance()

        for i in range(hitNum):
            hit = hc.GetHit(i)
            AnalysisManager.FillNtupleIColumn(0, hit.fdectorNb)
            AnalysisManager.FillNtupleDColumn(1, hit.fEdep)
            AnalysisManager.AddNtupleRow(0)


class baseTrackingAction(G4UserTrackingAction):

    def __init__(self):
        super().__init__()

    def PreUserTrackingAction(self, aTrack):
        return

    def PostUserTrackingAction(self, aTrack):
        return


class baseSteppingAction(G4UserSteppingAction):

    def __init__(self):
        super().__init__()
        self.detector_hits = []

    def UserSteppingAction(self, aStep):
        # get Momentum of particle / with step length and eventID
        eventID = aStep.GetTrack().GetTrackID()
        totEnergy = aStep.GetTrack().GetKineticEnergy()/MeV
        lossEnergy = aStep.GetTotalEnergyDeposit()/MeV
        stepLength = aStep.GetStepLength()/mm
        global pathLength
        pathLength += stepLength
        
        # get volume ID
        tochable = aStep.GetPreStepPoint().GetTouchable()
        copyNo = tochable.GetCopyNumber()
                
        # save data to csv file
        if copyNo not in self.detector_hits:
            self.detector_hits.append(copyNo)
            
            AnalysisManager = G4AnalysisManager.Instance()
            AnalysisManager.FillNtupleIColumn(0, eventID)
            AnalysisManager.FillNtupleDColumn(1, pathLength)
            AnalysisManager.FillNtupleDColumn(2, stepLength)
            AnalysisManager.FillNtupleDColumn(3, lossEnergy)
            AnalysisManager.FillNtupleDColumn(4, totEnergy)
            AnalysisManager.FillNtupleIColumn(5, copyNo)
            AnalysisManager.AddNtupleRow()
        else:
            pass
        
        
        
        
class baseStackingAction(G4UserStackingAction):

    def __init__(self):
        super().__init__()

    def ClassifyNewTrack(self, aTrack):
        return

    def NewStage(self):
        return

    def PrepareNewEvent(self):
        return


# Start of the simulation
ui = None

if len(sys.argv) == 1:
    ui = G4UIExecutive(len(sys.argv), sys.argv)

# optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

# Construct the default run manager
runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)


###########################################
####### User initialization classes #######
###########################################

runManager.SetUserInitialization(baseDetectorConstruction())

###########################################
############## Physics list ###############
###########################################

physicsList = QGSP_BERT()
runManager.SetUserInitialization(physicsList)

###########################################
####### User action initialization ########
###########################################

runManager.SetUserInitialization(baseActionInitialization())


# Initialize visualization
visManager = G4VisExecutive()
# G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
# visManager = G4VisExecutive("Quiet")
visManager.Initialize()

# Get the User Interface manager
UImanager = G4UImanager.GetUIpointer()

# Process macro or start UI session
if ui == None:
    # batch mode
    command = "/control/execute "
    fileName = sys.argv[1]
    UImanager.ApplyCommand(command+fileName)
else:
    # interactive mode
    UImanager.ApplyCommand("/control/execute init_vis.mac")
    ui.SessionStart()
