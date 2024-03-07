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

    def Construct(self):
        nist = G4NistManager.Instance()

        # World - Galactic
        world_mat = nist.FindOrBuildMaterial("G4_AIR")
        world_sizeXY = 10*cm
        world_sizeZ = 10*cm

        solidWorld = G4Box("World", world_sizeXY, world_sizeXY, world_sizeZ)

        logicWorld = G4LogicalVolume(solidWorld, world_mat, "World")

        physWorld = G4PVPlacement(None,                 # no rotation
                                  G4ThreeVector(),      # at (0,0,0)
                                  logicWorld,           # its logical volume
                                  "World",              # its name
                                  None,                 # its mother volume
                                  False,                # no boolean operations
                                  0,                    # copy number
                                  True)   # overlaps checking

        # Detector - Air
        detector_mat = nist.FindOrBuildMaterial("G4_AIR")

        detector_sizeXY = 5*cm
        detector_sizeZ = 5*cm

        solidDetector = G4Box("Detector", detector_sizeXY, detector_sizeXY, detector_sizeZ)

        logicDetector = G4LogicalVolume(solidDetector,
                                        detector_mat,
                                        "Detector")
        
        
        G4PVPlacement(None,
                      G4ThreeVector(0, 0, 0),
                      logicDetector,
                      "Detector",
                      logicWorld,
                      False,
                      0,
                      True)
        
        # Visualization attributes
        logicWorld.SetVisAttributes(G4VisAttributes.GetInvisible())

        simpleBoxVisAtt = G4VisAttributes(G4Colour(1, 1, 1))
        simpleBoxVisAtt.SetVisibility(True)
        logicDetector.SetVisAttributes(simpleBoxVisAtt)
        
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

class BraggPeakActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        self.SetUserAction(BraggPeakRunAction())

    def Build(self):
        self.SetUserAction(BraggPeakPrimaryGeneratorAction())
        self.SetUserAction(BraggPeakRunAction())
        self.SetUserAction(BraggPeakSteppingAction())
        
        global pathLength
        pathLength = 0
        
        
class BraggPeakRunAction(G4UserRunAction):

    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Particle_position.csv")

        AnalysisManager.CreateNtuple("step", "Step information")
        AnalysisManager.CreateNtupleIColumn("eventID")
        AnalysisManager.CreateNtupleDColumn("Path length (cm)")
        AnalysisManager.CreateNtupleDColumn("step length (cm)")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV)")
        AnalysisManager.CreateNtupleDColumn("Total Energy (MeV)")
        
        AnalysisManager.FinishNtuple()

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

        # collect energy deposited in this step
        eventID = G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
        totEnergy = aStep.GetTrack().GetKineticEnergy()/MeV
        energyDeposit = aStep.GetTotalEnergyDeposit()/MeV
        lossEnergy = aStep.GetTotalEnergyDeposit()/MeV
        stepLength = aStep.GetStepLength()/cm
        
        global pathLength
        pathLength += stepLength
        
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.FillNtupleIColumn(0, eventID+1)
        AnalysisManager.FillNtupleDColumn(1, pathLength)
        AnalysisManager.FillNtupleDColumn(2, stepLength)
        AnalysisManager.FillNtupleDColumn(3, lossEnergy)
        AnalysisManager.FillNtupleDColumn(4, totEnergy)
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
