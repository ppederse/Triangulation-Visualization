#This file contains the code for the triangle splitting algorithm. 

from generalFunctions import *

def inTri(pt, tri):
    """This function takes in a data point with x and y values and a list of 
    three tuples, representing the vertices of a triangle (sorted counter clockwise). 
    If the point is in interior of the triangle, return True. Else, 
    return False. This does function does not handle degeneracies. """
    cross1 = crossProduct(tri[0], tri[1], pt)
    cross2 = crossProduct(tri[1], tri[2], pt)
    cross3 = crossProduct(tri[2], tri[0], pt)
    if (cross1 > 0 and cross2 > 0 and cross3 > 0):
        return(True)
    return(False)

def edgesOfHull(pts):
    """This function takes in a list of vertices and returns a list
    of the edges that connect them."""
    convHEdges = []
    numPts = len(pts)
    for i in range(0, numPts):
        convHEdges.append((pts[i], pts[(i+1)%numPts]))
    return(convHEdges)

def naiveConvexHull(H):
    """This function takes in a list of tuples (assumed to be in general 
    position) and returns a list of the points that make up the 
    counter-clockwise convex hull. The list starts with the left-most
    point. """
    #Arbitrary cases of zero, one, or two points
    if len(H) <= 2:
        return(H)
    
    convH = []
    currPt = H[1]
    #find the leftmost point
    for pt in H:
        if pt[0] < currPt[0]:#MAX MIN LOOK HERE
            currPt = pt
    convH.append(currPt)
    #True as long as all points to the right    
    flag = True
    while(flag):
        flag2 = True
        i = 0
        #flag2 ends the loop when the valid edge is found. 
        while(i < len(H) and flag2):
            if(H[i] != currPt):
                if(isEdge(currPt, H[i], H)):
                    #End if we've found the starting point (completed hull)
                    if(H[i] in convH):
                        flag = False
                    else:
                        convH.append(H[i])
                        flag2 = False
            i = i + 1
        currPt = convH[-1]
    return(convH)

def triangleSplittingDict(dataSet):
    """Returns dictionary that holds the edges of a triangulation of the dataset
    as the keys and the incident triangles as the values."""
    convH = naiveConvexHull(dataSet)
    #Note that convH stores the first and last point twice
    if(len(dataSet) < 3):
        return(convH)
    elif(len(dataSet) == 3):
        return(convH.append(convH[0]))
    #A list of the internal edges
    edges = edgesOfHull(convH)

    #The internal vertices
    k = []
    #stores a list of three tuples that hold the vertices of the triangles
    tris = []
    #Adds in edges between the anchor vertex and non-adj hull points
    for i in range(2, len(convH) - 1):
        new = (convH[0], convH[i])
        edges.append(new)
        new = (convH[0], convH[i-1], convH[i])
        tris.append(new)
    #Put in the last triangle!
    new = (convH[0], convH[i], convH[i+1])
    tris.append(new)
    for d in dataSet:
        if d not in convH:
            k.append(d)

    for pt in k:
        flag = True
        t = 0
        while t < len(tris) and flag:
            if inTri(pt, tris[t]):
                #Create the edges new triangle edges, update tris
                #Put three new edges in edges
                for v in tris[t]:
                    new = (pt, v)
                    edges.append(new)
                #Put three new triangles in tris
                for i in range(0, 3):
                    new = (pt, tris[t][i], tris[t][(i+1)%3])
                    tris.append(new)
                tris.remove(tris[t])
                t = t - 1
                flag = False   
            t = t + 1
    #Build the dictionary
    edgeDict = {}
    for e in edges:
        edgeDict[e] = []
        for t in tris:
            if isIncident(e, t):
                edgeDict[e].append(t)
    return(edgeDict)

def triangleSplitting(dataSet):
    """Returns dictionary that holds the edges of a triangulation of the dataset
    as the keys and the incident triangles as the values."""
    d = triangleSplittingDict(dataSet)

    return(d.keys())