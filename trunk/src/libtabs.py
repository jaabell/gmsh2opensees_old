# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 07:53:48 2010

@author: jose
"""
from Tkinter import *
from ttk import *
from libgmsh2opensees import *
import tkMessageBox as Mes
import tkFont as font

#from Tkinter.ttk import *
#from pyTtk import *



# ------------------------------------------------------------------------------
# TAB: Geometry
# ------------------------------------------------------------------------------
class FrameSummary(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        
        thisRow = 0
        
        # File Path
        self.labelFname = Label(self,text='Path: ')
        self.labelFname.grid(row=0,column=0,pady=5, sticky=NW)
        
        self.labelPath = Label(self,text='No file selected!')
        self.labelPath.grid(row=0,column=1,pady=5, sticky=NW)
        
        # Model Description
        self.labelNnodesTxt = Label(self,text='Number of nodes: ')
        self.labelNnodesTxt.grid(row=2,column=0,pady=5, sticky=NW)
        self.labelNnodes = Label(self,text='0')
        self.labelNnodes.grid(row=2,column=1,pady=5, sticky=NW)
        
        self.labelNelemTxt = Label(self,text='Number of elements: ')
        self.labelNelemTxt.grid(row=3,column=0,pady=5, sticky=NW)
        self.labelNelem = Label(self,text='0')
        self.labelNelem.grid(row=3,column=1,pady=5, sticky=NW)
        
        self.xSpanTxt = Label(self, text = 'Model Extension in X: ')
        self.xSpanRange = Label(self, text='[xmin,xmax]')
        self.ySpanTxt = Label(self, text = 'Model Extension in Y: ')
        self.ySpanRange = Label(self, text='[ymin,ymax]')
        self.zSpanTxt = Label(self, text = 'Model Extension in Z')
        self.zSpanRange = Label(self, text='[zmin,zmax]: ')
        
        self.xSpanTxt.grid(row=4,column=0)
        self.ySpanTxt.grid(row=5,column=0)
        self.zSpanTxt.grid(row=6,column=0)
        self.xSpanRange.grid(row=4,column=1,pady=5, sticky=NW)
        self.ySpanRange.grid(row=5,column=1,pady=5, sticky=NW)
        self.zSpanRange.grid(row=6,column=1,pady=5, sticky=NW)
        
        self.labelNphysgrpTxt = Label(self, text = 'Number of Defined Physical Groups: ')
        self.labelNphysgrpVal = Label(self, text='--none--')
        self.labelNphysgrpTxt.grid(row=7,column=0,pady=5, sticky=NW)
        self.labelNphysgrpVal.grid(row=7,column=1,pady=5, sticky=NW)
        
        self.frameNumberOfElementsByType = Labelframe(self,text = 'Number of Elements by Type')
        self.frameNumberOfElementsByType.grid(row = 8,column = 0, columnspan = 2)
        
        self.labelComments = Label(self, text = 'User Comments: ')
        self.labelComments.grid(row = 9, column = 0, sticky=N)
        
        self.textboxComments = Text(self, width=50, height=10)
        self.textboxComments.grid(row = 9, column = 1)
        
        self.includeInCommentInOutput = Checkbutton(self, text= "Include comments in all output files")
        self.includeInCommentInOutput.grid(row =10, column = 1)
        
        self.coordRange =  lambda xmin,xmax: '[{0:12.5f}, {1:12.5f}]'.format(xmin,xmax)
    
    def updateWidgets(self,model):
        self.model = model
        self.labelPath['text'] = model.sourceFile
        self.labelNnodes['text'] = '{0}'.format(model.Nnodes)
        self.labelNelem['text'] = '{0}'.format(model.Nelem)
        
        self.xSpanRange['text'] = self.coordRange(model.XYZ[:,0].min(), model.XYZ[:,0].max())
        self.ySpanRange['text'] = self.coordRange(model.XYZ[:,1].min(), model.XYZ[:,1].max())
        self.zSpanRange['text'] = self.coordRange(model.XYZ[:,2].min(), model.XYZ[:,2].max())
        
        self.labelNphysgrpVal['text'] = str(len(model.physgrp))
        
        self.frameNumberOfElementsByType.labelTxt = [Label(self.frameNumberOfElementsByType, text = 'Element Type')]
        self.frameNumberOfElementsByType.labelNum = [Label(self.frameNumberOfElementsByType, text = '     N      ')]
        self.frameNumberOfElementsByType.labelTxt[0].grid(column=0,row=0)
        self.frameNumberOfElementsByType.labelNum[0].grid(column=1,row=0)
        
        self.frameNumberOfElementsByType.sep = Separator(self.frameNumberOfElementsByType, orient='horizontal')
        self.frameNumberOfElementsByType.sep.grid(row=1,column=0,columnspan = 2)
        
        i = 1
        for typeKey in model.elemTypes.keys():
            numberOfElements = model.elemTypes[typeKey] .Nelem
            #print numberOfElements
            self.frameNumberOfElementsByType.labelTxt.append(Label(self.frameNumberOfElementsByType, text = typeKey))
            self.frameNumberOfElementsByType.labelTxt[i].grid(row = i, column = 0)
            self.frameNumberOfElementsByType.labelNum.append(Label(self.frameNumberOfElementsByType, text = str(numberOfElements)))
            self.frameNumberOfElementsByType.labelNum[i].grid(row = i, column = 1)
            i += 1
        

# ------------------------------------------------------------------------------
# TAB: Materials
# ------------------------------------------------------------------------------
class FrameMaterials(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
        
    def createWidgets(self):
        
        self.comboFont = font.Font(family='Helvetica', size=8)
        
        self.title = Label(self, text = 'Material Generator', anchor = 'center')
        self.title.grid(row = 0, column = 0, columnspan = 4, sticky = EW)
        
        #Headers
        self.materialTxt = Label(self, text = 'Material')
        self.materialTxt.grid(row = 1, column = 0, sticky = EW)
        self.matTypeTxt = Label(self, text = 'Type')
        self.matTypeTxt.grid(row = 1, column = 1, sticky = EW)
        self.matIdTxt = Label(self, text = 'Id')
        self.matIdTxt.grid(row = 1, column = 2, sticky = EW)
        self.matArgsTxt = Label(self, text = 'Parameters')
        self.matArgsTxt.grid(row = 1, column = 3, sticky = EW)
        
        self.uniaxialMaterialTypes = ()
        self.ndMaterialTypes = ()
        self.sectionTypes = ()
        self.frictionModelTypes = ()
        self.geomTransfTypes = ()
        
        basicWidth = 3
        
        #Comboboxes 
        self.materialCombo = Combobox(self, width=5*basicWidth)#, textvariable = self.materialVar)
        self.materialCombo.bind('<<ComboboxSelected>>', self.updateMatTypeCombo)
        self.materialCombo.grid(row = 2, column = 0, sticky=EW)
        
        
        self.matTypeCombo = Combobox(self, font = self.comboFont, width=5*basicWidth)
        self.matTypeCombo.bind('<<ComboboxSelected>>',  self.updateMatArgsCombo)
        self.matTypeCombo.grid(row = 2, column = 1, sticky = EW)
        
        self.matIdEntry = Label(self, width=1*basicWidth)
        self.matIdEntry.grid(row = 2, column = 2)
        
        self.matArgsEntry = Entry(self, width=15*basicWidth)
        self.matArgsEntry.grid(row = 2, column = 3, sticky = EW)
        
        
        #Buttons
        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row = 3, column = 0, columnspan = 4)
        
        self.addButt = Button(self.buttonFrame,text='Add (↓)',command = self.addMaterial)
        self.addButt.grid(row=0,column=0)
        self.modifyButt = Button(self.buttonFrame,text='Modify (↓)',command = self.modifyMaterial)
        self.modifyButt.grid(row=0,column=1)
        self.deleteButt = Button(self.buttonFrame,text='Delete (X)',command = self.deleteMaterial)
        self.deleteButt.grid(row=0,column=2)
        
        self.materialView = Treeview(self, height = 15, columns = ('Type','Id','Parameters'))
        self.materialView.column('Type', width=5*basicWidth, anchor='center')
        self.materialView.column('Id', width=1*basicWidth, anchor='center')
        self.materialView.column('Parameters', width=15*basicWidth, anchor='center')
        self.materialView.heading('Type', text='Type')
        self.materialView.heading('Id', text='Id')
        self.materialView.heading('Parameters', text='Parameters')
        self.materialView.grid(row=4, column = 0, columnspan=4, sticky=EW)
        
        self.scrollMaterials = Scrollbar(self,command = self.materialView.yview,orient = VERTICAL)
        self.scrollMaterials.grid(column=5,row = 4,sticky = NSEW)
        
        self.materialView['yscrollcommand'] = self.scrollMaterials.set
        
        self.materialView.bind('<Double-1>',self.loadMaterial)
        
        self.readMaterialsDatabase()
        
        self.materialCombo['values'] = tuple(self.materialList)
        
        self.columnconfigure(0,weight=5)
        self.columnconfigure(1,weight=5)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=20)
        
        self.treeItemIdList = []
        pass
    
    def addMaterial(self):
        print 'addMaterial'
        if len(self.model.materials.keys()) == 0:
            id = 1
        else:
            id = max(self.model.materials.keys())+1
        args = self.matArgsEntry.get()
        material = self.materialCombo.get()
        matType = self.matTypeCombo.get()
        self.model.addMaterial(id,[material, matType, args])
        #self.model.materials[id] = [material, matType, args]
        print 'Added material: '+material+' '+matType+' '+str(id)+' '+args
        self.updateMaterialLists()
        pass
    
    def loadMaterial(self, event):
        print 'modifyMaterial'
        self.currentValues = self.materialView.item(self.materialView.focus(), option = 'values')
        material = self.materialView.item(self.materialView.focus(), option = 'text')
        self.materialCombo.set(material)
        self.updateMatTypeCombo()
        self.matTypeCombo.set(self.currentValues[0])
        self.matIdEntry['text'] = self.currentValues[1]
        self.matArgsEntry.delete(0,'end')
        self.matArgsEntry.insert(0,self.currentValues[2])
        pass
        
    def modifyMaterial(self,*args):
        self.currentValues = self.materialView.item(self.materialView.focus(), option = 'values')

        id = int(self.currentValues[1])
        args = self.matArgsEntry.get()
        material = self.materialCombo.get()
        matType = self.matTypeCombo.get()
        
        self.model.materials[id] = [material, matType, args]
        print 'Modified material: '+material+' '+matType+' '+str(id)+' '+args
        self.updateMaterialLists()
        pass
    
    def deleteMaterial(self):
        self.currentValues = self.materialView.item(self.materialView.focus(), option = 'values')
        if len(self.currentValues) == 0:
            pass
        else:
            id = int(self.currentValues[1])
            self.model.deleteMaterial(id)
            self.updateMaterialLists()
            print 'deleteMaterial'
        pass
    
    def updateMaterialLists(self):        
        
        matIds = self.model.materials.keys()
        
        if len(self.treeItemIdList) == 0:
            pass
        else:
            for treeItemId in self.treeItemIdList:
                self.materialView.delete(treeItemId)
            self.treeItemIdList = []

        for id in matIds:
            material = self.model.materials[id]
            treeItemId = self.materialView.insert('', 'end', text=material[0], values=(material[1], str(id), material[2]))
            self.treeItemIdList.append(treeItemId)
        pass
        
    def updateMatTypeCombo(self,*args):
        print 'updateMatTypeCombo'
        
        material = self.materialCombo.get()
        matTypeList = []
        for mat in self.matTypeDict[material]:
            matTypeList.append(mat[0])
        self.matTypeCombo['values'] = tuple(matTypeList)
        self.matTypeList = matTypeList
        pass
    
    def updateMatArgsCombo(self,*args):
        print 'updateMatArgsCombo'
        material = self.materialCombo.get()
        matType = self.matTypeCombo.get()
        i = self.matTypeList.index(matType)
        cmdArgs = self.matTypeDict[material][i][1]
        self.matArgsEntry.delete(0,'end')
        self.matArgsEntry.insert(0,cmdArgs)
        pass
    
    def readMaterialsDatabase(self):
        fname = 'materials.db'
        fid = open(fname,'r')
        
        materialList = []
        matTypeDict = {}
        
        i = 1
        for line in fid:
            if line[0] == '#' or len(line) == 0:
                pass
            else:
                spline = line.split()
                mat = spline[0]
                if mat not in materialList:
                    materialList.append(mat)
                if matTypeDict.has_key(mat) == False:
                    matTypeDict[mat] = []
                cmd = ''
                for comp in spline[3:]:
                    cmd += ' '+comp
                matTypeDict[mat].append((spline[1],cmd))
            #print i
            i += 1
        self.materialList = materialList
        self.matTypeDict = matTypeDict
        
        fid.close()
    
    def updateWidgets(self,model):
        self.model = model
        self.updateMaterialLists()
        pass
# ------------------------------------------------------------------------------
# TAB: Assign
# ------------------------------------------------------------------------------
class FrameAssign(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.grpTreeIdDict = {}
        
        #+Add Button
        self.addCmd = Button(self, text = '+ Add object', width = 1, command=self.addElementToAssign, state='disabled')
        self.addCmd.grid(column = 0, row = 0, columnspan = 3, sticky=EW)
        
        #Fake frame to set width
        self.dummyFrame = Frame(self, width = 50)
        self.dummyFrame.grid(column = 3, row = 0)
        
        #Tree for model navigation
        self.modelNavigator = Treeview(self)
        self.modelNavigator.grid(column = 0, row = 1, columnspan = 2, sticky = NSEW)
        self.scrollModelV = Scrollbar(self,command = self.modelNavigator.yview,orient = VERTICAL)
        self.scrollModelV.grid(column=2,row = 1,sticky = NSEW)
        self.scrollModelH = Scrollbar(self,command = self.modelNavigator.xview,orient = HORIZONTAL)
        self.scrollModelH.grid(column=0,columnspan=2,row = 2,sticky = NSEW)
        self.modelNavigator['yscrollcommand'] = self.scrollModelV.set
        self.modelNavigator['xscrollcommand'] = self.scrollModelH.set
                
        #Frame to view current selection relevant data
        self.currentSelection = NoneAssigner(self)
        self.currentSelection.createWidgets()
        self.currentSelection.grid(column = 3, row = 1, rowspan = 2,sticky=NSEW)
        
        
        #Command editor object
        self.editCmd = cmdEditBox(self)
        self.editCmd.grid(row = 3, column=3, sticky=NSEW)
        self.editCmd.subscribe(self)
        
        #Command navigator (list) and buttons
        self.cmdNavigator = Listbox(self)
        self.cmdNavigator.grid(column = 0, columnspan = 1, row = 3, sticky = NSEW)
        self.scrollCmds = Scrollbar(self,command = self.cmdNavigator.yview,orient = VERTICAL)
        self.scrollCmds.grid(column=1,row = 3,sticky = NSEW)
        self.cmdNavigator['yscrollcommand'] = self.scrollCmds.set
        self.cmdNavigator.bind('<Double-1>',self.viewCommand)
        
        self.cmdNavFrame = Frame(self)
        self.cmdNavFrame.grid(column = 2, row = 3)
        
        #self.cmdNewCmd = Button(self.cmdNavFrame, text = 'New', width=3)
        #self.cmdNewCmd.pack()
        self.cmdNavUpCmd = Button(self.cmdNavFrame, text = 'Up', width=3, command = self.movCmdUpList)
        self.cmdNavUpCmd.pack()
        self.cmdNavRemCmd = Button(self.cmdNavFrame, text = 'X', width=3, command = self.deleteCmdFromList)
        self.cmdNavRemCmd.pack()
        self.cmdNavDnCmd = Button(self.cmdNavFrame, text = 'Dn', width=3, command = self.movCmdDownList)
        self.cmdNavDnCmd.pack()
        
        pass
    
    def updateWidgets(self, model):
        #Incorporate model o enable data access
        self.model = model
        
        #        self['command'] = self.addElementToAssign(model)
        
        #Generate tree root
        self.rootPhys = self.modelNavigator.insert('', 'end',text='Physical Groups',tags=('addDisabled'))
        self.rootEltype = self.modelNavigator.insert('', 'end',text='By Element Type',tags=('addDisabled'))
        self.rootAllElements = self.modelNavigator.insert('', 'end',text='All Elements',tags=('element','addEnabled'), values='allelements')
        self.rootAllNodes = self.modelNavigator.insert('', 'end',text='All Nodes',tags=('node','addEnabled'), values='allnodes')
        self.modelNavigator.selection_set(self.rootPhys)
        
        self.cmdList = model.assigns.keys()
        
        #Generate model tree
        i = 0
        
        #Group loop (add model physical groups)
        for grp in model.physgrp:
            numElemsInGrp = len(model.elemPG[i])
            numNodesInGrp = len(model.nodePG[i])
            
            #Gen group folder
            id = self.modelNavigator.insert(self.rootPhys, 'end',text=model.genGroupNumber(grp),tags=('group','addDisabled'),values='grp{0}'.format(grp))
            self.grpTreeIdDict[id] = grp
            
            #Gen root (folders) for elements and nodes 
            idElems = self.modelNavigator.insert(id,'end',text='Elements'+' ({0} elements.)'.format(numElemsInGrp),tags=('element','addEnabled'),values='egr'+str(grp))
            idNodes = self.modelNavigator.insert(id,'end',text='Nodes'+' ({0} nodes)'.format(numNodesInGrp),tags=('node','addEnabled'),values = 'ngr'+str(grp))
            
            #Elements in group loop (add model elements)
            for ele in model.elemPG[i]:
                idThisEle = self.modelNavigator.insert(idElems,'end',text='Element {0} ({1} Nodes)'.format(ele,len(model.elemDict[ele-1].nodes)),values='ele{0}'.format(ele),tags=('element','addEnabled'))
                
                #Nodes in element in group loop (add model nodes)
                for nod in model.elemDict[ele-1].nodes:
                    self.modelNavigator.insert(idThisEle, 'end',text='Node     {0}'.format(nod),values='nod{0}'.format(nod),tags=('node','addEnabled'))
            
            #Nodes in group loop
            for nod in model.nodePG[i]:
                self.modelNavigator.insert(idNodes, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node','addEnabled'))
            pass
            
            #Advance counter
            i += 1
        
        for type in model.elemTypes.keys():
            exElem = model.elemTypes[type].elemList[0]
            idThisType = self.modelNavigator.insert(self.rootEltype,'end',text='Type '+str(type)+ ' ({0} Nodes)'.format(len(model.elemDict[exElem-1].nodes)),tags=('element','addEnabled'),values='ety'+str(type))
            for ele in model.elemTypes[type].elemList:
                idThisEle = self.modelNavigator.insert(idThisType,'end',text='Element {0}'.format(ele),values='ele{0}'.format(ele),tags=('element','addEnabled'))
                
                #Nodes in element in group loop (add model nodes)
                for nod in model.elemDict[ele-1].nodes:
                    self.modelNavigator.insert(idThisEle, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node','addEnabled'))
            pass
               
        
        #Bind commands (actions) to tags 
        #self.modelNavigator.tag_bind('group','<ButtonPress-1><ButtonRelease-1>',self.groupSelected)
        self.modelNavigator.tag_bind('element','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)
        self.modelNavigator.tag_bind('node','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)
        self.modelNavigator.tag_bind('none','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)        
        self.modelNavigator.tag_bind('addEnabled','<ButtonPress-1><ButtonRelease-1>',self.enableSelection)        
        self.modelNavigator.tag_bind('addDisabled','<ButtonPress-1><ButtonRelease-1>',self.disableSelection)        
        
        self.modelNavigator.bind('<Double-1>',self.addElementToAssign)
        
        self.editCmd.createWidgets(self.model)
        if len(self.model.assigns) == 0:
            self.editCmd.disableWidgets()
        
        self.updateCmdList()
        pass
    
    def uponSelection(self,event):
        self.currentValues = self.modelNavigator.item(self.modelNavigator.focus(), option = 'values')[0]
        
        print self.currentValues
        
        self.currentSelection.grid_forget()
        if self.currentValues[:3] == 'egr':
            self.currentSelection = ElementAssigner(self)
        elif self.currentValues[:3] == 'ngr':
            self.currentSelection = NodeAssigner(self)
        elif self.currentValues[:3] == 'ele':
            self.currentSelection = ElementAssigner(self)
        elif self.currentValues[:3] == 'nod':
            self.currentSelection = NodeAssigner(self)
        else:
            self.currentSelection = NoneAssigner(self)
            
        self.currentSelection.createWidgets(self.model,self.currentValues)
        self.currentSelection.grid(column = 3, row = 1, rowspan = 2,sticky=NSEW)
        pass

    def addElementToAssign(self, extra='null'):
        if len(self.model.assigns) == 0:
            self.editCmd.enableWidgets()
            self.editCmd.addObjectToList(self.currentValues)
        else:
            self.editCmd.addObjectToList(self.currentValues)
        ncmds = len(self.model.assigns)
        self.editCmd.cmdNameEntry.delete(0,'end')
        self.editCmd.cmdNameEntry.insert(0,'CMD_{0:03.0f}'.format(float(ncmds+1)))
        #editCmd.
    
    def enableSelection(self,event):
        self.addCmd['state'] = 'normal'
        pass 
    
    def commandAdded(self,cmdObject,name):
        self.model.addCommand(name, cmdObject)
        self.cmdList = StringVar(value = self.model.cmdList)
        self.updateCmdList()
    
    def disableSelection(self,event):
        self.addCmd['state'] = 'disabled'
        pass
        
    def updateCmdList(self):
        self.cmdNavigator.delete(0,'end')
        for item in self.model.cmdList:
            self.cmdNavigator.insert('end',item)
        pass
        
    def deleteCmdFromList(self):
        curSelect = self.cmdNavigator.curselection()
        if len(curSelect) > 0:
            currentIndex = int(curSelect[0])
            name = self.model.cmdList[currentIndex]
            self.model.deleteCommand(name)
            self.updateCmdList()
        pass
        
    def movCmdUpList(self):
        curSelect = self.cmdNavigator.curselection()
        if len(curSelect) > 0:
            currentIndex = int(curSelect[0])
            name = self.model.cmdList[currentIndex]
            self.model.promoteCmd(name)
            self.updateCmdList()
        pass
        
    def movCmdDownList(self):
        curSelect = self.cmdNavigator.curselection()
        if len(curSelect) > 0:
            currentIndex = int(curSelect[0])
            name = self.model.cmdList[currentIndex]
            self.model.demoteCmd(name)
            self.updateCmdList()
        pass
    
    def viewCommand(self,event):
        curSelect = self.cmdNavigator.curselection()
        currentIndex = int(curSelect[0])
        name = self.model.cmdList[currentIndex]
        
        cmdToView = self.model.assigns[name]
        
        cmd = cmdToView.instruction
        objectList = cmdToView.objectList
        applyTo = cmdToView.applyTo
        applyToElemType= cmdToView.applyToElemType
        self.editCmd.modifyThisCmd(name, cmd, objectList, applyTo,applyToElemType)
        
        #        if applyTo == 'nodes':
        #            self.editCmd.disableCombo()
        #        elif applyTo == 'elements':
        #            self.editCmd.disableCombo()
        #            self.editCmd.enableCombo()
        
        print 'CMDName    = '+name+'\n'
        print 'Command    = '+cmdToView.instruction+'\n'
        print 'ApplyTo    = '+cmdToView.applyTo+'\n'
        print 'ObjectList = '+cmdToView.objectList+'\n'
        print 'ElemType   = '+cmdToView.applyToElemType+'\n'
        

# ------------------------------------------------------------------------------
# TAB: ASSIGN -> Frame: ASSIGNERS
# ------------------------------------------------------------------------------
class NoneAssigner(Labelframe):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        pass
    
    def createWidgets(self, model='void', currentValues='void'):
        self['text'] = 'Current Selection: None'
        self.title = Label(self,text='Select an element group')
        self.title.pack()
        pass

class NodeAssigner(Labelframe):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        pass
    
    def createWidgets(self, model, currentValues):
        self['text'] = 'Current Selection: '+currentValues
        
        #Frame Title
        self.title = Label(self,text='Node Assigner')
        self.title.grid(column=0,row=0)
        
        #Show Node Data
        self.nodeIdTxt = Label(self, text = 'Node Id:')
        self.nodeIdTxt.grid(column = 0, row = 0)
        self.nodeIdNum = Label(self, text = '')
        self.nodeIdNum.grid(column = 0, row = 0)
        
        self.coordShowerLabel = Label(self, text='Node Coords:')
        self.coordShowerLabel.grid(column=0,row=0)
        pass

class ElementAssigner(Labelframe):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        pass
    
    def createWidgets(self, model, currentValues):
        
        self['text'] = 'Current Selection: '+currentValues
        
        self.title = Label(self,text='Element Assigner')
        self.title.pack()
        pass


class infoBox(Labelframe):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
        
    def createWidgets(self,model,current):
        
        #Initialize text header
        if current[:3] == 'ele':
            self['text'] = 'Information for single element '+current[3:]
        if current[:3] == 'egr':
            self['text'] = 'Information for element group '+current[3:]
        if current[:3] == 'nod':
            self['text'] = 'Information for single node '+current[3:]
        if current[:3] == 'ngr':
            self['text'] = 'Information for node group '+current[3:]
        

class cmdEditBox(Labelframe):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        
        self.observers = []
        pass
    
    def createWidgets(self,model):
        self['text'] = 'Edit Command'
        
        #ncmds = len(model.assigns)
        self.model = model
        
        #CMDNAME
        self.cmdNameTxt = Label(self,text = 'Command Name: ')
        self.cmdNameTxt.grid(row = 0, column = 0,sticky=E)
        self.cmdNameEntry = Entry(self)
        self.cmdNameEntry.delete(0,'end')
        #self.cmdNameEntry.insert(0,'CMD_{0:03.0f}'.format(float(ncmds+1)))
        self.cmdNameEntry.grid(row = 0, column = 1, sticky=W)
        
        #CMD_INSTRUCTION
        self.cmdInstructionTxt = Label(self,text = 'OpenSEES CMD:')
        self.cmdInstructionTxt.grid(row = 1, column = 0,sticky=E)
        self.cmdInstructionEntry = Entry(self,width=50)
        self.cmdInstructionEntry.grid(row = 1, column = 1,sticky=EW)
        
        #CMD_INSTRUCTION
        self.applyToTxt = Label(self,text = 'Apply Command To:')
        self.applyToTxt.grid(row = 2, column = 0,sticky=W)
        self.applyToEntryTxt = ''
        self.applyToEntry = Entry(self, textvariable = self.applyToEntryTxt)
        #self.applyToEntry.insert('')
        self.applyToEntry.grid(row = 2, column = 1,sticky=EW)
        
        #Select nodes or elements
        
        self.nodElemLabelFrame = Labelframe(self,text = 'Apply command to the following objects in group:')
        self.nodElemLabelFrame.grid(row=3, column=0, columnspan = 2, sticky=EW)
        
        self.assignToObjectType = StringVar()
        self.elementTypesVar = StringVar()
        
        self.elementTypeCombo = Combobox(self.nodElemLabelFrame, textvariable =  self.elementTypesVar)
        self.assignNodesRadio = Radiobutton(self.nodElemLabelFrame, text='Nodes', variable=self.assignToObjectType, value='nodes', command = self.disableCombo)
        self.assignElementsRadio = Radiobutton(self.nodElemLabelFrame, text='Elements', variable=self.assignToObjectType, value='elements' , command = self.enableCombo)
        
        
        self.assignNodesRadio.pack(side='left')
        self.assignElementsRadio.pack(side='left')
        self.elementTypeCombo.pack(side='left')
        
        self.elementTypeCombo['state'] = 'disabled'
        
        self.assignToObjectType.set('nodes')
        
        #CMD_INSTRUCTION
        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row = 4, column = 0, columnspan = 2,sticky=EW)
        
        self.addCMDButton = Button(self.buttonFrame,text = 'Add/Modify', command = self.addThisCmd)
        self.addCMDButton.pack(side = 'left', anchor=CENTER)
        self.clearButton = Button(self.buttonFrame,text = 'Clear', command = self.clearForm)            
        self.clearButton.pack(side = 'left', anchor=CENTER)
    
    def addThisCmd(self):
        name = self.cmdNameEntry.get()
        
        if len(name) == 0:
            Mes.showinfo(message = 'Command must have a name. Command not added.')
            print 'Command not added.'
        else:
            if name in self.model.assigns.keys():
                Mes.showinfo(message = 'Command already exists. Command not added.')
                print 'Command not added.'
            else:
                cmd = self.cmdInstructionEntry.get()
                
                if len(cmd) == 0:
                    Mes.showinfo(message = 'Empty command. Command not added.')
                    print 'Command not added.'
                else:
                    objectList = self.applyToEntry.get()
                    applyTo = self.assignToObjectType.get()
                    applyToElemType = self.elementTypeCombo.get()
                    cmdObject = OpenSEESassign(cmd,objectList,applyTo,applyToElemType)
                
                    for obs in self.observers:
                        obs.commandAdded(cmdObject, name)
                    print str(len(self.model.assigns)) + '\n'
                    print self.model.assigns.keys()
        pass
        
    def modifyThisCmd(self,name,cmd,objectList,applyTo,applyToElementTypes):
        self.applyToEntry.delete(0,'end')
        self.applyToEntry.insert(0,objectList)
        self.cmdNameEntry.delete(0,'end')
        self.cmdNameEntry.insert(0,name)
        self.assignToObjectType.set(applyTo)
        self.cmdInstructionEntry.delete(0,'end')
        self.cmdInstructionEntry.insert(0,cmd)
        
        if applyTo == 'nodes':
            self.disableCombo()
        if applyTo == 'elements':
            self.disableCombo()
            self.enableCombo()
            self.elementTypeCombo.set(str(applyToElementTypes))
        pass
    
    def clearForm(self):
        self.cmdInstructionEntry.delete(0,'end')
        self.cmdNameEntry.delete(0,'end')
        self.applyToEntry.delete(0,'end')
        #self.assignToObjectType.delete(0,'end')
        pass
    
    
    def addObjectToList(self, object):
        prev = self.applyToEntry.get()
        self.applyToEntry.delete(0,'end')
        if len(prev) == 0:
            self.applyToEntry.insert(0,object)
        else:
            self.applyToEntry.insert(0,prev+'+'+object)
        print 'added '+object
        
    def updateWidgets(self, model, currentValue):
        pass
    
    def disableWidgets(self):
        self.cmdNameEntry['state'] = 'disabled'
        self.cmdInstructionEntry['state'] = 'disabled'
        self.applyToEntry['state'] = 'disabled'
        self.addCMDButton['state'] = 'disabled'
        #self.editCMDButton['state'] = 'disabled'
        
    def enableWidgets(self):
        
        
        self.cmdNameEntry['state'] = 'normal'
        self.cmdInstructionEntry['state'] = 'normal'
        self.applyToEntry['state'] = 'normal'
        self.addCMDButton['state'] = 'normal'
    
    def disableCombo(self):
        self.elementTypeCombo.delete(0,'end')
        self.elementTypeCombo['state'] = 'disabled'
        pass
        
    def enableCombo(self):
        self.elementTypeCombo['state'] = 'normal'
        self.elementTypeCombo.delete(0,'end')
        values = []
        values.append('All')
   
        for type in self.model.elemTypes.keys():
            exElem = self.model.elemTypes[type].elemList[0]
            values.append('{0}'.format(type,len(self.model.elemDict[exElem-1].nodes)))
            #values.append('Type {0:03.0f} ({1} Nodes)'.format(type,len(self.model.elemDict[exElem-1].nodes)))
            
        self.elementTypeCombo['values'] = tuple(values)
        self.elementTypeCombo.set('All')
        pass
        
    def subscribe(self, observer):
        self.observers.append(observer)
    
class CmdNavigatorList(Listbox):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        pass
    def updateList(self,model):
        pass
# ------------------------------------------------------------------------------
# TAB: Patterns
# ------------------------------------------------------------------------------
class FramePatterns(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
        
    def createWidgets(self):
        pass


# ------------------------------------------------------------------------------
# TAB: Recorders
# ------------------------------------------------------------------------------
class FrameRecorders(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        pass



# ------------------------------------------------------------------------------
# TAB: Analysis
# ------------------------------------------------------------------------------
class FrameAnalysis(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        pass

# ------------------------------------------------------------------------------
# TAB: Analysis
# ------------------------------------------------------------------------------
class FrameVariables(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        pass


# ------------------------------------------------------------------------------
# Master TAB
# ------------------------------------------------------------------------------
class GenTabMaster(Notebook):
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        self.tabMaster = Notebook(self.master)