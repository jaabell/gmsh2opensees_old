# -*- coding: utf-8 -*-
# gmsh2opensees: A GUI application to transform .gmsh output files
# into opensees commands and read ouput back into gmsh
#
# 2010 - José Antonio Abell
#

from libtabs import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import tkMessageBox as Mes
from webbrowser import open_new_tab
from splash import SplashScreen
import platform

from libgmsh2opensees import *

class App:
    def createWidgets(self):
        # ----------------------------------------------------------------------
        #Title
        # ----------------------------------------------------------------------
        #Create Menubar
        self.topMenu = Menu(self.master)
        self.master['menu'] = self.topMenu
        
        self.menu_file = Menu(self.topMenu)
        self.menu_edit = Menu(self.topMenu)
        self.menu_about = Menu(self.topMenu)
        self.menu_run = Menu(self.topMenu)
        self.topMenu.add_cascade(menu = self.menu_file, label = 'File')
        self.topMenu.add_cascade(menu = self.menu_edit, label = 'Edit')
        self.topMenu.add_cascade(menu = self.menu_run, label = 'Run')
        self.topMenu.add_cascade(menu = self.menu_about, label = '?')
        
        # FILE MENU
        # Index
        # 0: New Project
        # 1: Load .gmsh file
        # 2: Load Project...
        # 3: Save Project
        # 4: ---------- SEPARATOR-----------
        # 5: Save Geometry
        # 6: Save Materials
        # 7: Save Assigns
        # 8: Save Patterns
        # 9: Save Recorders
        # 10: Save Analysis
        # 11: Save All files
        
        self.menu_file.add_command(label = 'New Project', command = self.clearProject)
        self.menu_file.add_command(label = 'Load .gmsh file...', command = self.loadGmshFile)
        self.menu_file.add_command(label = 'Load Project...', command = self.loadProject)
        self.menu_file.add_command(label = 'Save Project', command = self.saveProject, state = 'disabled')
        
        self.menu_file.add_separator()
        
        self.menu_file.add_command(label = 'Save Geometry', command = self.saveGeom, state = 'disabled')
        self.menu_file.add_command(label = 'Save Materials', command = self.saveMat, state = 'disabled')
        self.menu_file.add_command(label = 'Save Assigns', command = self.saveAssigns, state = 'disabled')
        self.menu_file.add_command(label = 'Save Patterns', command = self.savePat, state = 'disabled')
        self.menu_file.add_command(label = 'Save Recorders', command = self.saveRec, state = 'disabled')
        self.menu_file.add_command(label = 'Save Analysis', command = self.saveAnalysis, state = 'disabled')
        self.menu_file.add_command(label = 'Save Master File', command = self.saveMaster, state = 'disabled')
        self.menu_file.add_command(label = 'Save All Files', command = self.saveAll, state = 'disabled')
        
        self.menu_file.add_separator()
        
        self.menu_file.add_command(label = 'Close', command = self.closeMainWindow, state = 'normal')
        
        # EDIT MENU
        self.editProjectFilesButt = self.menu_edit.add_command(label = 'Project Files', command = self.editProjectFiles)
        self.menu_edit.add_command(label = 'Preferences', command = self.editPreferences)
        
        # RUN MENU
        self.runOpenSEESButt = self.menu_run.add_command(label = 'Run in OpenSEES', command = self.runOpenSEES)
        self.getResultsButt = self.menu_run.add_command(label = 'Get Results', command = self.getResults)
        
        # About MENU
        self.openSEESHelp =  'http://opensees.berkeley.edu/wiki/index.php/OpenSees_User'
        self.openOpenSEESHelp = lambda url=0: webbrowser.open_new_tab(self.openSEESHelp)
        self.menu_about.add_command(label = 'Help', command = self.showHelp)
        self.menu_about.add_command(label = 'OpenSEES Help', command = self.openOpenSEESHelp)
        self.menu_about.add_separator()
        self.menu_about.add_command(label = 'About...', command = self.showAbout)
        
         # ----------------------------------------------------------------------
        # Tabs setup
        # ----------------------------------------------------------------------
        self.tabMaster = GenTabMaster(self.master)
        
        self.tabSummary = FrameSummary(self.tabMaster)
        self.tabMaster.add(self.tabSummary, text='Model Summary', state='disabled')
        self.tabSummary.createWidgets()
        
        self.tabMaterials = FrameMaterials(self.tabMaster)
        self.tabMaster.add(self.tabMaterials, text='Materials', state='disabled')
        self.tabMaterials.createWidgets()
        
        self.tabAssign = FrameAssign(self.tabMaster)
        self.tabMaster.add(self.tabAssign, text='Assignments', state='disabled')
        self.tabAssign.createWidgets()
        
        self.tabPatterns = FramePatterns(self.tabMaster)
        self.tabMaster.add(self.tabPatterns, text='Patterns', state='disabled')
        self.tabPatterns.createWidgets()
        
        self.tabRecord = FrameRecorders(self.tabMaster)
        self.tabMaster.add(self.tabRecord, text='Recorders', state='disabled')
        self.tabRecord.createWidgets()

        self.tabAnalysis = FrameAnalysis(self.tabMaster)
        self.tabMaster.add(self.tabAnalysis, text='Analysis Setup', state='disabled')
        self.tabAnalysis.createWidgets()
        
        self.tabVariables = FrameVariables(self.tabMaster)
        self.tabMaster.add(self.tabVariables, text='Variables', state='disabled')
        self.tabVariables.createWidgets()

        self.tabMaster.pack()
        
    def loadGmshFile(self):
        self.fname = askopenfilename(parent=self.master, title="gmsh2OpenSEES:  Seleccionar malla de origen", initialdir=".", filetypes=[("GMSH mesh","*.msh")])
        
        if len(self.fname) > 0:
            self.model = Model.loadFromGmshFile(self.fname)
        
        if self.model.success == 1:
            print 'Success in loading GMSH file!'
            self.activateGui()
            self.model.subscribe(self)
        else:
            pass
        
    def saveGeom(self):
        self.outfname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=self.model.fnames['geometry'])
        self.model.fnames['geometry'] = self.outfname
        self.model.writeGeometry()
        pass
    
    def saveMat(self):
        self.outfname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=self.model.fnames['materials'])
        self.model.fnames['materials'] = self.outfname
        self.model.writeMaterials()
        pass

    def saveAssigns(self):
        print 'saveAssigns'
        self.outfname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=self.model.fnames['assigns'])
        self.model.fnames['assigns'] = self.outfname
        self.model.writeAssigns()
        pass
        
    def savePat(self):
        print 'savePat'
        pass
        
    def saveRec(self):
        print 'saveRec'
        pass
        
    def saveAnalysis(self):
        print 'saveAnalysis'
        pass
        
    def saveMaster(self):
        print 'saveMaster'
        self.outfname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=self.model.fnames['master'])
        self.model.fnames['master'] = self.outfname
        self.model.writeMaster()
        pass
        
    def saveAll(self):
        print 'Saving Geometry specification to  '+str(self.model.flags['geometry'])+' :'+self.model.fnames['geometry']+'\n'
        print 'Saving Material specifications to '+str(self.model.flags['materials'])+' :'+self.model.fnames['materials']+'\n'
        print 'Saving Assigns to                 '+str(self.model.flags['assigns'])+' :'+self.model.fnames['assigns']+'\n'
        print 'Saving Patterns to                '+str(self.model.flags['patterns'])+' :'+self.model.fnames['patterns']+'\n'
        print 'Saving Analysis Options to        '+str(self.model.flags['analysis'])+' :'+self.model.fnames['analysis']+'\n'
        print 'Saving Variables to               '+str(self.model.flags['variables'])+' :'+self.model.fnames['variables']+'\n'
        print 'Saving Recorder Settings to       '+str(self.model.flags['recorders'])+' :'+self.model.fnames['recorders']+'\n\n'
        print '                   >> MASTER FILE '+str(self.model.flags['master'])+' :'+self.model.fnames['master']+'\n'
        if self.model.flags['geometry'] == 1:
            self.model.writeGeometry()
        if self.model.flags['materials'] == 1:
            self.model.writeMaterials()
        if self.model.flags['assigns'] == 1:
            self.model.writeAssigns()
        if self.model.flags['master'] == 1:
            self.model.writeMaster()
        if self.model.flags['patterns'] == 1:
            pass
        if self.model.flags['recorders'] == 1:
            pass
        if self.model.flags['analysis'] == 1:
            pass
        if self.model.flags['elements'] == 1:
            pass
        if self.model.flags['variables'] == 1:
            self.model.writeVariables()
            pass
        pass
        
    def loadProject(self):
        print 'loadProject'
        self.fname = askopenfilename(parent=self.master, title="gmsh2OpenSEES:  Seleccionar el archivo de destino", initialdir=".", filetypes=[("gmsh2opensees Binary Model Representation","*.bmr")])
        if len(self.fname) > 0:
            self.model = Model.loadDatabase(self.fname)
            print 'Success in loading GMSH file!'        
            if self.model.success == 1:
                self.activateGui()
                self.model.subscribe(self)
                #self.catchModelChange()
                self.checkModelFlags()
        pass
        
    def activateGui(self):
        self.tabMaster.tab(0,state="normal")
        self.tabMaster.tab(1,state="normal")
        self.tabMaster.tab(2,state="normal")
        self.tabMaster.tab(3,state="normal")
        self.tabMaster.tab(4,state="normal")
        self.tabMaster.tab(5,state="normal")
        self.tabMaster.tab(6,state="normal")
        self.tabMaster.select(0)
        self.menu_file.entryconfig(3,state = 'normal')
        self.menu_file.entryconfig(5,state = 'normal')
        self.menu_file.entryconfig(11,state = 'normal')
        self.menu_file.entryconfig(12,state = 'normal')
        
        self.tabSummary.updateWidgets(self.model)
        self.tabAssign.updateWidgets(self.model)
        self.tabMaterials.updateWidgets(self.model)
            
    def saveProject(self):
        fname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("gmsh2opensees Binary Model Representation","*.bmr")], initialfile=self.fname[:-4]+'.bmr')
        self.model.saveDatabase(fname)
        print 'saveProject'
        pass
        
    def dumpModelToIntepreter(self):
        ans = Mes.askyesno(message='This will end current session', icon='warning', title='gmsh2OpenSEES: Dump to python interpreter.')

        if ans == TRUE:
            return self.model
            self.destroy()
        else:
            pass
    
    def checkModelFlags(self):
        # FILE MENU
        # Index
        # 0: New Project
        # 1: Load .gmsh file
        # 2: Load Project...
        # 3: Save Project
        # 4: ---------- SEPARATOR-----------
        # 5: Save Geometry
        # 6: Save Materials
        # 7: Save Assigns
        # 8: Save Patterns
        # 9: Save Recorders
        # 10: Save Analysis
        # 11: Save All files
        # 12: Save Master
        # 13: ---------- SEPARATOR-----------
        # 14: Close gui
        
        if self.model.flags['geometry'] == 1:
            self.menu_file.entryconfig(5,state='normal')
            self.menu_file.entryconfig(12,state='normal')
        else:
            self.menu_file.entryconfig(5,state='disabled')
            self.menu_file.entryconfig(12,state='disabled')
            pass
            
        if self.model.flags['master'] == 1:
            self.menu_file.entryconfig(11,state='normal')
            pass
        else:
            self.menu_file.entryconfig(11,state='disabled')
            pass
            
        if self.model.flags['materials'] == 1:
            self.menu_file.entryconfig(6,state='normal')
        else:
            self.menu_file.entryconfig(6,state='disabled')
            pass
            
        if self.model.flags['assigns'] == 1:
            self.menu_file.entryconfig(7,state='normal')
        else:
            self.menu_file.entryconfig(7,state='disabled')
            pass
            
        if self.model.flags['patterns'] == 1:
            self.menu_file.entryconfig(8,state='normal')
        else:
            self.menu_file.entryconfig(8,state='disabled')
            pass
            
        if self.model.flags['recorders'] == 1:
            self.menu_file.entryconfig(9,state='normal')
        else:
            self.menu_file.entryconfig(9,state='disabled')
            pass
            
        if self.model.flags['analysis'] == 1:
            self.menu_file.entryconfig(10,state='normal')
        else:
            self.menu_file.entryconfig(10,state='disabled')
            pass
            
        if self.model.flags['elements'] == 1:
            pass
        else:
            pass
            
    def clearProject(self):
        pass
        
    def editProjectFiles(self):
        pass
        
    def editPreferences(self):
        pass
        
    def runOpenSEES(self):
        pass
        
    def getResults(self):
        pass
        
    def showAbout(self):
        self.splash = Toplevel(self.master)
        self.splash.wm_iconbitmap('icons/clone-old.ico')
        self.splash.imgobj = PhotoImage(file='icons/splash.gif')
        self.splash.picture = Label(self.splash)
        self.splash.picture['image'] = self.splash.imgobj
        self.splash.picture.grid(row = 0, column = 0)
        self.splash.agradecimientos = Label(self.splash,text='(C)2010 Universidad de los Andes + Gracias Matías Recabarren')
        self.splash.agradecimientos.grid(row = 1, column=0)
        self.splash.okButt = Button(self.splash,text='Ok',command=self.splash.destroy)
        self.splash.okButt.grid(row = 2, column = 0)
        pass
        
    def showHelp(self):
        pass
        
    def updateWidgets(self):
        self.tabAssign.updateWidgets(self.model)
        self.tabMaterials.updateWidgets(self.model)
        pass
    
    def catchModelChange(self):
        self.checkModelFlags()
        self.updateWidgets()
        pass
    
    def closeMainWindow(self):
        ans = Mes.askyesno(message='This will end current session', icon='warning', title='gmsh2OpenSEES: exit')
        
        if ans == TRUE:
            self.master.destroy()
        else:
            pass
        pass
    
    def __init__(self, master):
        self.master = master
        self.master.title("gmsh2OpenSEES")
        self.model = 'void'
        self.createWidgets()
        

# MAIN
root = Tk()
root.option_add('*tearOff', FALSE)   #Remove undockable menus

if platform.system() == 'Windows':
    root.wm_iconbitmap('icons/clone-old.ico')

with SplashScreen( root, 'icons/splash.gif', 1.0 ):
   App(root)

root.mainloop()
