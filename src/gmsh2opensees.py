# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 07:53:48 2010

@author: jose
"""
from libtabs import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from libgmsh2opensees import *

class App:
    def createWidgets(self):
        # ----------------------------------------------------------------------
        #Title
        # ----------------------------------------------------------------------
               
        self.topMenu = Frame(self.master)
        
        self.title = Label(self.topMenu)
        self.title.text = 'gmsh2opensees'
        self.title.fill = 'x'
        self.title.pack()
        
        self.loadGmshMeshButt = Button(self.topMenu, command = self.loadGmshFile)
        self.loadGmshMeshButt['text'] = 'Load .msh file'
        self.loadGmshMeshButt.pack(side = 'left', expand = 1)
        
        self.loadProjectButt = Button(self.topMenu)
        self.loadProjectButt['text'] = 'Load Project'
        self.loadProjectButt.pack(side = 'left', expand = 1)
        
        self.saveProjectButt = Button(self.topMenu)
        self.saveProjectButt['text'] = 'Save Project'
        self.saveProjectButt.pack(side = 'left', expand = 1)
        
        self.topMenu.pack(expand = 1)
        
        # ----------------------------------------------------------------------
        # Tabs setup
        # ----------------------------------------------------------------------
        self.tabMaster = GenTabMaster(self.master)
        
        self.tabSummary = FrameSummary(self.tabMaster)
        self.tabMaster.add(self.tabSummary, text='Model Summary', state='disabled')
        self.tabSummary.createWidgets()
        
        
        self.tabAssign = FrameAssign(self.tabMaster)
        self.tabMaster.add(self.tabAssign, text='Assignments', state='disabled')
        self.tabAssign.createWidgets()
        
        self.tabRecord = FrameRecorders(self.tabMaster)
        self.tabMaster.add(self.tabRecord, text='Recorders', state='disabled')
        
        self.tabAnalysis = FrameAnalysis(self.tabMaster)
        self.tabMaster.add(self.tabAnalysis, text='Analysis Setup', state='disabled')
        
        self.tabMaster['width'] = 800
        self.tabMaster['height'] = 600
        self.tabMaster.pack()
        
        # ----------------------------------------------------------------------
        # Lower Buttons
        # ----------------------------------------------------------------------
        
        self.buttonFrame = Frame(self.master)
        
        self.saveGeomButt = Button(self.buttonFrame, command=self.saveGeom)
        self.saveGeomButt['text'] = 'Save Geometry'
        self.saveGeomButt['state'] = 'disabled'
        self.saveGeomButt.pack(side = 'left', expand = 1)
        
        self.saveAssignButt = Button(self.buttonFrame, command=self.saveAssigns)
        self.saveAssignButt['text'] = 'Save Physical Assigns'
        self.saveAssignButt['state'] = 'disabled'
        self.saveAssignButt.pack(side = 'left', expand = 1)
        
        self.saveAnalysisButt = Button(self.buttonFrame, command=self.saveAnalysis)
        self.saveAnalysisButt['text'] = 'Save Analysis Options'
        self.saveAnalysisButt['state'] = 'disabled'
        self.saveAnalysisButt.pack(side = 'left', expand = 1)
        
        self.buttonFrame.pack(expand = 1)
        
    def loadGmshFile(self):
        self.fname = askopenfilename(parent=self.master, title="gmsh2OpenSEES:  Seleccionar malla de origen", initialdir=".", filetypes=[("GMSH mesh","*.msh")])
        self.model = Model.loadFromGmshFile(self.fname)
        
        if self.model.success == 1:
            print 'Success in loading GMSH file!'
            #self.tabMaster.tab(self.tabSummary, state ="normal")
            self.tabMaster.tab(0,state="normal")
            self.tabMaster.tab(1,state="normal")
            self.tabMaster.tab(2,state="normal")
            self.tabMaster.tab(3,state="normal")
            self.saveGeomButt['state'] = "normal"
            
            self.tabSummary.updateWidgets(self.model)
            self.tabAssign.updateWidgets(self.model)
            
        else:
            pass
        
    def saveGeom(self):
        self.outfname = asksaveasfilename(parent=self.master,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=self.fname[:-4]+'.ops')
        self.model.writeModelToOpsFile(self.outfname)
        
        pass
    def saveAssigns(self):
        print 'saveAssigns'
        pass
    def saveAnalysis(self):
        print 'saveAnalysis'
        pass
    def loadProject(self):
        print 'loadProject'
        pass
    def saveProject(self):
        print 'saveProject'
        pass
    
    def __init__(self, master):
        self.master = master
        self.master.title("gmsh2OpenSEES")
        self.model = 'void'
        self.createWidgets()



# MAIN
root = Tk()
a = App(root)
root.mainloop()
