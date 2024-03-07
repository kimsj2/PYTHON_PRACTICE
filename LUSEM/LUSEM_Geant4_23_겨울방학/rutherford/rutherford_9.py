from geant4_pybind import *

import math
import sys


class RutherfordDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        self.fScoringVolume = None

    def Construct(self):
        nist = G4NistManager.Instance()

        # World - Air
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        world_sizeXY = 100*cm
        world_sizeZ = 100*cm

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

        # Target - Thin foil of gold
        foil_mat = nist.FindOrBuildMaterial("G4_Au")
        foil_sizeXY = 10*cm
        foil_sizeZ = 0.1*um

        solidFoil = G4Box("Target", foil_sizeXY,
                          foil_sizeXY, foil_sizeZ)

        logicFoil = G4LogicalVolume(solidFoil, foil_mat, "Target")

        G4PVPlacement(None,                 # no rotation
                      G4ThreeVector(),      # at (0,0,0)
                      logicFoil,           # its logical volume
                      "Target",             # its name
                      logicWorld,           # its mother  volume
                      False,                # no boolean operations
                      10,                    # copy number
                      True)   # overlaps checking

        # Detector - Silicon
        detector_mat = nist.FindOrBuildMaterial("G4_Si")

        innerRadius = 49.0*cm
        outerRadius = 50.0*cm
        halfHeight = 90*cm
        startAngle = 9.0 * degree
        spanningAngle = 38.0 * degree

        solidDetector = G4Tubs("Detector",
                               innerRadius,
                               outerRadius,
                               halfHeight,
                               startAngle,
                               spanningAngle)

        logicDetector = G4LogicalVolume(solidDetector,
                                        detector_mat,
                                        "Detector")

        for i in range(9):
            angle = 90.0 * degree
            pos = G4ThreeVector(0, 0, 0)
            rot = G4RotationMatrix()
            rot.rotateY(angle)
            rot.rotateZ(i * -38.0 * degree)

            G4PVPlacement(rot,
                          pos,
                          logicDetector,
                          "Detector"+str(i+1),
                          logicWorld,
                          False,
                          i+1,
                          True)

        return physWorld


class RutherfordPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        self.fParticleGun = G4ParticleGun(1)

        # Default particle kinematic
        ParticleTable = G4ParticleTable.GetParticleTable()
        particle = ParticleTable.FindParticle("alpha")
        self.fParticleGun.SetParticleDefinition(particle)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, -1))
        self.fParticleGun.SetParticleEnergy(5*MeV)

    def GeneratePrimaries(self, anEvent):
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, 50*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class RutherfordRunAction(G4UserRunAction):

    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, run):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Particle_position.csv")

        AnalysisManager.CreateNtuple("step", "Step information")
        AnalysisManager.CreateNtupleIColumn("eventID")
        AnalysisManager.CreateNtupleDColumn("x (cm)")
        AnalysisManager.CreateNtupleDColumn("y (cm)")
        AnalysisManager.CreateNtupleDColumn("z (cm)")
        AnalysisManager.CreateNtupleIColumn("VolumeID")
        AnalysisManager.FinishNtuple()

    def EndOfRunAction(self, run):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()


class RutherfordSteppingAction(G4UserSteppingAction):

    def __init__(self):
        super().__init__()

    def UserSteppingAction(self, step):
        track = step.GetTrack()

        if track.GetVolume().GetName().startswith("Detector"):
            # Get the position at the end of the step
            position = step.GetPostStepPoint().GetPosition()
            eventID = G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
            VolumeID = step.GetPreStepPoint().GetTouchable().GetVolume().GetCopyNo()
            AnalysisManager = G4AnalysisManager.Instance()
            AnalysisManager.FillNtupleIColumn(0, eventID+1)
            AnalysisManager.FillNtupleDColumn(1, round(float(position.x)*0.1, 4))
            AnalysisManager.FillNtupleDColumn(2, round(float(position.y)*0.1, 4))
            AnalysisManager.FillNtupleDColumn(3, round(float(position.z)*0.1, 4))
            AnalysisManager.FillNtupleIColumn(4, VolumeID)
            AnalysisManager.AddNtupleRow(0)


class RutherfordActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(RutherfordRunAction())

    def Build(self):
        self.SetUserAction(RutherfordPrimaryGeneratorAction())
        self.SetUserAction(RutherfordRunAction())
        self.SetUserAction(RutherfordSteppingAction())


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

runManager.SetUserInitialization(RutherfordDetectorConstruction())

###########################################
############## Physics list ###############
###########################################

physicsList = QGSP_BERT()
runManager.SetUserInitialization(physicsList)

###########################################
####### User action initialization ########
###########################################

runManager.SetUserInitialization(RutherfordActionInitialization())


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
