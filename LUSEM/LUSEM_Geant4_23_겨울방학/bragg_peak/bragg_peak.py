from geant4_pybind import *

import math
import sys


class BraggPeakDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        self.fScoringVolume = None
        
    def Construct(self):
        nist = G4NistManager.Instance()
        
        # World - Galactic
        world_mat = nist.FindOrBuildMaterial("G4_AIR")
        world_sizeXY = 20*cm
        world_sizeZ = 20*cm

        solidWorld = G4Box("World", world_sizeXY, world_sizeXY, world_sizeZ)

        logicWorld = G4LogicalVolume(solidWorld, world_mat, "World")

        physWorld = G4PVPlacement(None,                 # no rotation
                                  G4ThreeVector(),      # at (0,0,0)
                                  logicWorld,           # its logical volume
                                  "World",              # its name
                                  None,                 # its mother  volume
                                  False,                # no boolean operations
                                  0,                    # copy number
                                  False)   # overlaps checking
        
        # Detector - Air
        detector_mat = nist.FindOrBuildMaterial("G4_AIR")

        detector_sizeXY = 10*cm
        detector_sizeZ = 10*cm

        solidDetector = G4Box("Detector", detector_sizeXY, detector_sizeXY, detector_sizeZ)
        
        logicDetector = G4LogicalVolume(solidDetector,
                                        detector_mat,
                                        "Detector")

        G4PVPlacement(None,
                      G4ThreeVector(0,0,0),
                      logicDetector,
                      "Detector",
                      logicWorld,
                      False,
                      0,
                      True)
        
        self.fScoringVolume = logicDetector
        
        return physWorld


class BraggPeakPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        self.fParticleGun = G4ParticleGun(1)

        # Default particle kinematic
        ParticleTable = G4ParticleTable.GetParticleTable()
        particle = ParticleTable.FindParticle("alpha")
        self.fParticleGun.SetParticleDefinition(particle)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, 1))
        self.fParticleGun.SetParticleEnergy(5.49*MeV)

    def GeneratePrimaries(self, anEvent):
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, 0))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class BraggPeakRunAction(G4UserRunAction):

    def __init__(self):
        super().__init__()
        milligray = 1.e-3*gray
        microgray = 1.e-6*gray
        nanogray = 1.e-9*gray
        picogray = 1.e-12*gray

        G4UnitDefinition("milligray", "milliGy", "Dose", milligray)
        G4UnitDefinition("microgray", "microGy", "Dose", microgray)
        G4UnitDefinition("nanogray", "nanoGy", "Dose", nanogray)
        G4UnitDefinition("picogray", "picoGy", "Dose", picogray)
        
        self.edep = G4Accumulable(0)
        self.edep2 = G4Accumulable(0)
        
        accumulableManager = G4AccumulableManager.Instance()
        accumulableManager.RegisterAccumulable(self.edep)
        accumulableManager.RegisterAccumulable(self.edep2)
        
        
    def BeginOfRunAction(self, aRun):
        
        G4RunManager.GetRunManager().SetRandomNumberStore(False)

        accumulableManager = G4AccumulableManager.Instance()
        accumulableManager.Reset()
        

    def EndOfRunAction(self, aRun):
        nofEvents = aRun.GetNumberOfEvent()
        if nofEvents == 0:
            return
        
        accumulableManager = G4AccumulableManager.Instance()
        accumulableManager.Merge()
        
        edep = self.edep.GetValue()
        edep2 = self.edep2.GetValue()
        
        
        rms = edep2 - edep*edep/nofEvents
        if rms > 0:
            rms = math.sqrt(rms)
        else:
            rms = 0

        detectorConstruction = G4RunManager.GetRunManager().GetUserDetectorConstruction()
        mass = detectorConstruction.fScoringVolume.GetMass()
        dose = edep/mass
        rmsDose = rms/mass

        generatorAction = G4RunManager.GetRunManager().GetUserPrimaryGeneratorAction()
        runCondition = ""
        if generatorAction != None and isinstance(generatorAction, BraggPeakPrimaryGeneratorAction):
            particleGun = generatorAction.fParticleGun
            runCondition += particleGun.GetParticleDefinition().GetParticleName() + "(s)"
            runCondition += " of "
            particleEnergy = particleGun.GetParticleEnergy()
            runCondition += "{:.5g}".format(G4BestUnit(particleEnergy, "Energy"))

        if self.IsMaster():
            print("--------------------End of Global Run-----------------------")
        else:
            print("--------------------End of Local Run------------------------")

        print(" The run consists of", nofEvents, runCondition)
        print(" Cumulated dose per run, in scoring volume: ", end="")
        print("{:.5f} rms = {:.5f}".format(G4BestUnit(dose, "Dose"), G4BestUnit(rmsDose, "Dose")))
        print("------------------------------------------------------------")
        print("")
        
    def AddEdep(self, edep):
        self.edep += edep
        self.edep2 += edep*edep
            
class BraggPeakEventAction(G4UserEventAction):

    def __init__(self, runAction):
        super().__init__()
        self.fRunAction = runAction

    def BeginOfEventAction(self, anEvent):
        self.fEdep = 0

    def EndOfEventAction(self, anEvent):
        self.fRunAction.AddEdep(self.fEdep)

    def AddEdep(self, edep):
        self.fEdep += edep
        
        
class BraggPeakSteppingAction(G4UserSteppingAction):

    def __init__(self, eventAction):
        super().__init__()
        self.fEventAction = eventAction
        self.fScoringVolume = None
        
    def UserSteppingAction(self, aStep):
        # track = step.GetTrack()

        if self.fScoringVolume == None:
            detectorConstruction = G4RunManager.GetRunManager().GetUserDetectorConstruction()
            self.fScoringVolume = detectorConstruction.fScoringVolume

        volume = aStep.GetPreStepPoint().GetTouchable().GetVolume().GetLogicalVolume()

        # check if we are in scoring volume
        if volume != self.fScoringVolume:
            return
        # collect energy deposited in this step
        
        position = step.GetPostStepPoint().GetPosition()
        
        edepStep = aStep.GetTotalEnergyDeposit()
        
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.FillNtupleIColumn(0, eventID+1)
        AnalysisManager.FillNtupleDColumn(3, round(float(position.z)*0.1, 4))
        AnalysisManager.FillNtupleIColumn(4, VolumeID)
        AnalysisManager.AddNtupleRow(0)
        
        self.fEventAction.AddEdep(edepStep)
        
        

class BraggPeakActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(BraggPeakRunAction())

    def Build(self):
        self.SetUserAction(BraggPeakPrimaryGeneratorAction())
        
        runAction = BraggPeakRunAction()
        self.SetUserAction(runAction)
        
        eventAction = BraggPeakEventAction(runAction)
        self.SetUserAction(eventAction)
        
        self.SetUserAction(BraggPeakSteppingAction(eventAction))


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

runManager.SetUserInitialization(BraggPeakDetectorConstruction())

###########################################
############## Physics list ###############
###########################################

physicsList = QGSP_BERT()
runManager.SetUserInitialization(physicsList)

###########################################
####### User action initialization ########
###########################################

runManager.SetUserInitialization(BraggPeakActionInitialization())

# Initialize visualization
visManager = G4VisExecutive()
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
