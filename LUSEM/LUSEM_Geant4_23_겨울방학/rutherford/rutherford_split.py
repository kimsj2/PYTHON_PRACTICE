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

        solidWorld = G4Box("World", world_sizeXY,world_sizeXY, world_sizeZ)

        logicWorld = G4LogicalVolume(solidWorld, world_mat, "World")

        physWorld = G4PVPlacement(None,                 # no rotation
                                  G4ThreeVector(),      # at (0,0,0)
                                  logicWorld,           # its logical volume
                                  "World",              # its name
                                  None,                 # its mother  volume
                                  False,                # no boolean operations
                                  0,                    # copy number
                                  True)   # overlaps checking

        # Target - Thin foil of gold
        foil_mat = nist.FindOrBuildMaterial("G4_Au")
        foil_sizeXY = 10*cm
        foil_sizeZ = 1*um

        solidFoil = G4Box("Target", foil_sizeXY,
                          foil_sizeXY, foil_sizeZ)

        logicFoil = G4LogicalVolume(solidFoil, foil_mat, "Target")

        G4PVPlacement(None,                 # no rotation
                      G4ThreeVector(),      # at (0,0,0)
                      logicFoil,           # its logical volume
                      "Target",             # its name
                      logicWorld,           # its mother  volume
                      False,                # no boolean operations
                      0,                    # copy number
                      True)   # overlaps checking

        # Detector - Silicon
        
        shape_mat = nist.FindOrBuildMaterial("G4_CESIUM_IODIDE")
        
        innerRadius = 49.0*cm
        outerRadius = 50.0*cm # 반지름을 조절하여 얇은 판의 크기 조절
        halfHeight = 40*cm # 얇은 판의 높이 조절
        startAngle = 5.0 *degree
        spanningAngle = 50.0*degree
        
        solidShape = G4Tubs("FluorescentScreen", innerRadius, outerRadius, 
                            halfHeight, startAngle, spanningAngle)

        # 형광 스크린의 논리체 생성
        logicShape = G4LogicalVolume(solidShape, shape_mat,"FluorescentScreen")

        # 형광 스크린을 원하는 위치에 배치
        for i in range(7):
            rotation_matrix = G4RotationMatrix()
            rotation_matrix.rotateY(90.0 * degree)
            rotation_matrix.rotateZ(i * -50.0 * degree)
            
            G4PVPlacement(rotation_matrix,
                          G4ThreeVector(0, 0, 0),
                          logicShape,
                          "FluorescentScreen" + str(i),
                          logicWorld,
                          False,
                          i,  # copy number를 유니크하게 설정
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
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, -50*cm))
        self.fParticleGun.SetParticleEnergy(5*MeV)

    def GeneratePrimaries(self, anEvent):
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0,50*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class RutherfordRunAction(G4UserRunAction):

    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, run):
        # print("### Run {} start.".format(run.GetRunID()))
        return

    def EndOfRunAction(self, run):
        # print("### Run {} end.".format(run.GetRunID()))
        return

class RutherfordEventAction(G4UserEventAction):

    def __init__(self):
        super().__init__()

    def BeginOfEventAction(self, event):
        # print("### Event {} start.".format(event.GetEventID()))
        return
    
    def EndOfEventAction(self, event):
        # print("### Event {} end.".format(event.GetEventID()))
        return

class RutherfordSteppingAction(G4UserSteppingAction):

    def __init__(self):
        super().__init__()

    def UserSteppingAction(self, step):
        # print("### Stepping action.")
        return


class RutherfordActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(RutherfordRunAction())

    def Build(self):
        self.SetUserAction(RutherfordPrimaryGeneratorAction())
        self.SetUserAction(RutherfordRunAction())
        self.SetUserAction(RutherfordEventAction())
        self.SetUserAction(RutherfordSteppingAction()) # need to fix


# Start of the simulation
ui = None

if len(sys.argv) == 1:
    ui = G4UIExecutive(len(sys.argv), sys.argv)

# optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

# Construct the default run manager
runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

####### User initialization classes #######
runManager.SetUserInitialization(RutherfordDetectorConstruction())

####### Physics list #######
physicsList = QGSP_BERT()
physicsList.SetVerboseLevel(1)

runManager.SetUserInitialization(physicsList)

####### User action initialization ########
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
