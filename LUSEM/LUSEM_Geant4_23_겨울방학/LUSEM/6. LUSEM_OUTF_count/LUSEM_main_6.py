from geant4_pybind import *

import pandas as pd
import numpy as np
import math
import sys


class LUSEMDetectorConstruction(G4VUserDetectorConstruction):

    def __init__(self):
        super().__init__()
        self.world = None
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO',
                     ' BF', 'BT2', 'BT1', 'BU2', 'BU1', 'BO']
        self.Dets_LV = ['d1_VF_si', 'd1_VT6_si', 'd1_VT4_si', 'd1_VT3_si', 'd1_VT1_si',
                        'd1_VO_si', 'd2_VF_si', 'd2_VT6_si', 'd2_VT4_si', 'd2_VT3_si', 'd2_VT1_si', 'd2_VO_si']

    def Construct(self):
        self.gdml_parser = G4GDMLParser()
        file = '20220928_LUSEM_FREECAD_VER0.91.gdml'
        self.gdml_parser.Read(file)
        self.world = self.gdml_parser.GetWorldVolume()

        # Set color of the detector
        visAtt = G4VisAttributes(G4Colour(1, 1, 0))

        for i in range(len(self.Dets_LV)):
            LV = self.gdml_parser.GetVolume(self.Dets_LV[i])
            LV.SetVisAttributes(visAtt)

        # Set Structure invisible
        visAttributes = G4VisAttributes(G4Colour(1, 1, 1))
        visAttributes.SetVisibility(False)

        for i in range(131):

            if i == 7 or i == 11 or i == 12 or i == 14:
                continue

            if i == 105 or i == 108 or i == 110 or i == 114:
                continue

            Structure_name = f"Element_step_{i}__vol"
            LV = self.gdml_parser.GetVolume(Structure_name)
            LV.SetVisAttributes(visAttributes)

        return self.world

    def ConstructSDandField(self):
        for i in range(len(self.Dets)):
            # The string within is the name to be called in later analysis
            SD = G4MultiFunctionalDetector(f"Det_{self.Dets[i]}")
            G4SDManager.GetSDMpointer().AddNewDetector(SD)
            primitive = G4PSEnergyDeposit("Edep")
            SD.RegisterPrimitive(primitive)
            self.SetSensitiveDetector(self.Dets_LV[i], SD)

        # Set magnetic field
        magfield = MagneticField()
        self.fMagneticField = magfield

        FieldMgr = G4TransportationManager.GetTransportationManager().GetFieldManager()
        FieldMgr.SetDetectorField(magfield)
        FieldMgr.CreateChordFinder(magfield)
        pass

        return


class MagneticField(G4MagneticField):

    def __init__(self):
        super().__init__()
        file = 'B_field_sorted.txt'
        df = pd.read_csv(file, sep=',')

        self.xq = np.unique(df.iloc[:, 0].to_numpy())
        self.yq = np.unique(df.iloc[:, 1].to_numpy())
        self.zq = np.unique(df.iloc[:, 2].to_numpy())

        self.xq_min = self.xq.min()
        self.xq_max = self.xq.max()
        self.yq_min = self.yq.min()
        self.yq_max = self.yq.max()
        self.zq_min = self.zq.min()
        self.zq_max = self.zq.max()

        nx = len(self.xq)
        ny = len(self.yq)
        nz = len(self.zq)

        self.bx = np.reshape(
            df.iloc[:, 3].to_numpy(), (nx, ny, nz), order='C')*tesla
        self.by = np.reshape(
            df.iloc[:, 4].to_numpy(), (nx, ny, nz), order='C')*tesla
        self.bz = np.reshape(
            df.iloc[:, 5].to_numpy(), (nx, ny, nz), order='C')*tesla

    # points given from outside, Bfield to be returned by this class
    def GetFieldValue(self, point, Bfield):

        def find_near_grids(a, x):
            i0 = np.abs(a - x).argmin()
            i1 = i0 + 1 if (x - a[i0]) >= 0 else i0 - 1
            # return np.sort([i0, i1])
            return [i0, i1]

        # interpolate scalar function f given on grid x, y, z for pts
        def linear_3Dint(x, y, z, f, pts):
            [i0, i1] = find_near_grids(x, pts[0])
            [j0, j1] = find_near_grids(y, pts[1])
            [k0, k1] = find_near_grids(z, pts[2])

            f1 = f[i0, j0, k0] + (f[i1, j0, k0] - f[i0, j0, k0])/(x[i1]-x[i0])*(pts[0]-x[i0])  \
                + (f[i0, j1, k0] - f[i0, j0, k0])/(y[j1]-y[j0])*(pts[1]-y[j0])  \
                + (f[i0, j0, k1] - f[i0, j0, k0])/(z[k1]-z[k0])*(pts[2]-z[k0])
            return f1

        x = point[0]*mm
        y = point[1]*mm
        z = point[2]*mm
        pts = [x, y, z]

        # No electric field
        Bfield[3] = 0.
        Bfield[4] = 0.
        Bfield[5] = 0.

        IntheVolumeX = self.xq_min < x < self.xq_max
        IntheVolumeY = self.yq_min < y < self.yq_max
        IntheVolumeZ = self.zq_min < z < self.zq_max
        IntheVolume = IntheVolumeX and IntheVolumeY and IntheVolumeZ

        if IntheVolume:
            Bfield[0] = linear_3Dint(self.xq, self.yq, self.zq, self.bx, pts)
            Bfield[1] = linear_3Dint(self.xq, self.yq, self.zq, self.by, pts)
            Bfield[2] = linear_3Dint(self.xq, self.yq, self.zq, self.bz, pts)

        else:
            Bfield[0] = 0.*tesla
            Bfield[1] = 0.*tesla
            Bfield[2] = 0.*tesla


class LUSEMPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        self.fParticleGun = G4ParticleGun()

        ParticleTable = G4ParticleTable.GetParticleTable()
        self.electron = ParticleTable.FindParticle("e-")
        self.proton = ParticleTable.FindParticle("proton")


    def GeneratePrimaries(self, anEvent):
        self.fParticleGun.SetParticleDefinition(self.electron)
        particle_df.loc[anEvent.GetEventID(), 'Particle'] = self.fParticleGun.GetParticleDefinition().GetParticleName()

        Emin = 10*keV
        Emax = 10000*keV
        Ep = Emin + G4UniformRand()*(Emax - Emin)
        self.fParticleGun.SetParticleEnergy(Ep)
        particle_df.loc[anEvent.GetEventID(), 'Incident'] = round(Ep/keV, 4)
        
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0, 0, -1))
        
        # proton : -3.0 cm
        # electron : 7.0 cm
        self.fParticleGun.SetParticlePosition(G4ThreeVector(-25.0*mm, -12.48*mm, 6.0*cm))
        self.fParticleGun.GeneratePrimaryVertex(anEvent)


class LUSEMActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(LUSEMRunAction())

    def Build(self):
        # initialization of actions
        self.SetUserAction(LUSEMPrimaryGeneratorAction())
        self.SetUserAction(LUSEMRunAction())
        self.SetUserAction(LUSEMEventAction())


col_p=['Particle', 'Incident', 'Detected', 'Config', 'AF', 'AT2', 'AT1', 'AU2','AU1', 'AO']
particle_df = pd.DataFrame(columns=col_p)


col_bin = ['F', 'FT', 'FTU', 'FTUO', 'O', 'OU', 'OUT', 'OUTF']

bin_df = pd.DataFrame(index=range(10001), columns=col_bin)
bin_df.fillna(0, inplace=True)

# bin_2D = pd.DataFrame(index=range(10001), columns=range(10001))
# bin_2D.fillna(0, inplace=True)


class LUSEMRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data

    def __init__(self):
        super().__init__()

    def EndOfRunAction(self, aRun):
        # Starts at the end of a run
        particle_df.to_csv('LUSEM_tot.csv', index=False)
        bin_df.to_csv('LUSEM_bin.csv', index=False)
        return


class LUSEMEventAction(G4UserEventAction):
    # Can be used when you use sensitive detector

    def __init__(self):
        super().__init__()
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1','AO']
        self.init_energy = 0

    def EndOfEventAction(self, anEvent):
        # Extract the data from each hit and write it to a file
        config = ""
        O = 0
        U = 0
        T = 0
        F = 0

        for i in range(len(self.Dets)):
            self.HCID = G4SDManager.GetSDMpointer().GetCollectionID(
                f"Det_{self.Dets[i]}/Edep")
            hc = anEvent.GetHCofThisEvent().GetHC(self.HCID)

            for id, edep in hc:
                particle_df.loc[anEvent.GetEventID(), self.Dets[i]] = edep/keV

                if self.Dets[i] == 'AO':
                    O += edep/keV
                    config += 'O'

                elif self.Dets[i] == 'AU1' or self.Dets[i] == 'AU2':
                    U += edep/keV
                    if 'U' not in config:
                        config += 'U'

                elif self.Dets[i] == 'AT1' or self.Dets[i] == 'AT2':
                    T += edep/keV
                    if 'T' not in config:
                        config += 'T'

                elif self.Dets[i] == 'AF':
                    F += edep/keV
                    config += 'F'

        total_detect = O + U + T + F
        particle_df.loc[anEvent.GetEventID(), 'Detected'] = round(total_detect, 4)
        
        
        if particle_df.loc[anEvent.GetEventID(), 'Particle'] == 'proton':
            particle_df.loc[anEvent.GetEventID(), 'Config'] = config[::-1]

            if config[::-1] == 'O':    
                bin_df.loc[math.ceil(round(total_detect, 4)), 'O'] += 1
            elif config[::-1] == 'OU':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'OU'] += 1
            elif config[::-1] == 'OUT':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'OUT'] += 1
            elif config[::-1] == 'OUTF':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'OUTF'] += 1
        
        else:
            particle_df.loc[anEvent.GetEventID(), 'Config'] = config

            if config == 'F':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'F'] += 1
            elif config == 'FT':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'FT'] += 1
            elif config == 'FTU':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'FTU'] += 1
            elif config == 'FTUO':
                bin_df.loc[math.ceil(round(total_detect, 4)), 'FTUO'] += 1

        return


class LUSEMSteppingAction(G4UserSteppingAction):
    
        def __init__(self):
            super().__init__()
    
        def UserSteppingAction(self, aStep):
            return


def runBatch(n_events):
    # Construct the default run manager
    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

    # Detector construction
    runManager.SetUserInitialization(LUSEMDetectorConstruction())
    # Physics list
    # proton => FTFP_BERT
    # electron => QGSP_BERT
    # alpha => QGSP_BERT
    physicsList = QGSP_BERT()
    runManager.SetUserInitialization(physicsList)
    # Particle generator
    runManager.SetUserInitialization(LUSEMActionInitialization())

    runManager.Initialize()

    # Get the User Interface manager
    UImanager = G4UImanager.GetUIpointer()

    UImanager.ApplyCommand("/run/verbose 0")
    UImanager.ApplyCommand("/event/verbose 0")

    # Start a run with ray
    runManager.BeamOn(n_events)

    return


def runGUI():
    # Start of the simulation
    ui = None

    if len(sys.argv) == 1:
        ui = G4UIExecutive(len(sys.argv), sys.argv)


    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

    runManager.SetUserInitialization(LUSEMDetectorConstruction())

    # proton => FTFP_BERT
    # electron => QGSP_BERT
    # alpha => QGSP_BERT
    physicsList = QGSP_BERT()
    runManager.SetUserInitialization(physicsList)

    runManager.SetUserInitialization(LUSEMActionInitialization())


    # Initialize visualization
    visManager = G4VisExecutive()
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

    return


runBatch(100000)

# Random Energy / range : 10-10000 keV
#  1,000 : 43s
# 10,000 : 
#100,000 : 59m 25s