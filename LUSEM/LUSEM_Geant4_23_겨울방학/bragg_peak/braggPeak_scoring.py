# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:44:24 2024

@author: kimsj
"""

from geant4_pybind import *

import math
import sys


class BraggPeakDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        
    
    def DefineMaterials(self):
        nist = G4NistManager.Instance()
        nist.FindOrBuildMaterial("G4_AIR")
    
    def DefineVolumes(self):
        
        nofLayers = 500
        
        absoThickness = 0.1*mm
        gapThickness = 0.1*mm
        
        layerThickness = absoThickness + gapThickness
        
        detectorSizeXY = 10*cm
        
        detectorThickness = nofLayers * layerThickness
        worldSizeXY = 1.2 * detectorSizeXY
        worldSizeZ = 1.2 * detectorThickness

        defaultMaterial = G4Material.GetMaterial("G4_AIR")
        
        # World - Galactic
        
        solidWorld = G4Box("World", worldSizeXY/2, worldSizeXY/2, worldSizeZ/2)
        
        logicWorld = G4LogicalVolume(solidWorld, defaultMaterial, "World")
        
        physWorld = G4PVPlacement(None,                 # no rotation
                                  G4ThreeVector(0,0,0),      # at (0,0,0)
                                  logicWorld,           # its logical volume
                                  "World",              # its name
                                  None,                 # its mother volume
                                  False,                # no boolean operations
                                  0,                    # copy number
                                  True)   # overlaps checking

        # env - Air
        envS = G4Box("Env", detectorSizeXY/2, detectorSizeXY/2, detectorThickness/2)
        
        envLV = G4LogicalVolume(envS,
                                        defaultMaterial,
                                        "Env")
        
        G4PVPlacement(None,
                      G4ThreeVector(0, 0, 0),
                      envLV,
                      "Env",
                      logicWorld,
                      False,
                      0,
                      True)
        
        # Layer - Air
        
        layerS = G4Box("Layer",                                         # its name
                       detectorSizeXY/2, detectorSizeXY/2, layerThickness/2)  # its size
        
        layerLV = G4LogicalVolume(layerS,           # its solid
                                  defaultMaterial,  # its material
                                  "Layer")          # its name
        
        # Create and set sensitive detector
        # sensitiveDetector = G4VSensitiveDetector("MySensitiveDetector")
        # layerLV.SetSensitiveDetector(sensitiveDetector)
        # G4SDManager.GetSDMpointer().AddNewDetector(sensitiveDetector)
        
        G4PVReplica("Layer",         # its name
                    layerLV,         # its logical volume
                    envLV,         # its mother
                    kZAxis,          # axis of replication
                    nofLayers,       # number of replica
                    layerThickness)  # width of replica
        
        # Absorber

        absorberS = G4ScoringBox("Abso",                                         # its name
                          detectorSizeXY/2, detectorSizeXY/2, absoThickness/2)  # its size

        absorberLV = G4LogicalVolume(absorberS,         # its solid
                                     defaultMaterial,  # its material
                                     "Abso")            # its name

        self.fAbsorberPV = G4PVPlacement(None,                                  # no rotation
                                         G4ThreeVector(0, 0,-gapThickness/2),  # its position
                                         absorberLV,                            # its logical volume
                                         "Abso",                                # its name
                                         layerLV,                               # its mother  volume
                                         False,                                 # no boolean operation
                                         0,                                     # copy number
                                         True)                   # checking overlaps
        # Gap
        gapS = G4Box("Gap",                                         # its name
                     detectorSizeXY/2, detectorSizeXY/2, gapThickness/2)  # its size

        gapLV = G4LogicalVolume(gapS,         # its solid
                                defaultMaterial,  # its material
                                "Gap")        # its name

        self.fGapPV = G4PVPlacement(None,                                  # no rotation
                                    G4ThreeVector(0, 0, absoThickness/2),  # its position
                                    gapLV,                                 # its logical volume
                                    "Gap",                                 # its name
                                    layerLV,                               # its mother volume
                                    False,                                 # no boolean operation
                                    0,                                     # copy number
                                    True)                   # checking overlaps

        # Visualization attributes
        logicWorld.SetVisAttributes(G4VisAttributes.GetInvisible())
        
        simpleBoxVisAtt = G4VisAttributes(G4Colour(1, 1, 1))
        simpleBoxVisAtt.SetVisibility(True)
        envLV.SetVisAttributes(simpleBoxVisAtt)
        
        return physWorld

    def Construct(self):
        self.DefineMaterials()
        return self.DefineVolumes()

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
        self.fParticleGun.SetParticlePosition(G4ThreeVector(0, 0, -2.5*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)

class BraggPeakActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(BraggPeakRunAction())
        
    def Build(self):
        self.SetUserAction(BraggPeakPrimaryGeneratorAction())
        self.SetUserAction(BraggPeakRunAction())
        self.SetUserAction(BraggPeakSteppingAction())
        
        
        
class BraggPeakRunAction(G4UserRunAction):

    def __init__(self):
        super().__init__()
        AnalysisManager = G4AnalysisManager.Instance()
        

        AnalysisManager.CreateNtuple("step", "Step information")
        AnalysisManager.CreateNtupleIColumn("eventID")
        AnalysisManager.CreateNtupleDColumn("step length (cm)")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        AnalysisManager.CreateNtupleDColumn("Total Energy (MeV)")
        
        AnalysisManager.FinishNtuple()
        
    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Particle_position_scoring.csv")
        
    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()
        

class BraggPeakEventAction(G4UserEventAction):
    def __init__(self):
        super().__init__()
        
    def BeginOfEventAction(self, anEvent):
        pass

    def EndOfEventAction(self, anEvent):
        pass
    

class BraggPeakTrackingAction(G4UserTrackingAction):

    def __init__(self):
        super().__init__()

    def PreUserTrackingAction(self, aTrack):
        pass

    def PostUserTrackingAction(self, aTrack):
        pass


class BraggPeakSteppingAction(G4UserSteppingAction):

    def __init__(self):
        super().__init__()
        
    def UserSteppingAction(self, aStep):
        
        volume = aStep.GetPreStepPoint().GetTouchable().GetVolume().GetLogicalVolume()
        
        # Check if the particle hit the sensitive detector
        touchable = aStep.GetPreStepPoint().GetTouchable()
        # if touchable and touchable.GetVolume(touchable.GetHistoryDepth()).IsSensitiveDetector():
            # Get the scoring volume (Detector)
        stepLength = aStep.GetStepLength()
        
        # collect energy deposited in this step
        eventID = G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
        totEnergy = aStep.GetTrack().GetKineticEnergy()/MeV
    
        energyDeposit = aStep.GetTotalEnergyDeposit()/MeV
    
        lossEnergy = aStep.GetTotalEnergyDeposit()/MeV
        stepLength = aStep.GetStepLength()/cm
    
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.FillNtupleIColumn(0, eventID+1)
        AnalysisManager.FillNtupleDColumn(1, stepLength)
        AnalysisManager.FillNtupleDColumn(2, lossEnergy)
        AnalysisManager.FillNtupleDColumn(3, totEnergy)
        AnalysisManager.AddNtupleRow(0)

class BraggPeakStackingAction(G4UserStackingAction):

    def __init__(self):
        super().__init__()

    def ClassifyNewTrack(self, aTrack):
        pass

    def NewStage(self):
        pass

    def PrepareNewEvent(self):
        pass


# Start of the simulation
ui = None

if len(sys.argv) == 1:
    ui = G4UIExecutive(len(sys.argv), sys.argv)

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

# User initialization
runManager.SetUserInitialization(BraggPeakDetectorConstruction())
physicsList = QGSP_BERT()
runManager.SetUserInitialization(physicsList)

# User action initialization
runManager.SetUserInitialization(BraggPeakActionInitialization())

# Initialize visualization
visManager = G4VisExecutive()
visManager.Initialize()

# Get the User Interface manager
UImanager = G4UImanager.GetUIpointer()

# Process macro or start UI session
if ui is None:
    # batch mode
    command = "/control/execute "
    fileName = sys.argv[1]
    UImanager.ApplyCommand(command + fileName)
else:
    # interactive mode
    UImanager.ApplyCommand("/control/execute init_vis.mac")
    ui.SessionStart()