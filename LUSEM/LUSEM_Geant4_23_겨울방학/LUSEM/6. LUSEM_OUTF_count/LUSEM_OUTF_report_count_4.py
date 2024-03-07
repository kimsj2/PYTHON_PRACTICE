from geant4_pybind import *
import sys
import pandas as pd
import numpy as np
import random
import datetime

Emin = 10
Emax = 10000
Ebin = 1

logiclist = ['F','T','U','O','FT','FU','FO','TU','TO','UO','FTU','FTO','FUO','TUO','FTUO']
Dets = ['particle_name', 'config','Incident_energy','Detected_energy','start_time','end_time','total_time']
dataframe = pd.DataFrame(columns=Dets)
dataframe_logiclist = {}

columns = ['F','T','U','O']
rightlogic = ['F','O','FT','UO','FTU','TUO','FTUO']

for x in logiclist:
    index_values = [str(Emin + i) for i in range(0, Emax - Emin + 1, Ebin)]
    data = np.zeros((len(index_values), len(columns)))
    dataframe_logiclist[x] = pd.DataFrame(data,columns=columns, index=index_values)


class MyDetectorConstruction(G4VUserDetectorConstruction):
 
    def __init__(self):
        super().__init__()
        self.world= None
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO',' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO']
        self.Dets_LV = ['d1_VF_si', 'd1_VT6_si','d1_VT4_si', 'd1_VT3_si','d1_VT1_si', 'd1_VO_si',
                   'd2_VF_si', 'd2_VT6_si','d2_VT4_si', 'd2_VT3_si','d2_VT1_si', 'd2_VO_si']
 
    def Construct(self):
        self.gdml_parser= G4GDMLParser()
        file = '20220928_LUSEM_FREECAD_VER0.91.gdml'
        self.gdml_parser.Read(file)
        self.world = self.gdml_parser.GetWorldVolume()
        # only see detector
        visual = G4VisAttributes()
        visual.SetVisibility(False)

        for i in range(131):
            if i==7 or i==11 or i ==12 or i ==14:
                continue
            
            # if i in range(102, 117):
            #     continue
            if i==105 or i==108 or i ==110 or i ==114:
                continue

            lv = self.gdml_parser.GetVolume(f"Element_step_{i}__vol")
            lv.SetVisAttributes(visual)
        
        return self.world
 
    def ConstructSDandField(self):
        for i in range(len(self.Dets)):
            SD =  G4MultiFunctionalDetector(f"Det_{self.Dets[i]}") # The string within is the name to be called in later analysis
            G4SDManager.GetSDMpointer().AddNewDetector(SD)
            primitive = G4PSEnergyDeposit("Edep")
            SD.RegisterPrimitive(primitive)
            self.SetSensitiveDetector(self.Dets_LV[i], SD)
 
        magfield =  MagneticField()
        self.fMagneticField = magfield
        globalFieldMgr =  G4TransportationManager.GetTransportationManager().GetFieldManager()
        self.fFieldMgr = globalFieldMgr
        self.fFieldMgr.SetDetectorField(magfield)
        self.fFieldMgr.CreateChordFinder(magfield)
        

        
class MagneticField(G4MagneticField):
 
    def __init__(self):
        super().__init__()
        file = 'B_field_sorted.txt'
        df =  pd.read_csv(file,sep=',')
 
        self.xq = np.unique(df.iloc[:,0].to_numpy())
        self.yq = np.unique(df.iloc[:,1].to_numpy())
        self.zq = np.unique(df.iloc[:,2].to_numpy())
 
        self.xq_min = self.xq.min()
        self.xq_max = self.xq.max()
        self.yq_min = self.yq.min()
        self.yq_max = self.yq.max()
        self.zq_min = self.zq.min()
        self.zq_max = self.zq.max()
 
        nx = len(self.xq)
        ny = len(self.yq)
        nz = len(self.zq)
 
        self.bx = np.reshape(df.iloc[:,3].to_numpy(), (nx,ny,nz), order='C')*tesla
        self.by = np.reshape(df.iloc[:,4].to_numpy(), (nx,ny,nz), order='C')*tesla
        self.bz = np.reshape(df.iloc[:,5].to_numpy(), (nx,ny,nz), order='C')*tesla
 
    def GetFieldValue(self, point, Bfield): # points given from outside, Bfield to be returned by this class
 
        def find_near_grids (a, x):
            i0 =  np.abs(a - x).argmin()
            i1 =  i0 + 1 if (x - a[i0]) >= 0 else i0 - 1
            #return np.sort([i0, i1])
            return [i0, i1]
 
        def linear_3Dint(x, y, z, f, pts): # interpolate scalar function f given on grid x, y, z for pts
            [i0,i1] = find_near_grids(x, pts[0])
            [j0,j1] = find_near_grids(y, pts[1])
            [k0,k1] = find_near_grids(z, pts[2])
 
            f1 = f[i0,j0,k0] + (f[i1,j0,k0] - f[i0,j0,k0])/(x[i1]-x[i0])*(pts[0]-x[i0])  \
                            +  (f[i0,j1,k0] - f[i0,j0,k0])/(y[j1]-y[j0])*(pts[1]-y[j0])  \
                            +  (f[i0,j0,k1] - f[i0,j0,k0])/(z[k1]-z[k0])*(pts[2]-z[k0])
            return f1
 
        x = point[0]*mm
        y = point[1]*mm
        z = point[2]*mm
        pts = [x,y,z]
 
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
            

class MyPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        
        # proton & telescope A
        self.fParticleGun = G4ParticleGun(1)
        
        # self.Emin = 10 *keV
        # self.Emax = 10000 *keV
        particle_energy = Emin*keV + G4UniformRand()*((Emax*keV-Emin*keV))
        
        # Default particle kinematic (electron)
        ParticleTable = G4ParticleTable.GetParticleTable()
        self.electron = ParticleTable.FindParticle("e-")
        self.fParticleGun.SetParticleDefinition(self.electron)
        
        # (telescope A / F)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 75*mm))
        self.fParticleGun.SetParticleEnergy(particle_energy)
        
    def GeneratePrimaries(self, anEvent):
        self.fParticleGun.SetParticleDefinition(self.electron)
        particle_energy = Emin*keV + G4UniformRand()*((Emax*keV-Emin*keV))
        self.fParticleGun.SetParticleEnergy(particle_energy)
        dataframe.loc[anEvent.GetEventID(), 'Incident_energy'] = particle_energy/keV
        
        # # F or O
        # i = int(2 * G4UniformRand())
        # if i == 0:
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 75*mm))
        # else:
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, -47*mm))

        self.fParticleGun.GeneratePrimaryVertex(anEvent)

class MyActionInitialization(G4VUserActionInitialization):

    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(MyRunAction())

    def Build(self):
        # initialization of actions
        self.SetUserAction(MyPrimaryGeneratorAction())
        runAction = MyRunAction()
        self.SetUserAction(runAction)
        self.SetUserAction(MyEventAction())
        # self.SetUserAction(MyStackingAction())
        # self.SetUserAction(MyTrackingAction())
        # self.SetUserAction(MySteppingAction())
        

class MyRunAction(G4UserRunAction):
    # Define what to do at the beginning and end of a run
    # Can be used to save data
    def __init__(self):
        super().__init__()
        # self.Dets = ['particle_name', 'config','Incident_energy','Detected_energy'] # ' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO'
        
    def BeginOfRunAction(self, aRun):
        self.start_time = datetime.datetime.now()
        dataframe.loc[0, 'start_time'] = str(self.start_time)
        
    def EndOfRunAction(self, aRun):
        for x in logiclist:
            if x in rightlogic:
                dataframe_logiclist[x].to_csv(f'detail_data/right_logic/LUSEM_electron_{x}.csv')
            else:
                dataframe_logiclist[x].to_csv(f'detail_data/wrong_logic/LUSEM_electron_{x}.csv')
        self.end_time = datetime.datetime.now()
        elapsed_time = self.end_time - self.start_time
        dataframe.loc[0, 'end_time'] = str(self.end_time)
        dataframe.loc[0,'total_time'] = elapsed_time
        dataframe.to_csv('detail_data/LUSEM_electron_main.csv')
        
        
class MyEventAction(G4UserEventAction):

    def __init__(self):
        super().__init__()
        self.detector_num = 6 # or 12
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO',' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO'] # ' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO'
        # self.realdata = [0] * self.detector_num
        self.FTUO = [0] * 4
        self.config = ""
        self.detected_energy = 0
        
    def EndOfEventAction(self, anEvent):
        HCE = anEvent.GetHCofThisEvent()
        
        generatorAction = G4RunManager.GetRunManager().GetUserPrimaryGeneratorAction()
        particle = generatorAction.fParticleGun.GetParticleDefinition()
        partName = particle.GetParticleName()
        
        for i in range(self.detector_num):
            evtMap = HCE.GetHC(i)
            for _, edep in evtMap:
                
                if self.Dets[i][1] not in self.config:
                    self.config += self.Dets[i][1]
                
                if i in [0, 1]:
                    self.FTUO[i] = edep / keV
                elif i ==2:
                    self.FTUO[i - 1] += edep / keV
                elif i == 3:
                    self.FTUO[i - 1] = edep / keV
                elif i==4:
                    self.FTUO[i - 2] += edep / keV
                elif i == 5:
                    self.FTUO[i - 2] = edep / keV
                    
        for j in range(4):
            self.detected_energy += self.FTUO[j]
            
        dataframe.loc[anEvent.GetEventID(), 'particle_name'] = partName
        dataframe.loc[anEvent.GetEventID(), 'Detected_energy'] = self.detected_energy
        if self.config == "":
            self.config = "None"  # 빈 문자열인 경우 'None'으로 설정
        else:
            dataframe.loc[anEvent.GetEventID(), 'config'] = self.config
            for i in range(len(columns)):
                fit_energy = int((self.FTUO[i]-self.FTUO[i]%1))
                dataframe_logiclist[self.config].iloc[fit_energy-Emin,i] +=1
                
        self.config= ""
        self.detected_energy = 0
        # self.realdata = [0] * self.detector_num
        self.FTUO = [0] * 4
        
        
def runBatch(n):
    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
    runManager.SetUserInitialization(MyDetectorConstruction())
    physicsList = QGSP_BERT()
    runManager.SetUserInitialization(physicsList)
    runManager.SetUserInitialization(MyActionInitialization())
    runManager.Initialize()
    UImanager = G4UImanager.GetUIpointer()
    UImanager.ApplyCommand("/run/verbose 0")
    UImanager.ApplyCommand("/event/verbose 0")
    runManager.BeamOn(n)
    
def runGUI():
    ui = None

    if len(sys.argv) == 1:
        ui = G4UIExecutive(len(sys.argv), sys.argv)

    # optionally: choose a different Random engine...
    # G4Random.setTheEngine(MTwistEngine())

    # Construct the default run manager
    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)


    runManager.SetUserInitialization(MyDetectorConstruction())

    ###########################################
    ############## Physics list ###############
    ###########################################

    physicsList = FTFP_BERT() # proton
    # physicsList = QGSP_BERT() # electron, alpha

    runManager.SetUserInitialization(physicsList)

    ###########################################
    ####### User action initialization ########
    ###########################################

    runManager.SetUserInitialization(MyActionInitialization())


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


runBatch(100000)
