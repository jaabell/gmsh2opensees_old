from Tkinter import *
from ttk import *
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
        self.modelNavigator = Treeview(self)
        self.modelNavigator.pack(side = 'left', fill='both')
        self.grpTreeIdDict = {}
        
        self.currentSelection = NoneAssigner(self)
        self.currentSelection.createWidgets()
        self.currentSelection.pack(side = 'left', fill='both')
        pass
    
    def updateWidgets(self, model):
        #Incorporate model o enable data access
        self.model = model
        
        #Generate tree root
        self.rootId = self.modelNavigator.insert('', 'end',text='Physical Groups')
        self.modelNavigator.selection_set(self.rootId)
        
        #Generate model tree
        i = 0
        
        #Group loop (add model physical groups)
        for grp in model.physgrp:
            numElemsInGrp = len(model.elemPG[i])
            numNodesInGrp = len(model.nodePG[i])
            
            #Gen group folder
            id = self.modelNavigator.insert(self.rootId, 'end',text=model.genGroupNumber(grp),tags=('group'),values='grp{0}'.format(grp))
            self.grpTreeIdDict[id] = grp
            
            #Gen root (folders) for elements and nodes 
            idElems = self.modelNavigator.insert(id,'end',text='Elements'+' ({0} elems.)'.format(numElemsInGrp),tags=('none'))
            idNodes = self.modelNavigator.insert(id,'end',text='Nodes'+' ({0} elems.)'.format(numNodesInGrp),tags=('none'))
            
            #Elements in group loop (add model elements)
            for ele in model.elemPG[i]:
                idThisEle = self.modelNavigator.insert(idElems,'end',text='Element {0} ({1} Nodes)'.format(ele,len(model.elemDict[ele-1].nodes)),values='ele{0}'.format(ele),tags=('element'))
                
                #Nodes in element in group loop (add model nodes)
                for nod in model.elemDict[ele-1].nodes:
                    self.modelNavigator.insert(idThisEle, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node'))
            
            #Nodes in group loop
            for nod in model.nodePG[i]:
                self.modelNavigator.insert(idNodes, 'end',text='Node {0}'.format(nod),values='nod{0}'.format(nod),tags=('node'))
            pass
            
            #Advance counter
            i += 1
            
        #Bind commands (actions) to tags 
        self.modelNavigator.tag_bind('group','<ButtonPress-1><ButtonRelease-1>',self.groupSelected)
        self.modelNavigator.tag_bind('element','<1>',self.elementSelected)
        self.modelNavigator.tag_bind('node','<1>',self.nodeSelected)
        self.modelNavigator.tag_bind('none','<1>',self.noneSelected)
        pass
    
    def groupSelected(self,event):
        
        grupNum = self.modelNavigator.item(self.modelNavigator.focus(), option = 'values')[0]
        
        self.currentSelection.pack_forget()
        self.currentSelection = GroupAssigner(self)
        self.currentSelection.createWidgets()
        self.currentSelection.pack(side = 'left', fill='both')
        
        print grupNum
        print self.modelNavigator.selection()
        #        print event
        pass
    
    def elementSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = ElementAssigner(self)
        self.currentSelection.createWidgets()
        self.currentSelection.pack(side = 'left', fill='both')
        print self.modelNavigator.selection()
        pass
    
    def nodeSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = NodeAssigner(self)
        self.currentSelection.createWidgets()
        self.currentSelection.pack(side = 'left', fill='both')
        print self.modelNavigator.selection()
        #print event.data
        pass
    
    def noneSelected(self,event):
        self.currentSelection.pack_forget()
        self.currentSelection = NoneAssigner(self)
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
        self.title = Label(self,text='Select an element group')
        self.title.pack()
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
        pass

class NodeAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        
        #Frame Title
        self.title = Label(self,text='Node Assigner')
        self.title.grid(column=0,row=0)
        
        #Show Node Data
        
        self.coordShower = Label(self, text='Node Coords:')
        self.coordShower.grid(column=0,row=1)
        pass
        
    def destroyWidgets(self):
        self.title.pack_forget()
        pass

class GroupAssigner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        pass
    
    def createWidgets(self):
        self.title = Label(self,text='Group Assigner')
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
        self.title = Label(self,text='Element Assigner')
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