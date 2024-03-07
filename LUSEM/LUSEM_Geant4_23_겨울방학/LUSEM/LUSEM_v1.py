from geant4_pybind import *
import sys
import pandas as pd
import numpy as np
import datetime
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory "+ directory)

# initial condition
Emin = 10
Emax = 10000
Einterval = 1
Run_num = 20000000
round_num = 4

# create save folder
detail_folder = f'detail_data_write_final_{Run_num}'
createFolder(detail_folder)

# create bin dataframe
bin_columns = ['Incident_energy','Detected_energy','F','O','FT','UO','FTU','TUO','FTUO'] # 'T','U','FU','FO','TU','TO','FTO','FUO'
index_values = [i for i in range(1, Emax+ 1, Einterval)]
dataframe_bins = pd.DataFrame(0,columns=bin_columns, index=index_values)
dataframe_bins.fillna(0, inplace = True)


class LUSEMDetectorConstruction(G4VUserDetectorConstruction):
 
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
            

class LUSEMPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self, runAction):
        super().__init__()
        
        self.generator = G4GeneralParticleSource()
        UImanager = G4UImanager.GetUIpointer()
        UImanager.ApplyCommand("/gps/pos/type Surface")
        UImanager.ApplyCommand("/gps/pos/shape Sphere")
        UImanager.ApplyCommand("/gps/pos/centre 0. 0. 0. cm")
        UImanager.ApplyCommand("/gps/pos/radius 12 cm")
        
        UImanager.ApplyCommand("/gps/ang/type iso")
        UImanager.ApplyCommand("/gps/ang/mintheta 0 deg")
        UImanager.ApplyCommand("/gps/ang/maxtheta 90 deg")
        
        UImanager.ApplyCommand("/gps/particle e-")
        UImanager.ApplyCommand("/gps/ene/type Lin")
        UImanager.ApplyCommand("/gps/ene/gradient 0")
        UImanager.ApplyCommand("/gps/ene/intercept 1")
        UImanager.ApplyCommand("/gps/ene/max 10 MeV")
        UImanager.ApplyCommand("/gps/ene/min 10 keV")
        
        UImanager.ApplyCommand("/gps/number 1")
        self.runAction = runAction
        
    def GeneratePrimaries(self, anEvent):
        self.generator.GeneratePrimaryVertex(anEvent)
        
        self.initial_energy = self.generator.GetParticleEnergy()/keV
        self.initial_energy = round(self.initial_energy,round_num)
        particle_name = str(self.generator.GetParticleDefinition().GetParticleName())
        
        self.runAction.incident_energy_file.write(particle_name+ '\t'+ str(self.initial_energy)+'\n')
        
        fit_energy = int((self.initial_energy-self.initial_energy%Einterval))
        dataframe_bins.at[fit_energy, 'Incident_energy'] +=1


class LUSEMActionInitialization(G4VUserActionInitialization):
    def BuildForMaster(self):
        # this function is called only once for work thread
        self.SetUserAction(LUSEMRunAction())
    def Build(self):
        # initialization of actions
        runAction = LUSEMRunAction()
        self.SetUserAction(LUSEMPrimaryGeneratorAction(runAction))
        self.SetUserAction(runAction)
        self.SetUserAction(LUSEMEventAction(runAction))

class LUSEMRunAction(G4UserRunAction):
    def __init__(self):
        super().__init__()

    def BeginOfRunAction(self, aRun):
        # time record start
        self.start_time = datetime.datetime.now()
        self.start_time_str = self.start_time.strftime("%Y-%m-%d_%H-%M-%S")
        
        # save file open (Incident_energy, Detected_energy)
        self.incident_energy_file = open(detail_folder + '/Incident_energy.txt', 'a')
        self.detected_energy_file = open(detail_folder + '/Detected_energy.txt', 'a')
        
    def EndOfRunAction(self, aRun):
        # save time (end time)
        self.end_time = datetime.datetime.now()
        end_time_str = self.end_time.strftime("%Y-%m-%d_%H-%M-%S")
        elapsed_time = self.end_time - self.start_time
        dataframe_bins.to_csv(detail_folder +'/LUSEM_bin.csv')
        with open(detail_folder+'/time.txt','a') as f:
            f.write(self.start_time_str + '\t'+end_time_str+'\t'+str(elapsed_time))
            f.write('\n')
            
        # File close 
        self.incident_energy_file.close()
        self.detected_energy_file.close()
        
class LUSEMEventAction(G4UserEventAction):
    def __init__(self,runAction):
        super().__init__()
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO'] # ' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO'
        # self.realdata = [0] * self.detector_num
        self.config = ""
        self.detected_energy = 0
        self.runAction = runAction
        
    def EndOfEventAction(self, anEvent):
        HCE = anEvent.GetHCofThisEvent()
        self.anEvent_num = anEvent.GetEventID()
        
        for i in range(len(self.Dets)):
            evtMap = HCE.GetHC(i)
            for _, edep in evtMap:
                # config logc
                if self.Dets[i][1] not in self.config:
                    self.config += self.Dets[i][1]
                
                # energy sum
                self.detected_energy += edep/keV
        
        # round -> to save memory
        self.detected_energy = round(self.detected_energy,round_num)
        # save detected energy
        self.runAction.detected_energy_file.write(str(self.detected_energy)+'\t'+self.config+'\n')
        
        right_logic = ['F','O','FT','UO','FTU','TUO','FTUO']
        
        if self.config != "":
            if self.config in right_logic:
                fit_energy = int((self.detected_energy-self.detected_energy%Einterval))
                dataframe_bins.at[fit_energy, self.config] +=1
                dataframe_bins.at[fit_energy, 'Detected_energy'] +=1
                    
        self.config= ""
        self.detected_energy = 0

def runBatch(n):
    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
    
    runManager.SetUserInitialization(LUSEMDetectorConstruction())
    
    physicsList = QGSP_BERT()
    runManager.SetUserInitialization(physicsList)
    
    runManager.SetUserInitialization(LUSEMActionInitialization())
    
    runManager.Initialize()
    
    UImanager = G4UImanager.GetUIpointer()
    UImanager.ApplyCommand("/run/verbose 0")
    UImanager.ApplyCommand("/event/verbose 0")
    
    runManager.BeamOn(n)
    
def runGUI():
    ui = None
    if len(sys.argv) == 1:
        ui = G4UIExecutive(len(sys.argv), sys.argv)

    runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

    runManager.SetUserInitialization(LUSEMDetectorConstruction())

    physicsList = FTFP_BERT() # proton
    # physicsList = QGSP_BERT() # electron, alpha
    runManager.SetUserInitialization(physicsList)
    runManager.SetUserInitialization(LUSEMActionInitialization())
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
        
runBatch(Run_num)
