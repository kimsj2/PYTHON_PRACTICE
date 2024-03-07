from geant4_pybind import *

import math
import sys


######################################################
######## Mandatory for all Geant4 simulations ########
######################################################

class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        # Setting fScoringVolume
        # If you want to set the scoring for every each volume,
        # you can use the following code.

        self.fScoringVolume = None

        # you need to set the scoring volume in Construct() method

    def Construct(self):
        # Solid volume -> Logical volume -> Physical volume
        #
        # 1. Set solid volume
        # Choose shape from G4VSolid and size
        world_sizeXY = 10*cm
        world_sizeZ = 10*cm
        solidWorld = G4Box("World",
                           world_sizeXY,
                           world_sizeXY,
                           world_sizeZ)

        env_sizeXY = 10*cm
        env_sizeZ = 5*cm
        solidEnv = G4Box("Envelope",
                              env_sizeXY,
                              env_sizeXY,
                              env_sizeZ)

        # 2. Set logical volume
        # Choose material from G4NistManager
        nist = G4NistManager.Instance()
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        logicWorld = G4LogicalVolume(solidWorld,
                                     world_mat,
                                     "World")

        env_mat = nist.FindOrBuildMaterial("G4_AIR")
        logicEnv = G4LogicalVolume(solidEnv,
                                        env_mat,
                                        "Envelope")

        # 3. Set physical volume
        physWorld = G4PVPlacement(None,
                                  G4ThreeVector(),
                                  logicWorld,
                                  "World",
                                  None,
                                  False,
                                  0,
                                  True)

        G4PVPlacement(None,
                      G4ThreeVector(0, 0, 5*cm),
                      logicEnv,
                      "Envelope",
                      logicWorld,
                      False,
                      1,
                      True)

        # Can be multiple placements
        # But only one mother volume -> name it "physWorld"

        return physWorld


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
        # self.SetUserAction(baseEventAction())
        # self.SetUserAction(baseStackingAction())
        # self.SetUserAction(baseTrackingAction())
        global pathLength
        pathLength = 0
        self.SetUserAction(baseSteppingAction())

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
        AnalysisManager.OpenFile("Particle_energy.csv")
        
        AnalysisManager.CreateNtuple("Step", "Step information")
        AnalysisManager.CreateNtupleIColumn("eventID")
        AnalysisManager.CreateNtupleDColumn("Path length (mm)")
        AnalysisManager.CreateNtupleDColumn("step length (mm)")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        AnalysisManager.CreateNtupleDColumn("Total Energy (MeV)")
        
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

    def UserSteppingAction(self, aStep):
        # get Momentum of particle / with step length and eventID
        eventID = aStep.GetTrack().GetTrackID()
        totEnergy = aStep.GetTrack().GetKineticEnergy()/MeV
        lossEnergy = aStep.GetTotalEnergyDeposit()/MeV
        stepLength = aStep.GetStepLength()/mm
        global pathLength
        pathLength += stepLength
                
        # save data to csv file
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.FillNtupleIColumn(0, eventID)
        AnalysisManager.FillNtupleDColumn(1, pathLength)
        AnalysisManager.FillNtupleDColumn(2, stepLength)
        AnalysisManager.FillNtupleDColumn(3, lossEnergy)
        AnalysisManager.FillNtupleDColumn(4, totEnergy)
        AnalysisManager.AddNtupleRow()
        
        
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
