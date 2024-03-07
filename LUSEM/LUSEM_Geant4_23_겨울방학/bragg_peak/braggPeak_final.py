from geant4_pybind import *

import math
import sys


######################################################
######## Mandatory for all Geant4 simulations ########
######################################################

class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()


    def Construct(self):
        world_sizeXY = 5*cm
        world_sizeZ = 11*cm
        solidWorld = G4Box("World",
                           0.5 * world_sizeXY,
                           0.5 * world_sizeXY,
                           0.5 * world_sizeZ)


        nist = G4NistManager.Instance()
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        logicWorld = G4LogicalVolume(solidWorld,
                                     world_mat,
                                     "World")

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
                                        "DetectorLV")
        
        for i in range(500):
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
        G4SDManager.GetSDMpointer().SetVerboseLevel(1)
        d_box = G4MultiFunctionalDetector("Detector")
        G4SDManager.GetSDMpointer().AddNewDetector(d_box)
        primitiv1 = G4PSEnergyDeposit("edep")
        d_box.RegisterPrimitive(primitiv1)
        self.SetSensitiveDetector("DetectorLV", d_box)


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
        self.SetUserAction(baseEventAction(baseRunAction()))
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
        AnalysisManager.OpenFile("SD_final.csv")
        
        AnalysisManager.CreateNtuple("Hit", "Hit information")
        AnalysisManager.CreateNtupleDColumn("Length(cm)")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        
        AnalysisManager.FinishNtuple()

    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()


class baseEventAction(G4UserEventAction):

    def __init__(self,runAction):
        super().__init__()
        self.fRunAction = runAction

    def EndOfEventAction(self, anEvent):
        HCE = anEvent.GetHCofThisEvent()
        SDMan = G4SDManager.GetSDMpointer()
        
        AnalysisManager = G4AnalysisManager.Instance()
        
        self.fCollID_d_box = SDMan.GetCollectionID("Detector/edep")
        evtMap = HCE.GetHC(self.fCollID_d_box)
        for copyNb, edep in evtMap:
            AnalysisManager.FillNtupleDColumn(0, copyNb*0.01)
            AnalysisManager.FillNtupleDColumn(1, edep)
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
