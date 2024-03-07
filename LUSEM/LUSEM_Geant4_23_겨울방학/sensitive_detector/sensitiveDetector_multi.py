from geant4_pybind import *

import math
import sys


class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()

    def Construct(self):
        nist = G4NistManager.Instance()
        
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        detector_mat = nist.FindOrBuildMaterial("G4_Si")
        
        world_sizeXY = 30*cm
        world_sizeZ = 30*cm
        solidWorld = G4Box("World",
                           world_sizeXY,
                           world_sizeXY,
                           world_sizeZ)
        
        logicWorld = G4LogicalVolume(solidWorld,
                                     world_mat,
                                     "World")

        physWorld = G4PVPlacement(None,
                                  G4ThreeVector(),
                                  logicWorld,
                                  "WorldLV",
                                  None,
                                  False,
                                  0,
                                  True)
        
        detector_sizeXY = 1*cm
        detector_sizeZ = 1*mm
        
        detectorS = G4Box("Detector",
                            detector_sizeXY,
                            detector_sizeXY,
                            detector_sizeZ)
        
        detectorLV = G4LogicalVolume(detectorS,
                                      detector_mat,
                                      "DetectorLV")
        
        G4PVPlacement(None,
                      G4ThreeVector(),
                      detectorLV,
                      "Detector",
                      logicWorld,
                      False,
                      0,
                      True)
        
        logicWorld.SetVisAttributes(G4VisAttributes.GetInvisible())
        
        return  physWorld
    
    def ConstructSDandField(self):
        G4SDManager.GetSDMpointer().SetVerboseLevel(1)
        
        d_box = G4MultiFunctionalDetector("Detector")
        G4SDManager.GetSDMpointer().AddNewDetector(d_box)
        
        primitiv1 = G4PSEnergyDeposit("edep")
        d_box.RegisterPrimitive(primitiv1)
        self.SetSensitiveDetector("DetectorLV", d_box)

class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        self.fParticleGun = G4ParticleGun(1)
        # Default particle kinematic
        ParticleTable = G4ParticleTable.GetParticleTable()
        self.electron = ParticleTable.FindParticle("e-")
        self.fParticleGun.SetParticleDefinition(self.electron)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, 1))
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, -10*cm))
        self.fParticleGun.SetParticleEnergy(1*MeV)
        
        self.proton = ParticleTable.FindParticle("proton")
        self.alpha = ParticleTable.FindParticle("alpha")
        
    def GeneratePrimaries(self, anEvent):
        i = int(3 * G4UniformRand())
        if i == 0:
            particle = self.proton
        elif i == 1:
            particle = self.alpha
        else:
            particle = self.electron
        self.fParticleGun.SetParticleDefinition(particle)
        self.fParticleGun.SetParticleEnergy(1*MeV)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, 1))
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, -10*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class baseActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(baseRunAction())

    def Build(self):
        # initialization of actions
        self.SetUserAction(basePrimaryGeneratorAction())
        runAction = baseRunAction()
        self.SetUserAction(runAction)
        self.SetUserAction(baseEventAction())
        # self.SetUserAction(baseStackingAction())
        # self.SetUserAction(baseTrackingAction())
        # self.SetUserAction(baseSteppingAction())

######################
###### Optional ######
######################


class baseRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()
        G4RunManager.GetRunManager().SetPrintProgress(1)
        AnalysisManager = G4AnalysisManager.Instance()
        
        AnalysisManager.CreateNtuple("step", "Step information")
        AnalysisManager.CreateNtupleSColumn("particle_name_1")
        AnalysisManager.CreateNtupleIColumn("eventID_1")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)_1")
        AnalysisManager.CreateNtupleSColumn("particle_name_2")
        AnalysisManager.CreateNtupleIColumn("eventID_2")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)_2")
        AnalysisManager.CreateNtupleSColumn("particle_name_3")
        AnalysisManager.CreateNtupleIColumn("eventID_3")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)_3")
        
        AnalysisManager.FinishNtuple()
        
        # self.fGoodEvents = G4Accumulable(0)
        # self.fSumDose = G4Accumulable(0)
        
        # accumulableManager = G4AccumulableManager.Instance()
        
        # accumulableManager.RegisterAccumulable(self.fGoodEvents)
        # accumulableManager.RegisterAccumulable(self.fSumDose)
        
        
    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Sensitive_Detector_multi.csv")
        
        
    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()
    
    # def Savedata(self, edep):
    #     nofEvents = run.GetNumberOfEvent()
    #     accumulableManager = G4AccumulableManager.Instance()
    #     accumulableManager.Merge()
        
    #     AnalysisManager = G4AnalysisManager.Instance()
    #     AnalysisManager.FillNtupleIColumn(0, nofEvents+1)
    #     AnalysisManager.FillNtupleDColumn(1, edep)
    #     AnalysisManager.AddNtupleRow(0)


class baseEventAction(G4UserEventAction):

    def __init__(self):
        super().__init__()
        self.fCollID_d_box = -1
        
    def EndOfEventAction(self, anEvent):
        HCE = anEvent.GetHCofThisEvent()
        SDMan = G4SDManager.GetSDMpointer()
        eventID = anEvent.GetEventID()
        
        generatorAction = G4RunManager.GetRunManager().GetUserPrimaryGeneratorAction()
        particle = generatorAction.fParticleGun.GetParticleDefinition()
        partName = particle.GetParticleName()
        
        self.fCollID_d_box = SDMan.GetCollectionID("Detector/edep")
        evtMap = HCE.GetHC(self.fCollID_d_box)
        for copyNb, edep in evtMap:
            AnalysisManager = G4AnalysisManager.Instance()
            if (partName =="e-"):
                AnalysisManager.FillNtupleSColumn(0, partName)
                AnalysisManager.FillNtupleIColumn(1, eventID+1)
                AnalysisManager.FillNtupleDColumn(2, edep)
            elif (partName =="proton"):
                AnalysisManager.FillNtupleSColumn(3, partName)
                AnalysisManager.FillNtupleIColumn(4, eventID+1)
                AnalysisManager.FillNtupleDColumn(5, edep)
            else:
                AnalysisManager.FillNtupleSColumn(6, partName)
                AnalysisManager.FillNtupleIColumn(7, eventID+1)
                AnalysisManager.FillNtupleDColumn(8, edep)
            
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

    def UserSteppingAction(self, aStep):
        return


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


runManager.SetUserInitialization(baseDetectorConstruction())

###########################################
############## Physics list ###############
###########################################

physicsList = FTFP_BERT() # proton
# physicsList = QGSP_BERT() # electron, alpha

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
