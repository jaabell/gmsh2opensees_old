# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 18:48:53 2010

@author: 15636763k
"""
# Script para transformar geometría GMSH con zonificacion a un archivo OpenSEES
#
# ------------------------------------------------------------------------------
# (C) 2010 Jose Abell 
# Facultad de Ingenieria y Ciencias Aplicadas
# Universidad de los Andes
# jaabell@miuandes.cl

#Importar modulos
from scipy import *
#import matplotlib.pyplot as plt
from libtools import *
import pickle

#from Tkinter import *
#from tkFileDialog import askopenfilename
#from tkFileDialog import asksaveasfilename

#ventana = Tk()


#Seleccionar archivos de origen y destino
#fname = askopenfilename(title="gmsh2OpenSEES:  Seleccionar malla de origen", initialdir=".", filetypes=[("GMSH mesh","*.msh")])
#outfname = asksaveasfilename(parent=ventana,title="gmsh2OpenSEES: Seleccionar el archivo de destino", filetypes=[("OpenSEES TCL Script","*.ops")], initialfile=fname[:-4]+'.ops')
#fname = 'amplitopo3.msh'
#outfname = fname[:-4]+'.ops'

# ------------------------------------------------------------------------------
# Estructura basica
# ------------------------------------------------------------------------------
class Elem:
    pass

class Stru:
    pass

class Model:
    @staticmethod
    def loadFromGmshFile(fname):
        # ------------------------------------------------------------------------------
        # Lectura de Archivo de Origen
        # ------------------------------------------------------------------------------
        # physgrp: Grupo fisico del elemento segun el archivo .msh
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
            
            #Detectar campoevent
            if line[0] == '$':
                if line.find('Nodes') > 0:
                    inNodes = 1
                if line.find('EndNodes')  > 0:
                    inNodes = 0
                if line.find('Elements')  > 0:
                    inElements = 1
                if line.find('EndElements')  > 0:
                    inElements = 0
                print line#+'{0} {1}'.format(inNodes,inElements)
            
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
        
        if model.success:
            model.formElemTypes()
            model.assigns = {}
            model.recorders = []
            model.analysisOptions = []
            model.materials = []
        
        return model
        
    def writeModelToOpsFile(self,outfname):
        
        fid = open(outfname,'w')
        
        #Encabezado
        fid.write('#Archivo generado automaticamente por gmsh2opensees a partir de:'+self.sourceFile+'\n')
        fid.write('#\n')
        
        #Escribir nodos
        fid.write('#Nodos\n')
        i = 0
        while i < self.XYZ.shape[0]:
            fid.write('node {0} {1:17.13} {2:17.13} \n'.format(i+1, self.XYZ[i,0], self.XYZ[i,1]))
            i += 1
        
        #Escribir elementos
        fid.write('#\n')
        fid.write('#Elementos\n')
        
        thick = 1.
        material = 1
        
        for elem in self.elemDict:
            if elem.eltype == 3:
                nodes = elem.nodes
                fid.write('element quad {0} {1} {2} {3} {4} {5:12.7} {6} {7}\n'.format(elem.elnum, nodes[0], nodes[1], nodes[2], nodes[3], thick, 'PlaneStrain', material))
        
        #Crear grupos fisicos
        fid.write('#\n')
        fid.write('#Grupos Fisicos\n')
        
        
        fid.write('\n#Elementos----------------\n')
        
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('set elem'+grupNum+' [list')
            for el in self.elemPG[i]:
                fid.write(' {0}'.format(el))
            fid.write(']\n')
        
        fid.write('\n#Nodos----------------\n')
        
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('set node'+grupNum+' [list')
            for nd in self.nodePG[i]:
                fid.write(' {0}'.format(nd))
            fid.write(']\n')
        
        fid.write('\n')
        fid.write('puts \"Loaded {0} nodal coordinates. \"\n'.format(self.Nnodes))
        fid.write('puts \"Loaded {0} elements. \" \n\n'.format(self.Nelem))
        fid.write('puts \"Nodal Groups Element Groups \"\n')
        fid.write('puts \"------------ -------------- \"\n')
        for i in range(len(self.physgrp)):
            grupNum = self.genGroupNumber(self.physgrp[i])
            fid.write('puts \"node'+grupNum+'    elem'+grupNum+' \"\n')
        fid.close()
        
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
    
    def saveDatabase(self,fname):
        fid = open(fname,mode = 'wb')
        databaseWrite = pickle.Pickler(fid)
        databaseWrite.dump(self)
        fid.close()
    
    @staticmethod
    def loadDatabase(fname):
        fid = open(fname,mode = 'rb')
        databaseRead = pickle.Unpickler(fid)
        model = databaseRead.load()
        fid.close()
        
        return model



class OpenSEESassign:
    #Defines an OpenSees command object class. This class generates aids in writing the TCL
    # to assign properties to elements in groups. 
    def __init__(self, instruction, objectList, applyTo='nodes'):
        self.instruction = instruction
        self.applyTo = applyTo.lower()
        self.objectList = objectList
        self.autoCodeString = '-- Code generated automagically by gmsh2opensees -- \n\n'
        
        print 'Added new OpenSEESassing \n'
        print 'instruction: ' + instruction + '\n'
        print 'applyTo:     ' + applyTo + '\n'
        print 'objectList:  ' + objectList + '\n\n'
        
    def __call__(self):
        return self.genCmdString()
        
    def genCmdString(self):
        if self.applyTo == 'nodes':
            return self.getNodeTCLCommand()
            pass
        elif self.applyTo == 'elements':
            return self.getElemTCLCommand()
            pass
        else:
            pass
    
    def getNodeTCLCommand(self,model):
        if self.instruction.find('$ele') == -1:
            pass
        else:
            str = self.autoCodeString
            str += 'for nod [list '
            for nod in getObjectIds(model):
                str += '{0} '.format(nod)
            str += '] { \n'
            str += self.instruction+'\n'
            str += '} \n \n'
            pass
        
    def getElemTCLCommand(self):
        if self.instruction.find('$nod') == -1:
            pass
        else:
            str = self.autoCodeString
            str += 'for ele [list '
            for ele in getObjectIds(model):
                str += '{0} '.format(ele)
            str += '] { \n'
            str += self.instruction+'\n'
            str += '} \n \n'
            pass
        pass 
        
    def getObjectIds(self, model):
        spList = self.objectList.splic(sep = '+')
        objIds = []
        for obj in spList:
            type = obj[:3]
            idnum = obj[3:]
            if type == 'grp':
                if self.applyTo == 'elements':
                    elemIds = model.elemPG[int(idnum)]
                    objIds = objIds+elemIds
                elif self.applyTo == 'nodes':
                    nodeIds = model.nodePG[int(idnum)]
                    objIds = objIds+nodeIds
            elif  type == 'nod':
                pass
            elif type == 'ele':
                pass
            pass
            return objIds
            
    def promoteCmd(self, cmdName):
        newAssigns = {}
        cmdList = self.assigns.keys()
        idx = cmdList.index(cmdName)
        if idx > 0:
            aux = cmdList[idx-1]
            cmdList[idx - 1] = cmdName
            cmdList[idx] = aux
            for cmd in cmdList:
                newAssigns[cmd] = model.assigns[cmd]
            model.assigns = newAssigns
        pass
        
    def demoteCmd(self, cmdName):
        newAssigns = {}
        cmdList = self.assigns.keys()
        idx = cmdList.index(cmdName)
        if idx < len(cmdList)-1:
            aux = cmdList[idx+1]
            cmdList[idx + 1] = cmdName
            cmdList[idx] = aux
            for cmd in cmdList:
                newAssigns[cmd] = model.assigns[cmd]
            model.assigns = newAssigns
        pass
        
    def loadDatabase(self,fname):
        pass
        