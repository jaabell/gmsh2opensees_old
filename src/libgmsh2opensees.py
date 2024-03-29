# -*- coding: utf-8 -*-
# gmsh2opensees: A GUI application to transform .gmsh output files
# into opensees commands and read ouput back into gmsh
#Copyright (C) 2010 José Antonio Abell Mena
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from scipy import *
from libtools import *
import pickle

# ===============================
# Main Model Class
# ===============================
class Model:
    #
    #Model creation and input methods
    #
    @staticmethod
    def loadFromGmshFile(fname):
        # ------------------------------------------------------------------------------
        # Lectura de Archivo de Origen
        # ------------------------------------------------------------------------------
        # self.physgrp: Grupo fisico del elemento segun el archivo .msh
        # self.XYZ: Coordenadas nodales. self.XYZ.shape = (Nnodes,3)
        # self.elemDict: Diccionario de elementos. Lista de largo Nelem. Cada elemento tiene
        # siguientes campos: 
        #      elnum  : Numero de elemento
        #      eltype : Tipo de elemento (ver documentacion gmsh)
        #      ntags  : Numero de tags asociados al elemento (tipico = 3)
        #      tags   : Tags (Tipico 3 tags). tags[0] = grupo fisico
        #      nodes  : Nodos asociados al elemento
        #
        model = Model()
        
        model.success = 0
        
        fid = open(fname,'r')
        
        inNodes = 0
        inElements = 0
        ncount = -1
        ecount = -1
        model.physgrp = []
        for line in fid:
            
            #Detectar campo event
            if line[0] == '$':
                if line.find('Nodes') > 0:
                    inNodes = 1
                if line.find('EndNodes')  > 0:
                    inNodes = 0
                if line.find('Elements')  > 0:
                    inElements = 1
                if line.find('EndElements')  > 0:
                    inElements = 0
                #print line#+'{0} {1}'.format(inNodes,inElements)
            
            #Leer nodos
            if inNodes:
                if ncount == 0:
                    Nnodes = int(line)
                    model.XYZ = zeros((Nnodes,3))
                elif ncount > 0:
                    model.XYZ[ncount-1,:] = array(line.split(),'double')[1:]
                ncount+=1
                
            #Leer elementos
            if inElements:
        
                if ecount == 0:
                    Nelem = int(line)
                    model.elemDict = []
                elif ecount > 0:
                    model.elemDict.append(Elem())
                    spline = line.split()
                    elnum = int(spline[0])
                    eltype = int(spline[1])
                    ntags = int(spline[2])
                    
                    tags = zeros(ntags)
                    idx = 0
                    for tg in tags:
                        tags[idx] = uint32(spline[3+idx])
                        idx += 1
                    nodes = array(spline[3+idx:],uint32)
                    model.elemDict[ecount-1].elnum = elnum
                    model.elemDict[ecount-1].eltype = eltype
                    model.elemDict[ecount-1].ntags = ntags
                    model.elemDict[ecount-1].tags = tags
                    model.elemDict[ecount-1].nodes = nodes
                    if tags[0] not in model.physgrp:
                        model.physgrp.append(uint32(tags[0]))
                ecount+=1
        fid.close()
        #Reportar numero de elementos y nodos
        print '{0} Elements'.format(Nelem)
        print '{0} Nodes'.format(Nnodes)
        
        model.elemPG = []
        model.nodePG = []
        i = 0
        for ph in model.physgrp:
            elemInGrp = []
            nodesInGrp = []
            for elem in model.elemDict:
                if elem.tags[0] == ph:
                    elemInGrp.append(elem.elnum)
                    for nd in elem.nodes:
                        if nd not in nodesInGrp:
                            nodesInGrp.append(nd)
            model.elemPG.append(elemInGrp)
            model.nodePG.append(nodesInGrp)
            i += 1
        
        model.Nnodes = Nnodes
        model.Nelem = Nelem
        model.success = 1
        model.sourceFile = fname
        
        #Initialize stuff
        if model.success:
            model.formElemTypes()
            model.assigns = {}
            model.recorders = []
            model.analysisOptions = {}
            model.materials = {}
            model.cmdList = []
            model.variables = {}
            
            # Filename dictionaries and write flags
            model.fnames = {}
            model.fnames['master'] = fname[:-4]+'_master.ops'
            model.fnames['materials']  = fname[:-4]+'_materials.ops'
            model.fnames['geometry'] = fname[:-4]+'_geometry.ops'
            model.fnames['assigns'] = fname[:-4]+'_assigns.ops'
            model.fnames['patterns'] = fname[:-4]+'_patterns.ops'
            model.fnames['recorders'] = fname[:-4]+'_recorders.ops'
            model.fnames['analysis'] = fname[:-4]+'_analysis.ops'
            model.fnames['variables'] = fname[:-4]+'_variables.ops'
            
            #Write to files
            model.flags = {}
            model.flags['geometry'] = 1
            model.flags['master'] = 1
            model.flags['materials'] = 0
            model.flags['assigns'] = 0
            model.flags['patterns'] = 0
            model.flags['recorders'] = 0
            model.flags['analysis'] = 0
            model.flags['elements'] = 0
            model.flags['variables'] = 0
        
            model.observers = []
            model.setDefaultOptions()
        return model
        pass
    
    
    @staticmethod
    def loadDatabase(fname):
        fid = open(fname,mode = 'rb')
        databaseRead = pickle.Unpickler(fid)
        model = databaseRead.load()
        fid.close()
        return model
    
    #
    #Database Processing Methods
    #
    def genGroupNumber(self,number):
        return 'GRP{0:03.0f}'.format(double(number))
        
    def formElemTypes(self):
        self.elemTypes = {}
        for elem in self.elemDict:
            if self.elemTypes.has_key(elem.eltype):
                self.elemTypes[elem.eltype] .Nelem += 1
                self.elemTypes[elem.eltype] .elemList.append(elem.elnum)
            else:
                self.elemTypes[elem.eltype] = Stru()
                self.elemTypes[elem.eltype].Nelem = 1
                self.elemTypes[elem.eltype] .elemList = [elem.elnum]
                pass
            pass

    
    #
    #Command (assigns) manipulation Methods
    #
    def addCommand(self,name,cmdObject):
        ncmds = len(self.cmdList)
        self.assigns[name] = cmdObject
        self.cmdList.append(name)
        
        if cmdObject.instruction.find('element') == 0:
            self.flags['elements'] = 1
            print 'Element creation command added: '+cmdObject.instruction
        else:
            self.flags['assigns'] = 1
        pass
        
    def deleteCommand(self,name):
        self.assigns.pop(name)
        self.cmdList.remove(name)
        
        if len(self.cmdList) == 0:
            self.flags['element'] = 0
            self.flags['assigns'] = 0
        self.shoutModelChange()
        pass
        
    def promoteCmd(self, cmdName):
        cmdList = self.cmdList
        idx = cmdList.index(cmdName)
        if idx > 0:
            aux = cmdList[idx-1]
            cmdList[idx - 1] = cmdName
            cmdList[idx] = aux
            self.cmdList = cmdList
        self.shoutModelChange()
        pass
        
    def demoteCmd(self, cmdName):
        cmdList = self.cmdList
        idx = cmdList.index(cmdName)
        if idx < len(cmdList)-1:
            aux = cmdList[idx+1]
            cmdList[idx + 1] = cmdName
            cmdList[idx] = aux
            self.cmdList = cmdList
        self.shoutModelChange()
        pass

    #
    #Materials
    #
    def addMaterial(self,id,material):
        self.materials[id] = material
        if len(self.materials) == 0:
            pass
        else:
            self.flags['materials'] = 1
        self.shoutModelChange()
        pass
        
    def deleteMaterial(self,id):
        self.materials.pop(id)
        self.shoutModelChange()
        pass
        
    #
    #Output Methods
    #
    def saveDatabase(self,fname):
        
        #Erase subscribers
        allObs = self.observers
        self.observers = []
        
        fid = open(fname,mode = 'wb')
        databaseWrite = pickle.Pickler(fid, protocol=2)
        databaseWrite.dump(self)
        fid.close()
        
        self.observers = allObs
        
    def writeGeometry(self,fid = []):
        
        if len(fid) == 0:
            fid = open(self.fnames['geometry'],'w')
        else:
            pass
        
        #Header
        fid.write('#File auto-generated with gmsh2opensees from:'+self.sourceFile+'\n')
        fid.write('#\n')
        
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        
        #Writeout nodes
        fid.write('#Nodes\n')
        i = 0
        while i < self.XYZ.shape[0]:
            fid.write('node {0} {1:17.13} {2:17.13} \n'.format(i+1, self.XYZ[i,0], self.XYZ[i,1]))
            i += 1
        
        #Elements must now be written with assignment commands
        fid.write('#\n')
        
        if self.flags['elements'] == 1:
            fid.write('#Elements\n')
            for cmd in self.assigns.keys():
                cmdObject = self.assigns[cmd]
                if cmdObject.isElementAssign == True:
                    cmdObject.writeCommand(fid,self.elemDict)
                    fid.write('#\n')
            fid.write('#\n')
        else:
            fid.write('\n\n')
            fid.write('Use the \'element\' command to assign elements.')
            fid.write('\n\n')
        
        
                
        #Create physical groups in OpenSEES file
        fid.write('#\n')
        fid.write('#Physical groups from GMSH\n')
        
        
        fid.write('\n#Element groups----------------\n')
        
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('set elem'+grupNum+' [list')
            for el in self.elemPG[i]:
                fid.write(' {0}'.format(el))
            fid.write(']\n')
        
        fid.write('\n#Node groups   ----------------\n')
        
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('set node'+grupNum+' [list')
            for nd in self.nodePG[i]:
                fid.write(' {0}'.format(nd))
            fid.write(']\n')
        
        #Output group name reference table
        fid.write('\n')
        fid.write('puts \"Loaded {0} nodal coordinates. \"\n'.format(self.Nnodes))
        fid.write('puts \"Nodal Groups Element Groups \"\n')
        fid.write('puts \"------------ -------------- \"\n')
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('puts \"node'+grupNum+'    elem'+grupNum+' \"\n')
        fid.close()
        
    def writeMaterials(self, fid=[]):
        if len(fid) == 0:
            fid = open(self.fnames['materials'],'w')
        else:
            pass
        
        fid.write('#File auto-generated with gmsh2opensees from:'+self.sourceFile+'\n')
        fid.write('#\n')
        
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        
        #Writeout nodes
        fid.write('#Materials\n')
        
        for id in self.materials:
            mat = self.materials[id]
            fid.write(mat[0]+' '+mat[1]+' '+str(id)+' '+mat[2]+'\n')
        fid.close()
        pass
        
    def writeAssigns(self, fid = []):
        if len(fid) == 0:
            fid = open(self.fnames['assigns'],'w')
        else:
            pass
        
        fid.write('#File auto-generated with gmsh2opensees from:'+self.sourceFile+'\n')
        fid.write('#\n')
        
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        
        for key in self.assigns.keys():
            cmd = self.assigns[key]
            if cmd.isElementAssign:
                pass
            else:
                cmd.writeCommand(fid,model=self)
            
        fid.close()
        pass
        
    def writePatterns(self,outfname):
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        pass
        
    def writeRecorders(self,outfname):
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        pass
        
    def writeAnalysis(self, fid  = []):
        if len(fid) == 0:
            fid = open(self.fnames['analysis'],'w')
        else:
            pass
        for option in self.analysisOptions['commandOrder']:
            writeThis = option+' '+self.analysisOptions[option].type+' '+self.analysisOptions[option].parameters+'\n'
            print writeThis
            fid.write(writeThis)
        fid.close()
        pass
        
    def writeMaster(self):
        if self.flags['variables'] == 1:
            fid.write('\n \n source '+self.fnames['variables']+' \n\n')
        
        fid = open(self.fnames['master'],'wt')
        for key in self.fnames.keys():
            if self.flags[key] == 1:
                fid.write('source '+self.fnames[key]+'\n')
            
        fid.close()
        pass
        
    #Observers must implement the .catchModelChange() method so that they can update information
    # based on changes in this model. This will be called each time a change needs to 
    # be reported by calling the self.shoutModelChange() method.
    def subscribe(self, observer):
        self.observers.append(observer)
        pass
        
    def clearsubscribers(self):
        self.observers = []
        pass
        
    def shoutModelChange(self):
        for obs in self.observers:
            obs.catchModelChange()
        pass
    
    def setAnalysisOption(self,option,optiontype,params='',shout=1):
        self.analysisOptions[option].type = optiontype
        self.analysisOptions[option].parameters = params
        if shout == 1:
            self.shoutModelChange()
        
        print option.upper()+' set to: '+optiontype+' '+params
        pass
    
    def setDefaultOptions(self,option='all'):
        #  Analysis Options

        if len(self.analysisOptions) == 0:
            self.analysisOptions['constraints'] = Stru()
            self.analysisOptions['numberer'] = Stru()
            self.analysisOptions['system'] = Stru()
            self.analysisOptions['test'] = Stru()
            self.analysisOptions['algorithm'] = Stru()
            self.analysisOptions['analysis'] = Stru()
            self.analysisOptions['integrator'] = Stru()
            self.analysisOptions['commandOrder'] = ['constraints','numberer','system','test','algorithm','analysis','integrator']

        if option == 'constraints' or option == 'all':
            self.analysisOptions['constraints'].type = 'Plain'
            self.analysisOptions['constraints'].parameters = ''        
        
        if option == 'numberer' or option == 'all':
            self.analysisOptions['numberer'].type = 'RCM'
            self.analysisOptions['numberer'].parameters = ''

        if option == 'system' or option == 'all':        
            self.analysisOptions['system'].type = 'ProfileSPD'
            self.analysisOptions['system'].parameters = ''

        if option == 'test' or option == 'all':
            self.analysisOptions['test'].type = 'NormDispIncr'
            self.analysisOptions['test'].parameters = '1e-6 100 1'
        
        if option == 'algorithm' or option == 'all':
            self.analysisOptions['algorithm'].type = 'Newton'
            self.analysisOptions['algorithm'].parameters = ''
        
        if option == 'analysis' or option == 'all':
            self.analysisOptions['analysis'].type = 'Static'        
            self.analysisOptions['analysis'].parameters = ''
        
        if option == 'integrator' or option == 'all':
            self.analysisOptions['integrator'].type = 'LoadControl'
            self.analysisOptions['integrator'].parameters = '1'
      
        self.flags['analysis'] = 1
        pass
        
    

# ===============================
# OpenSEES command class (used in assigns)
# ===============================
class OpenSEESassign:
    
    #Defines an OpenSees command object class. This class generates aids in writing the TCL
    # to assign properties to elements in groups. 
    # Example element assignment command: Use element quad $ele $n01 $n02 $n03 $n04 1.0 'PlaneStrain' 1
    def __init__(self, instruction, objectList, applyTo='nodes', applyToElemType = 'All'):
        
        #Private attributes
        self.__nodeFormat__ = '$n{0:02.0f}'
        
        self.instruction = instruction
        self.applyTo = applyTo.lower()
        self.objectList = objectList
        self.applyToElemType= applyToElemType
        self.autoCodeString = '-- Code generated automagically by gmsh2opensees -- \n\n'
        self.reservedList = ['$ele', '$nod']
        for i in range(0,100):
            self.reservedList.append(self.__nodeFormat__ .format(float(i)))
        
        if instruction.find('element') == 0:
            self.isElementAssign = True
        else:
            self.isElementAssign = False
        
        print 'Added new OpenSEESassing \n'
        print 'instruction: ' + instruction + '\n'
        print 'applyTo:     ' + applyTo + '\n'
        print 'objectList:  ' + objectList + '\n'
        print 'elemTypes:   ' + applyToElemType + '\n\n'

        
    def __call__(self):
        return self.genCmdString()
        
    def genCmdString(self, variables={}):
        if self.applyTo == 'nodes':
            cmd = self.getNodeTCLCommand()
            pass
        elif self.applyTo == 'elements':
            cmd = self.getElemTCLCommand()
            pass
        else:
            cmd = []
            pass
            
        #Do the following replacement (if variables are used)
        for var in variables.keys():
            cmd.replace(var,variables[var])
        return cmd
    
    def getNodeTCLCommand(self,model):
        cmd = ''
        if self.instruction.find('$ele') > 0:
            print 'gmsh2opensees.py: OpenSEESassign.getNodeTCLCommand(): \'$ele\' string found in node command'
            print self.instruction
            pass
        else:
            cmd = self.autoCodeString
            cmd += 'foreach nod [list '
            for nod in self.getObjectIds(model):
                cmd += '{0} '.format(nod)
            cmd += '] { \n'
            cmd += self.instruction+'\n'
            cmd += '} \n \n'
            print cmd
            pass
        return cmd
        
    def getElemTCLCommand(self,model):
        cmd = ''
        if self.instruction.find('$nod') > 0:
            print 'gmsh2opensees.py: OpenSEESassign.getElemTCLCommand(): \'$nod\' string found in element command'
            pass
        else:
            cmd = self.autoCodeString
            cmd += 'foreach ele [list '
            for ele in self.getObjectIds(model):
                cmd += '{0} '.format(ele)
            cmd += '] { \n'
            cmd += self.instruction+'\n'
            cmd += '} \n \n'
            print cmd
            pass
        return cmd
        pass 
        
    def getObjectIds(self, model):
        print self.objectList
        spList = self.objectList.split('+')
        
        #Initialize list that will contain the object (element or nodes) ids
        objIds = []
                
        #Run though object list
        for obj in spList:
            type = obj[:3]
            idnum = obj[3:]
            idx = model.physgrp.index(int(idnum))
            if self.applyTo == 'elements':
                #Element Groups
                if type == 'egr':
                    elemIds = model.elemPG[idx]
                    objIds = objIds+elemIds
                
                #Just 1 element
                if type == 'ele':
                    objIds = objIds + [int(idnum)]
                
                #All elements
                if type == 'allelements':
                        objIds = objIds + range(1,model.Nelem)
                pass  #apply to elements group
            
            if self.applyTo == 'nodes':
                #Node Groups
                if type == 'ngr':
                    nodeIds = model.nodePG[idx]
                    objIds = objIds+nodeIds
                    
                #Just 1 node
                if  type == 'nod':
                    objIds = objIds + [idnum]
                    
                #All nodes
                if obj == 'allnodes':
                    objIds = objIds + range(1,model.Nnodes)
                pass  # apply to nodes loop
            
            pass #obj for loop
            
            #Now if appyTo elements, then check whether specific element type is specified
            if self.applyTo == 'elements':
                if self.applyToElemTypes == 'all':
                    pass
                else:
                    totype = int(self.applyToElemTypes[5:8])
                    removeList = []
                    i = 0
                    for elem in objIds:
                        if model.elemDict[elem].eltype == totype:
                            pass
                        else:
                            removeList.append(i)
                        i += 1
                    for idx in removeList:
                        objIds.pop(idx)
        if len(objIds) == 0:
            objIds = -1
            print "libgmsh2opensees.py: OpenSEESassign.writeAssign(): Warning: Command applied to empty group."
        return objIds
        
    def writeCommand(self, fid, elemDict = [], variables = {}, model=[]):
        if self.applyTo == 'nodes':
            fid.write(self.getNodeTCLCommand(model))#+'\n\n')
            pass
        
        if self.applyTo == 'elements':
            if self.instruction.find('element') > -1:
                if len(elemDict) == 0:
                    pass
                else:
                    for elem in elemDict:
                        if str(self.applyToElemType) == str(elem.eltype):
                            cmd = self.instruction
                            i = 1
                            for nod in elem.nodes:
                                cmd = cmd.replace(self.__nodeFormat__ .format(float(i)), str(nod))
                                i += 1
                            cmd = cmd.replace('$ele',str(elem.elnum))
                            print 'Added element CMD: '+cmd
                            fid.write(cmd+'\n')
                pass
            else:
                fid.write(self.getElemTclCommand(model)+'\n\n')
                pass
            pass
        pass
# ===============================
# OpenSEES recorder command class 
# ===============================
class OpenSEESrecorder:
    def __init__(self):
        pass
# -----------------------------------------------------------------------------
# Auxilliary Classes
# -----------------------------------------------------------------------------
#Element structure class
class Elem:
    pass

#General 'structure' like class
class Stru:
    pass


