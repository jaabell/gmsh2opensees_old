from Tkinter import *
from ttk import *
#from Tkinter.ttk import *
#from pyTtk import *



# ------------------------------------------------------------------------------
# TAB: Geometry
# ------------------------------------------------------------------------------

class FrameGeom(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
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
    
    def updateWidgets(self,model):
        self.labelPath['text'] = model.sourceFile
        self.labelNnodes['text'] = '{0}'.format(model.Nnodes)
        self.labelNelem['text'] = '{0}'.format(model.Nelem)



# ------------------------------------------------------------------------------
# TAB: Assign
# ------------------------------------------------------------------------------

class FrameAssign(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.modelNavigator = Treeview(self)
        self.modelNavigator.pack(side = 'left', fill='both')
        self.grpTreeIdDict = {}
        
        self.currentSelection = NoneAssigner(self)
        self.currentSelection.pack(side = 'left', fill='both')
        pass
    
    def updateWidgets(self,model):
        self.modelNavigator.tag_bind('group','<1>',self.groupSelected)
        self.modelNavigator.tag_bind('element','<1>',self.elementSelected)
        self.modelNavigator.tag_bind('node','<1>',self.nodeSelected)
        self.modelNavigator.tag_bind('none','<1>',self.noneSelected)
        
        self.rootId = self.modelNavigator.insert('', 'end',text='Physical Groups')
        #print rootId
        i = 0
        for grp in model.physgrp:
            numElemsInGrp = len(model.elemPG[i])
            id = self.modelNavigator.insert(self.rootId, 'end',text=model.genGroupNumber(grp)+' ({0} elems.)'.format(numElemsInGrp),tags=('group'))
            self.grpTreeIdDict[id] = grp
            idElems = self.modelNavigator.insert(id,'end',text='Elements',tags=('none'))
            idNodes = self.modelNavigator.insert(id,'end',text='Nodes',tags=('none'))
            for ele in model.elemPG[i]:
                idThisEle = self.modelNavigator.insert(idElems,'end',text='Element {0} ({1} Nodes)'.format(ele,len(model.elemDict[ele-1].nodes)),values='ele{0}'.format(ele),tags=('element'))
                for nod in model.elemDict[ele-1].nodes:
                    self.modelNavigator.insert(idThisEle, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node'))
            for nod in model.nodePG[i]:
                self.modelNavigator.insert(idNodes, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node'))
            pass
            i += 1
        pass
    #@staticmethod
    def groupSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = GroupAssigner(self.model)
        self.currentSelection.createWidgets(self.model)
        self.currentSelection.pack(side = 'left', fill='both')
        
        print self.modelNavigator.selection()
        pass
    #@staticmethod
    def elementSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = ElementAssigner(self.model)
        self.currentSelection.createWidgets(self.model)
        self.currentSelection.pack(side = 'left', fill='both')
        print self.modelNavigator.selection()
        pass
    #@staticmethod
    def nodeSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = NodeAssigner(self.model)
        self.currentSelection.createWidgets(self.model)
        self.currentSelection.pack(side = 'left', fill='both')
        print self.modelNavigator.selection()
        pass
    #@staticmethod
    def noneSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = NoneAssigner()
        self.currentSelection.createWidgets()
        self.currentSelection.pack(side = 'left', fill='both')
        print self.modelNavigator.selection()
        pass



# ------------------------------------------------------------------------------
# TAB: ASSIGN -> Frame: ASSIGNERS
# ------------------------------------------------------------------------------

class NoneAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.title = Label(text='Select an element group')
        self.title.pack()
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
        pass

class NodeAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self,model):
        self.title = Label(text='Node Assigner')
        self.title.pack()
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
        pass

class GroupAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.title = Label(text='Group Assigner')
        self.title.pack()
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
        pass

class ElementAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.title = Label(text='Element Assigner')
        self.title.pack()
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
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