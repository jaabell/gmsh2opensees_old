from scipy import *
import matplotlib.pyplot as plt

def plotDomain(XYZ,elemDict):
    plt.figure()
    for elem in elemDict:
        plt.plot(XYZ[elem.nodes - 1,0],XYZ[elem.nodes - 1,1])
    plt.xlabel('X')
    plt.ylabel('Y')