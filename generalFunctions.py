#This file contains the functions that are used by the different algorithms. 

import random

def tupleListToList(T):
    """This function takes in a list of tuples that represent edges and converts 
    them into a format that can be plotted in Tkinter. """
    if(len(T) == 0):
        return []
    ans = []
    for tup in T:
        ans.append(tup[0])
        ans.append(tup[1])
    return(ans)

def crossProduct(pnt1, pnt2, pnt3):
    """This equation takes in three tuples with x and y coordinates and returns 
    the cross product of the vectors pnt1pnt2 and pnt1pnt3."""
    x1 = pnt1[0] - pnt2[0]
    y1 = pnt1[1] - pnt2[1]
    x2 = pnt1[0] - pnt3[0]
    y2 = pnt1[1] - pnt3[1]
    return(x1*y2-y1*x2)

def getKey(item):
    """This function returns the first element of a list."""
    return(item[0])


def sortTriCCW(tri):
    """Takes in a list of three tuples representing data points with x and y
    values. Returns them sorted in CCW order, starting at the smallest x value. 
    The input TRI is sorted by increasing x value."""
    if(crossProduct(tri[0], tri[1], tri[2]) > 0):
        #Already sorted :)
        return(tri)
    #Put it in the other order
    return([tri[0], tri[2], tri[1]])

def isEdge(pt1, pt2, H):
    """This function takes in two points and a data set in which the two points
    are contained. If all the points lie to the left of a vector drawn from pt1
    to pt2, return True. Else, return false."""
    flag = True
    for otrPt in H:
        if otrPt != pt1 and otrPt != pt2:
            if(crossProduct(pt1, pt2, otrPt) < 0):
                flag = False
    return(flag) 

def isIncident(edge, tri):
    """This function returns True if a given triangle has edge as one of its 
    edges"""
    if edge[0] in tri and edge[1] in tri:
        return True
    return False

def buildH(n):
    """Generates a list of n random tuples with no repeating elements. """
    H = []
    for i in range(n):
        H.append((random.random()*500 + 125, random.random()*500 + 125))
    return(H)