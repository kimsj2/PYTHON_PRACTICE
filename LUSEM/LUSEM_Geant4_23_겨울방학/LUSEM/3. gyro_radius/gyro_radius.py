from geant4_pybind import *
import sys
import pandas as pd
import math


class baseDetectorConstruction(G4VUserDetectorConstruction):
 
    def __init__(self):
        super().__init__()

    def Construct(self):
        nist = G4NistManager.Instance()

        # World - Air
        world_mat = nist.FindOrBuildMaterial("G4_Galactic")
        world_sizeXY = 101*m
        world_sizeZ = 101*m

        solidWorld = G4Box("World", world_sizeXY, world_sizeXY, world_sizeZ)

        logicWorld = G4LogicalVolume(solidWorld, world_mat, "World")

        physWorld = G4PVPlacement(None,                 # no rotation
                                  G4ThreeVector(),      # at (0,0,0)
                                  logicWorld,           # its logical volume
                                  "World",              # its name
                                  None,                 # its mother  volume
                                  False,                # no boolean operations
                                  0,                    # copy number
                                  True)   # overlaps checking


        # Detector - Silicon
        detector_mat = nist.FindOrBuildMaterial("G4_Galactic")
        detector_sizeXY = 100*m
        detector_sizeZ = 100*m

        detectorS = G4Box("Detector", detector_sizeXY, detector_sizeXY, detector_sizeZ)

        detectorLV = G4LogicalVolume(detectorS, detector_mat, "DetectorLV")

        G4PVPlacement(None,                 # no rotation
                      G4ThreeVector(),      # at (0,0,0)
                      detectorLV,           # its logical volume
                      "Detector",              # its name
                      logicWorld,                 # its mother  volume
                      False,                # no boolean operations
                      0,                    # copy number
                      True)   # overlaps checking
        
        detectorLV.SetVisAttributes(G4VisAttributes.GetInvisible())
        
        return physWorld
        
    def ConstructSDandField(self):
        # global magnetic field
        fieldValue = G4ThreeVector(0,0.2*tesla,0)
        self.fMagFieldMessenger = G4GlobalMagFieldMessenger(fieldValue)
        self.fMagFieldMessenger.SetVerboseLevel(1)

class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        
        # proton & telescope A
        self.fParticleGun = G4ParticleGun(1)
        self.particle_energy = 1*MeV
        ParticleTable = G4ParticleTable.GetParticleTable()
        self.proton = ParticleTable.FindParticle("proton")
        self.fParticleGun.SetParticleDefinition(self.proton)
        # self.electron = ParticleTable.FindParticle("e-")
        # self.fParticleGun.SetParticleDefinition(self.electron)
        
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,-2,1))
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0,0,0))
        self.fParticleGun.SetParticleEnergy(self.particle_energy)
        
        
    def GeneratePrimaries(self, anEvent):
        particle = self.proton
        self.fParticleGun.SetParticleDefinition(particle)
        self.fParticleGun.SetParticleEnergy(self.particle_energy)
        # original
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0,0,0))
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
        self.SetUserAction(baseEventAction(runAction))
        # self.SetUserAction(baseStackingAction())
        # self.SetUserAction(baseTrackingAction())
        # self.SetUserAction(baseSteppingAction())
        
        
class baseRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()
        self.Dets = ['particle_name', 'magnetic_field', 'momentum','gyro_radius']
        self.dataframe = pd.DataFrame(columns=self.Dets)
        
    def EndOfRunAction(self, aRun):
        self.dataframe.to_csv('Gyro_radius.csv', index=False)
        
        
class baseEventAction(G4UserEventAction):

    def __init__(self,runAction):
        super().__init__()
        self.fCollID_SD = []
        self.Dets = ['particle_name', 'magnetic_field', 'momentum','gyro_radius']
        self.runAction = runAction
        
        
    def EndOfEventAction(self, anEvent):
        generatorAction = G4RunManager.GetRunManager().GetUserPrimaryGeneratorAction()
        particle = generatorAction.fParticleGun.GetParticleDefinition()
        partName = particle.GetParticleName()
        
        # particle_definition = G4ParticleTable.GetParticleTable().FindParticle("proton")
        # particle_charge = particle_definition.GetPDGCharge()
        
        event_id = anEvent.GetEventID()
        
        
        particle_m = anEvent.GetPrimaryVertex().GetPrimary(0)
        momentum = particle_m.GetMomentum()
        momentum_z = momentum.getZ()
        
        particle_charge = 1.602*1e-19
        momentum_z = momentum_z/particle_charge
        gyro_radius = momentum_z/ (particle_charge*0.2*tesla)
        self.runAction.dataframe.loc[event_id,'particle_name'] = partName
        self.runAction.dataframe.loc[event_id,'magnetic_field'] = 0.2*tesla
        self.runAction.dataframe.loc[event_id,'momentum'] = momentum
        self.runAction.dataframe.loc[event_id,'gyro_radius'] = gyro_radius
        
        

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

