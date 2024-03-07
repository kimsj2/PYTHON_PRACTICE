from geant4_pybind import *

import pandas as pd
import math
import sys


class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()

    def Construct(self):
        world_sizeXY = 10*m
        world_sizeZ = 10*m
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
                                  False)

        return physWorld

    def ConstructSDandField(self):
        # Set Magnetic field
        fieldvalue = G4ThreeVector(0*tesla, 0.2*tesla, 0*tesla)
        self.fMagFieldMessenger = G4GlobalMagFieldMessenger(fieldvalue)
        self.fMagFieldMessenger.SetVerboseLevel(1)


class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        # 1. Set particle gun
        self.fParticleGun = G4ParticleGun(1)
        
        # 2. Set particle properties

        # a) set particle table and find particle
        ParticleTable = G4ParticleTable.GetParticleTable()
        self.electron = ParticleTable.FindParticle("e-")
        self.proton = ParticleTable.FindParticle("proton")
        # self.alpha = ParticleTable.FindParticle("alpha")

        self.fParticleGun.SetParticleDefinition(self.proton)

        # b) set particle energy and momentum direction
        self.fParticleGun.SetParticleEnergy(1*MeV)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, -0.001, 1))

    def GeneratePrimaries(self, anEvent):
        # this function is called at the begining of each event
        # this function specify particles of positions every event

        # 3. Set particle position
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 2.5*m, 0))

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
        # self.SetUserAction(baseEventAction())
        # self.SetUserAction(baseTrackingAction())
        self.SetUserAction(baseSteppingAction())
        # self.SetUserAction(baseStackingAction())

######################
###### Optional ######
######################

df = pd.DataFrame(columns=["x (cm)", "y (cm)", "z (cm)", "radius (cm)"])

class baseRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Radius.csv")

        AnalysisManager.CreateNtuple("Step", "Step information")
        AnalysisManager.CreateNtupleDColumn("x (cm)")
        AnalysisManager.CreateNtupleDColumn("y (cm)")
        AnalysisManager.CreateNtupleDColumn("z (cm)")
        AnalysisManager.CreateNtupleDColumn("radius (cm)")

        AnalysisManager.FinishNtuple()

    def EndOfRunAction(self, aRun):
        # Starts at the end of a run

        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()

        return


class baseEventAction(G4UserEventAction):
    # Can be used when you use sensitive detector

    def __init__(self):
        super().__init__()

    def BeginOfEventAction(self, anEvent):
        return

    def EndOfEventAction(self, anEvent):
        # Extract the data from each hit and write it to a file

        # hc = anEvent.GetHCofThisEvent().GetHC(0)
        # hitNum = hc.GetSize()
        # AnalysisManager = G4AnalysisManager.Instance()

        # for i in range(hitNum):
        #     hit = hc.GetHit(i)
        #     AnalysisManager.FillNtupleIColumn(0, hit.fdectorNb)
        #     AnalysisManager.FillNtupleDColumn(1, hit.fEdep)
        #     AnalysisManager.AddNtupleRow(0)

        return


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

    def UserSteppingAction(self, astep):
        AnalysisManager = G4AnalysisManager.Instance()
        
        position = astep.GetPostStepPoint().GetPosition()

        AnalysisManager.FillNtupleDColumn(0, round(float(position.x)*0.1, 4))
        AnalysisManager.FillNtupleDColumn(1, round(float(position.y)*0.1, 4))
        AnalysisManager.FillNtupleDColumn(2, round(float(position.z)*0.1, 4))
        AnalysisManager.FillNtupleDColumn(3, round((float(position.x)*0.1*float(position.x)*0.1 + float(position.z)*0.1*float(position.z)*0.1) / abs(2*float(position.x)*0.1), 4))
        AnalysisManager.AddNtupleRow(0)

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


###########################################
####### User initialization classes #######
###########################################

runManager.SetUserInitialization(baseDetectorConstruction())

###########################################
############## Physics list ###############
###########################################

physicsList = FTFP_BERT()
# proton => FTFP_BERT
# electron => QGSP_BERT
# alpha => QGSP_BERT
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
