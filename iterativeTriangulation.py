#This file contains the code for the iterative triangulation algorithm

from generalFunctions import *

def visVerts(pt, hull):
    """This function returns a list with the elements being -1 or 1. Each element
    corresponds to a vertex from the parent list hull, at the same index. If
    the value is -1, the point is considered visible. """
    #
    sgnList = [0] * len(hull)
    for i in range(0, len(hull)):
        #Modular arithmetic is to make the index wrap back to the zeroth entry at end
        if(crossProduct(hull[i], hull[(i+1)%len(hull)], pt) >= 0):
            sgnList[i] = 1
        else:
            sgnList[i] = -1
        #When it goes to negative, starts being visible
    return(sgnList)

def negBounds(l):
    """This function returns the indices at which a list containing a 
    sublist of -1's begins and ends."""
    ans = []
    i=0
    while(len(ans) == 0):
        if(l[i] == -1):
            ans.append(i)
        i = i+1
    #The i< len(l) is to prevent overflow for the case where the list ends in a string of negatives. 
    while(len(ans) == 1 and i < len(l)):
        if(l[i] == 1):
            ans.append(i-1)
        i = i + 1
    #For the case where list ends with multiple negatives in a row
    if(len(ans) == 1):
        ans.append(i - 1)
    return(ans)  

def iterativeTriangulate(H):
    """This function triangulates a data set using the iterative method. Edges stored 
    and returned as a list of lists of two data points, representing the vertices of an edge
    that needs to be drawn."""
    H = sorted(H, key = getKey)
    convH = sortTriCCW(H[0:3])
    edges = [[convH[0], convH[1]], [convH[1], convH[2]], [convH[2], convH[0]]]
    for i in range(3, len(H)):
        visibles = visVerts(H[i], convH)
        visibleBounds = negBounds(visibles)
        numVis = visibleBounds[1] - visibleBounds[0]
        edges.append(([H[i], convH[visibleBounds[0]]]))
        edges.append(([H[i], convH[(visibleBounds[1]+1)%len(convH)]]))
        for j in range(0, numVis):
            edges.append([H[i], convH[visibleBounds[1] - j]])
            del convH[visibleBounds[1] - j]
        convH.insert(visibleBounds[0] + 1, H[i])
    convH.append(convH[0])
    return(edges)