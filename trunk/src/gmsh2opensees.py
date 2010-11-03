# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 07:53:48 2010

@author: jose
"""
from libtabs import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import tkMessageBox as Mes

from libgmsh2opensees import *

class App:
    def createWidgets(self):
        # ----------------------------------------------------------------------
        #Title
        # ----------------------------------------------------------------------
               
        
        #Create Menubar
        #self.win = Toplevel(self)
        #self.win = Toplevel(self.master)
        #self.topMenu = Menu(self.win)
        self.topMenu = Menu(self.master)
        self.master['menu'] = self.topMenu
        #self['menu'] = self.topMenu
        
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
        self.menu_file.add_command(label = 'Save All Files', command = self.saveAll, state = 'disabled')
        
        # EDIT MENU
        self.editProjectFilesButt = self.menu_edit.add_command(label = 'Project Files', command = self.editProjectFiles)
        self.menu_edit.add_command(label = 'Preferences', command = self.editPreferences)
        
        # RUN MENU
        self.runOpenSEESButt = self.menu_run.add_command(label = 'Run in OpenSEES', command = self.runOpenSEES)
        self.getResultsButt = self.menu_run.add_command(label = 'Get Results', command = self.getResults)
        
        # About MENU
        self.menu_about.add_command(label = 'Help', command = self.showHelp)
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
        
        # ----------------------------------------------------------------------
        # Lower Save Buttons
        # ----------------------------------------------------------------------
        
        #self.buttonFrame = Frame(self.master)
        #self.buttonFrame.pack(expand = 1)
        
    def loadGmshFile(self):
        self.fname = askopenfilename(parent=self.master, title="gmsh2OpenSEES:  Seleccionar malla de origen", initialdir=".", filetypes=[("GMSH mesh","*.msh")])
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
        print 'saveMat'
        pass

    def saveAssigns(self):
        print 'saveAssigns'
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
        
    def saveAll(self):
        print 'saveRec'
        pass
        
    def loadProject(self):
        print 'loadProject'
        self.fname = askopenfilename(parent=self.master, title="gmsh2OpenSEES:  Seleccionar el archivo de destino", initialdir=".", filetypes=[("gmsh2opensees Binary Model Representation","*.bmr")])
        self.model = Model.loadDatabase(self.fname)
        print 'Success in loading GMSH file!'
        
        if self.model.success == 1:
            self.activateGui()
            self.model.subscribe(self)
            self.catchModelChange()
        
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
        #self.saveGeomButt['state'] = "normal"
        
        self.tabSummary.updateWidgets(self.model)
        self.tabAssign.updateWidgets(self.model)
        self.tabMaterials.updateWidgets(self.model)
        #self.saveProjectButt['state'] = 'normal'
        #self.dumpModelButt['state'] = 'normal'
            
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
        if self.model.flags['geometry'] == 1:
            self.menu_file.entryconfig(5,state='normal')
            #self.saveGeomButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(5,state='disabled')
            #self.saveGeomButt['state'] = 'disabled'
            pass
            
        if self.model.flags['master'] == 1:
            #self.saveMasterButt['state'] = 'normal'
            pass
        else:
            #self.saveMasterButt['state'] = 'disabled'
            pass
            
        if self.model.flags['materials'] == 1:
            self.menu_file.entryconfig(6,state='normal')
            #self.saveMatButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(6,state='disabled')
            #self.saveMatButt['state'] = 'disabled'
            pass
            
        if self.model.flags['assigns'] == 1:
            self.menu_file.entryconfig(7,state='normal')
            #self.saveAssignButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(7,state='disabled')
            #self.saveAssignButt['state'] = 'disabled'
            pass
            
        if self.model.flags['patterns'] == 1:
            self.menu_file.entryconfig(8,state='normal')
            #self.savePatButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(8,state='disabled')
            #self.savePatButt['state'] = 'disabled'
            pass
            
        if self.model.flags['recorders'] == 1:
            self.menu_file.entryconfig(9,state='normal')
            #self.saveRecButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(9,state='disabled')
            #self.saveRecButt['state'] = 'disabled'
            pass
            
        if self.model.flags['analysis'] == 1:
            self.menu_file.entryconfig(10,state='normal')
            #self.saveAnalysisButt['state'] = 'normal'
        else:
            self.menu_file.entryconfig(10,state='disabled')
            #self.saveAnalysisButt['state'] = 'disabled'
            pass
            
        if self.model.flags['elements'] == 1:
            #self.saveGeomButt['state'] = 'normal'
            pass
        else:
            #self.saveGeomButt['state'] = 'disabled'
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
    
    def __init__(self, master):
        self.master = master
        self.master.title("gmsh2OpenSEES")
        self.model = 'void'
        self.createWidgets()
        


# MAIN
root = Tk()
root.option_add('*tearOff', FALSE)   #Remove undockable menus
model = App(root)
root.mainloop()
