# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 07:53:48 2010

@author: jose
"""
from Tkinter import *
from ttk import *
import Tkinter as TkLib
from libgmsh2opensees import *

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
        self.rootAllElements = self.modelNavigator.insert('', 'end',text='All Elements',tags=('addDisabled'))
        self.rootAllNodes = self.modelNavigator.insert('', 'end',text='All Nodes',tags=('addDisabled'))
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
            pass
               
        
        #Bind commands (actions) to tags 
        #self.modelNavigator.tag_bind('group','<ButtonPress-1><ButtonRelease-1>',self.groupSelected)
        self.modelNavigator.tag_bind('element','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)
        self.modelNavigator.tag_bind('node','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)
        self.modelNavigator.tag_bind('none','<ButtonPress-1><ButtonRelease-1>',self.uponSelection)        
        self.modelNavigator.tag_bind('addEnabled','<ButtonPress-1><ButtonRelease-1>',self.enableSelection)        
        self.modelNavigator.tag_bind('addDisabled','<ButtonPress-1><ButtonRelease-1>',self.disableSelection)        
        
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

    def addElementToAssign(self):
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
        self.model.assigns[name] = cmdObject
        self.cmdList = StringVar(value = self.model.assigns.keys())
        self.updateCmdList()
    
    def disableSelection(self,event):
        self.addCmd['state'] = 'disabled'
        pass
        
    def updateCmdList(self):
        self.cmdNavigator.delete(0,'end')
        for item in self.model.assigns.keys():
            self.cmdNavigator.insert('end',item)
        pass
        
    def deleteCmdFromList(self,name):
        self.model.assigns.pop(name)
        self.updateCmdList()
        pass
        
    def movCmdUpList(self):
        currentIndex = self.cmdNavigator.curselection()
        name = self.model.assigns.keys()[currentIndex[0]]
        cmdList = self.model.assigns.promoteCmd(name)
        self.updateCmdList()
        pass
        
    def movCmdDownList(self):
        currentIndex = self.cmdNavigator.curselection()
        name = self.model.assigns.keys()[currentIndex[0]]
        cmdList = self.model.assigns.demoteCmd(name)
        self.updateCmdList()
        pass
        

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
        self.cmdNameTxt.grid(row = 0, column = 0,sticky=EW)
        self.cmdNameEntry = Entry(self)
        self.cmdNameEntry.delete(0,'end')
        #self.cmdNameEntry.insert(0,'CMD_{0:03.0f}'.format(float(ncmds+1)))
        self.cmdNameEntry.grid(row = 0, column = 1)
        
        #CMD_INSTRUCTION
        self.cmdInstructionTxt = Label(self,text = 'OpenSEES CMD:')
        self.cmdInstructionTxt.grid(row = 1, column = 0)
        self.cmdInstructionEntry = Entry(self,width=50)
        self.cmdInstructionEntry.grid(row = 1, column = 1,sticky=EW)
        
        #CMD_INSTRUCTION
        self.applyToTxt = Label(self,text = 'Apply Command To:')
        self.applyToTxt.grid(row = 2, column = 0)
        self.applyToEntryTxt = ''
        self.applyToEntry = Entry(self, textvariable = self.applyToEntryTxt)
        #self.applyToEntry.insert('')
        self.applyToEntry.grid(row = 2, column = 1,sticky=EW)
        
        #Select nodes or elements
        
        self.nodElemLabelFrame = Labelframe(self,text = 'Apply command to the following objects in group:')
        self.nodElemLabelFrame.grid(row=3, column=0, columnspan = 2, sticky=EW)
        
        self.assignToObjectType = StringVar()
        self.assignNodesRadio = Radiobutton(self.nodElemLabelFrame, text='Nodes', variable=self.assignToObjectType, value='nodes')
        self.assignElementsRadio = Radiobutton(self.nodElemLabelFrame, text='Elements', variable=self.assignToObjectType, value='elements')
        
        self.assignNodesRadio.pack(side='left')
        self.assignElementsRadio.pack(side='left')
        
        #CMD_INSTRUCTION
        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row = 4, column = 0, columnspan = 2,sticky=EW)
        
        self.addCMDButton = Button(self.buttonFrame,text = 'Add/Modify', command = self.addThisCmd)
        self.addCMDButton.pack(side = 'left')
        #self.editCMDButton = Button(self.buttonFrame, text = 'Modify Cmd.', command = self.modifyThisCmd)            
        #self.editCMDButton.pack(side = 'left')
        self.clearButton = Button(self.buttonFrame,text = 'Clear', command = self.clearForm)            
        self.clearButton.pack(side = 'left')
    
    def addThisCmd(self):
        name = self.cmdNameEntry.get()
        cmd = self.cmdInstructionEntry.get()
        objectList = self.applyToEntry.get()
        applyTo = self.assignToObjectType.get()
        cmdObject = OpenSEESassign(cmd,objectList,applyTo)
        
        for obs in self.observers:
            obs.commandAdded(cmdObject, name)
        
        #self.model.assigns[name] = OpenSEESassign(cmd,objectList,applyTo)
        
        print str(len(self.model.assigns)) + '\n'
        print self.model.assigns.keys()
        pass
        
    def modifyThisCmd(self):
        self.addThisCmd()
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
        #self.editCMDButton['state'] = 'normal'
    def subscribe(self, observer):
        self.observers.append(observer)
    
class CmdNavigatorList(Listbox):
    def __init__(self, parent):
        Labelframe.__init__(self, parent)
        pass
    def updateList(self,model):
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
# Master TAB
# ------------------------------------------------------------------------------
class GenTabMaster(Notebook):
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        self.tabMaster = Notebook(self.master)