from geant4_pybind import *
import sys


class baseDetectorConstruction(G4VUserDetectorConstruction):
 
    def __init__(self):
        super().__init__()
        self.world= None
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO',' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO']
        self.Dets_LV = ['d1_VF_si', 'd1_VT6_si','d1_VT4_si', 'd1_VT3_si','d1_VT1_si', 'd1_VO_si',
                   'd2_VF_si', 'd2_VT6_si','d2_VT4_si', 'd2_VT3_si','d2_VT1_si', 'd2_VO_si']
        self.logic = None
 
 
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
            
        # global magnetic field
        fieldValue = G4ThreeVector(0,0.2*tesla,0)
        self.fMagFieldMessenger = G4GlobalMagFieldMessenger(fieldValue)
        self.fMagFieldMessenger.SetVerboseLevel(1)
        
        # detector magnetic field
        # self.fMagneticField = B5MagneticField()
        # self.fFieldMgr = G4FieldManager()
        # self.fFieldMgr.SetDetectorField(self.fMagneticField)
        # self.fFieldMgr.CreateChordFinder(self.fMagneticField)
        # forceToAllDaughters = True
        # self.fMagneticLogical.SetFieldManager(self.fFieldMgr, forceToAllDaughters)
        
        

class basePrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):

    def __init__(self):
        super().__init__()
        
        # proton & telescope A
        self.fParticleGun = G4ParticleGun(1)
        self.particle_energy = 1*MeV
        # Default particle kinematic (electron)
        ParticleTable = G4ParticleTable.GetParticleTable()
        self.electron = ParticleTable.FindParticle("e-")
        self.fParticleGun.SetParticleDefinition(self.electron)
        
        # (telescope A / F)
        self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 75*mm))
        self.fParticleGun.SetParticleEnergy(self.particle_energy)
        
        self.proton = ParticleTable.FindParticle("proton")

    def GeneratePrimaries(self, anEvent):
        # i = int(2 * G4UniformRand())
        # if i == 0:
        #     particle = self.proton
        # else:
        #     particle = self.electron
        particle = self.electron
        self.fParticleGun.SetParticleDefinition(particle)
        
        self.particle_energy += 100*keV
            
        self.fParticleGun.SetParticleEnergy(self.particle_energy)
        
        # j = int(4*G4UniformRand())
        # if j == 0:
        #     # (telescope A / F)
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 20*mm))
        #     self.fParticleGun.SetParticleEnergy(self.particle_energy)
        # elif j==1:
        #     # (telescope A / O)
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 8*mm))
        #     self.fParticleGun.SetParticleEnergy(self.particle_energy)
        # elif j==2:
        #     # (telescope B / F)
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(25*mm,-12.48*mm, -20*mm))
        #     self.fParticleGun.SetParticleEnergy(self.particle_energy)
        # else:
        #     self.fParticleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        #     self.fParticleGun.SetParticlePosition(G4ThreeVector(25*mm,-12.48*mm, -9*mm))
        #     self.fParticleGun.SetParticleEnergy(self.particle_energy)
            
        # self.fParticleGun.GeneratePrimaryVertex(anEvent)
        
        # original
        self.fParticleGun.SetParticlePosition(G4ThreeVector(-25*mm,-12.48*mm, 75*mm))
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
        self.SetUserAction(baseEventAction())
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
        
        AnalysisManager.CreateNtuple("event", "Particle information")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AF detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AT2 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AT1 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AU2 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AU1 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for AO detector")
        
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BF detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BT2 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BT1 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BU2 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BU1 detector")
        AnalysisManager.CreateNtupleDColumn("Loss Energy (MeV) for BO detector")
        
        AnalysisManager.FinishNtuple()

    def BeginOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.OpenFile("Lusem_data.csv")
        
        
    def EndOfRunAction(self, aRun):
        AnalysisManager = G4AnalysisManager.Instance()
        AnalysisManager.Write()
        AnalysisManager.CloseFile()

class baseEventAction(G4UserEventAction):

    def __init__(self):
        super().__init__()
        self.fCollID_SD = []
        self.Dets = ['AF', 'AT2', 'AT1', 'AU2', 'AU1', 'AO',' BF', 'BT2', 'BT1', 'BU2','BU1', 'BO']
        
    def EndOfEventAction(self, anEvent):
        AnalysisManager = G4AnalysisManager.Instance()
        HCE = anEvent.GetHCofThisEvent()
        SDMan = G4SDManager.GetSDMpointer()
        
        for i in range(len(self.Dets)):
            self.fCollID_SD.append(SDMan.GetCollectionID(f"Det_{self.Dets[i]}/Edep"))
            collID = self.fCollID_SD[i]
            evtMap = HCE.GetHC(collID)
            
            for copyNb, edep in evtMap:
                AnalysisManager.FillNtupleDColumn(i,edep)
        AnalysisManager.AddNtupleRow(0)
            

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

