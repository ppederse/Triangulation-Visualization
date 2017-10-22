#This file contains the code for the Delaunay Triangulation algorithm

import math
from generalFunctions import *
from triangleSplitting import *

def isConvexQuad(pts):
    """This function takes in a list of four two dimensional points stored as 
    tuples and returns True if they make up a convex polygon, and False 
    otherwise."""
    for i in range(0, 4):
        if(crossProduct(pts[i], pts[(i+1)%4], pts[(i+2)%4]) <= 0):
            return(False)
    return(True)

def getPts(edge, tri1, tri2):
    """This function takes in two triangles that share an edge and returns a list of
    the four points in counter-clockwise order."""
    pts = []
    bottomLeft = edge[0]
    topRight = edge[1]

    #Figure out which edge is further left and if on a vertical line which is lower
    if(bottomLeft[0] > topRight[0]):
        bottomLeft = edge[1]
        topRight = edge[0]
    elif(bottomLeft[0] == topRight[0]):
        if(bottomLeft[1] > topRight[1]):
            bottomLeft = edge[1]
            topRight = edge[0]
    pts.append(bottomLeft)

    #Find the points not on the edge
    for i in range(0, 3):
        if(not tri1[i] in edge):
            ptNotOnEdge1 = tri1[i]
        if(not tri2[i] in edge):
            ptNotOnEdge2 = tri2[i]

    #If left turn start with that triangle in answer else start with other
    if(crossProduct(bottomLeft, ptNotOnEdge1, topRight) > 0):
        pts.extend([ptNotOnEdge1, topRight, ptNotOnEdge2])
        # pts.append(topRight)
        # pts.append(ptNotOnEdge2)
    else:
        pts.extend([ptNotOnEdge2, topRight, ptNotOnEdge1])
        # pts.append(topRight)
        # pts.append(ptNotOnEdge1)

    return(pts)

def removeRepeatTris(l):
    uniqueTs = []
    for t in l:
        if not t in uniqueTs:
            uniqueTs.append(t)
    return uniqueTs

def getLength(pt1, pt2):
    """This function calculates the euclidean distance between two points"""
    return(math.sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2))

def getAngles(tri):
    """This function takes in three points and returns the interior angles of the
    triangle they make up."""
    angles = []
    #lengths is ordered specially to make oppLongest the right value
    lengths = [getLength(tri[1], tri[2]), getLength(tri[2], tri[0]), getLength(tri[0], tri[1])]
    lengths = sorted(lengths)
    a = lengths[0]
    b = lengths[1]
    c = lengths[2]
    
    #Use the cosine rule to find the largest angle
    cos1 = (a**2 + b**2 - c**2) / (2*b*a)
    angle1 = math.acos(cos1)
    angles.append(angle1)

    #Use the sin rule to find the next angle
    sin2 = a*(math.sin(angle1)/c)
    angle2 = math.asin(sin2)
    angles.append(angle2)

    angles.append(math.pi - angle1 - angle2)
    return(angles)

def isLegal(edge, tri1, tri2):
    """This function takes in an edge and the two triangles that contain it."""
    pts = getPts(edge, tri1, tri2)
    angles1 = sorted(getAngles(tri1) + getAngles(tri2))

    #Find angles for the new triangles
    newTri1 = [pts[0], pts[1], pts[3]]
    newTri2 = [pts[1], pts[2], pts[3]]
    angles2 = sorted(getAngles(newTri1) + getAngles(newTri2))

    #If the new triangles are fatter, return True!
    if(angles2 > angles1):
        return(False)
    return(True)

def updateDict(d, t1, t2):
    etris = d.values()
    edges = d.keys()
    edgeDict = {}
    for e in edges:
        edgeDict[e] = []
        for ets in etris:
            for t in ets:
                if(t != t1 and t != t2):
                    if isIncident(e, t) and not t in edgeDict[e]:
                        edgeDict[e].append(t)

    return(edgeDict)

def initialTriangulate(dataSet):
    """Returns dictionary that holds the edges of a triangulation of the dataset
    as the keys and the incident triangles as the values."""
    edgeDict = triangleSplittingDict(dataSet)
    edges = edgeDict.keys()
    tris = removeRepeatTris(edgeDict.values())
    #Build the dictionary
    edgeDict = {}
    for e in edges:
        edgeDict[e] = []
        for t in tris:
            if isIncident(e, t):
                edgeDict[e].append(t)
    return(edgeDict)

def delaunayTriangulation(dataSet):
    """This function takes in a dataset and returns a list of the edges
    of the delaunay triangulation. """
    edgeDict = triangleSplittingDict(dataSet)
    edges = edgeDict.keys()
    flag = True
    while(flag):
        flag = False
        removableEdges = []
        innerFlag = True
        i = 0
        while innerFlag:
            e = edges[i]
            if i == len(edges) - 1:
                innerFlag = False
            i = i + 1
            if len(edgeDict[e]) == 2 and e[0] != e[1]:#Hacky Fix, need to debug initialTriangulate
                pts = getPts(e, edgeDict[e][0],edgeDict[e][1])
                if isConvexQuad(pts):
                    oldTri1 = edgeDict[e][0]
                    oldTri2 = edgeDict[e][1]
                    if not isLegal(e, oldTri1, oldTri2):
                        innerFlag = False
                        flag = True
                        newTris = [(pts[0], pts[1], pts[3]), (pts[1], pts[2], pts[3])]
                        newE = (pts[1], pts[3])
                        edgeDict[newE] = newTris
                        del edgeDict[e]
                        edges = edgeDict.keys()
                        edgeDict = updateDict(edgeDict, oldTri1, oldTri2)
                        i = 0

    return edgeDict.keys()   