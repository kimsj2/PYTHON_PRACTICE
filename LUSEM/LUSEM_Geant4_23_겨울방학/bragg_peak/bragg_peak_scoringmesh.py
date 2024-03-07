from geant4_pybind import *

import math
import sys


class baseDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        # Setting fScoringVolume
        # If you want to set the scoring for every each volume,
        # you can use the following code.
        self.fCheckOverlaps = True
        # self.fScoringVolume = None

        # you need to set the scoring volume in Construct() method
    
    def Construct(self):
        nist = G4NistManager.Instance()
        defaultMaterial = nist.FindOrBuildMaterial("G4_AIR")
        
        detector_sizeXY = 10*cm
        detector_sizeZ = 10*cm
        
        # world
        world_sizeXY = 1.2*detector_sizeXY
        world_sizeZ = 1.2*detector_sizeZ
        
        worldS = G4Box("World",
                           world_sizeXY/2,
                           world_sizeXY/2,
                           world_sizeZ/2)
        
        worldLV = G4LogicalVolume(worldS,
                                     defaultMaterial,
                                     "World")
        
        physWorld = G4PVPlacement(None,
                                  G4ThreeVector(0,0,0),
                                  worldLV,
                                  "World",
                                  None,
                                  False,
                                  0,
                                  self.fCheckOverlaps)  
        
        # detector - mesh
        detectorS = G4Box("detector", detector_sizeXY/2, detector_sizeXY/2,detector_sizeZ/2)
        
        detectorLV = G4LogicalVolume(worldS,
                                      defaultMaterial,
                                      "World")
        G4PVPlacement(None,
                      G4ThreeVector(0,0,0),
                      detectorLV ,
                      "detector",
                      worldLV,
                      False,
                      0,
                      self.fCheckOverlaps) 
        
        # scoring_mesh = G4MultiFunctionalDetector("ScoringMesh")
        # energyDeposit = G4PSEnergyDeposit("edep")
        # scoring_mesh.RegisterPrimitive(energyDeposit)
        # self.SetSensitiveDetector("ScoringMeshLV", scoring_mesh)
        
        # scoring_mesh_S =  G4Box("ScoringMesh", detector_sizeXY/2, detector_sizeXY/2,detector_sizeZ/2);
        # scoring_mesh_LV = G4LogicalVolume(scoring_mesh_S, defaultMaterial, "ScoringMeshLogical");
        
        # scoring_physical = G4PVPlacement(None,
        #                                   G4ThreeVector(0,0,0),
        #                                   scoring_mesh_LV,
        #                                   "ScoringMeshPhysical",
        #                                   worldLV,
        #                                   False,
        #                                   0,
        #                                   self.fCheckOverlaps)  
                
        # # Scoring Mesh에 물리 프로세스 추가 (예: 에너지 손실)
        # meshLV = mesh.ConstructLogicalVolume()
        # G4PVPlacement(0, G4ThreeVector(), meshLV, "ScoringVolume", worldLV, False, 0)
        
        # energyDeposit = G4PSEnergyDeposit("edep")
        # scoringMesh.RegisterPrimitive(energyDeposit)
        
        # # 물리 프로세스 매니저에 Scoring Mesh 등록
        # G4SDManager.GetSDMpointer().AddNewDetector(scoringMesh)
        # # self.SetSensitiveDetector("CrystalLV", cryst)
        
        # meshLV.SetVisAttributes(G4VisAttributes.GetInvisible())
        worldLV.SetVisAttributes(G4VisAttributes.GetInvisible())
        
        return  physWorld
        
    # def ConstructSDandField(self):
    #     G4SDManager.GetSDMpointer().SetVerboseLevel(1)

    #     # declare crystal as a MultiFunctionalDetector scorer
    #     box = G4MultiFunctionalDetector("box")
    #     G4SDManager.GetSDMpointer().AddNewDetector(box)

    #     primitiv1 = G4PSEnergyDeposit("edep")
    #     box.RegisterPrimitive(primitiv1)
    #     self.SetSensitiveDetector("BoxLV", box)
        
        

class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

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
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, -2.5*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)

class baseActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(baseRunAction())

    def Build(self):
        # initialization of actions
        self.SetUserAction(basePrimaryGeneratorAction())
        #self.SetUserAction(baseRunAction())
        #self.SetUserAction(baseEventAction())
        # self.SetUserAction(baseStackingAction())
        # self.SetUserAction(baseTrackingAction())
        # self.SetUserAction(baseSteppingAction())


class baseRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()
        G4RunManager.GetRunManager().SetPrintProgress(1)
        AnalysisManager = G4AnalysisManager.Instance()
        
        AnalysisManager.CreateNtuple("step", "Step information")
        AnalysisManager.CreateNtupleIColumn("eventID")
        AnalysisManager.CreateNtupleDColumn("step length (cm)")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        analysisManager.FinishNtuple()
        
    def BeginOfRunAction(self, aRun):
        analysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Particle_position_scoringmesh.csv")
        
    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()


class baseEventAction(G4UserEventAction):

    def __init__(self, scoring_mesh_data):
        super().__init__()
        self.scoring_mesh_data = scoring_mesh_data
        
    def BeginOfEventAction(self, anEvent):
        return

    def EndOfEventAction(self, anEvent):
        hce = anEvent.GetHCofThisEvent()
        if hce:
            scoring_mesh_hits_map = dynamic_cast(G4THitsMapG4double, hce.GetHC(0))

            # Access scoring mesh data and save it to the NumPy array
            if scoring_mesh_hits_map:
                num_entries = scoring_mesh_hits_map.entries()
                data_ptr = self.scoring_mesh_data.request().ptr

                for i in range(num_entries):
                    mesh_bin, energy_loss = scoring_mesh_hits_map[i]
                    
                    # Save energy loss to the NumPy array
                    data_ptr[mesh_bin] += energy_loss
        # scoring_manager = G4ScoringManager.GetScoringManager()
        # mesh_data = scoring_manager.GetScore(0)  # Assuming scoring mesh ID is 0

        # # Extract energy loss from each bin
        # for i in range(mesh_data.GetSize()):
        #     energy_loss = mesh_data.GetBinContent(i)
        #     self.scoring_mesh_data.append(energy_loss)
            
        
        AnalysisManager = G4AnalysisManager.Instance()
        eventID = G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
        
        AnalysisManager.FillNtupleIColumn(0, eventID+1)
        
        AnalysisManager.FillNtupleDColumn(1, stepLength)
        AnalysisManager.FillNtupleDColumn(2, energyDeposit)
        
        # AnalysisManager.AddNtupleRow(0)

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

runManager.SetUserInitialization(baseDetectorConstruction())

# ScoringManager = G4ScoringManager.GetScoringManager()

physicsList = QGSP_BERT()
runManager.SetUserInitialization(physicsList)

###########################################
####### User action initialization ########
###########################################

runManager.SetUserInitialization(baseActionInitialization())
scoringmesh = G4Sco
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
