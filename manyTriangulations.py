#Scott Pedersen
#Visualization of Triangulation Algorthms

from Tkinter import *
import math

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
    else:
        #Put it in the other order
        return([tri[0], tri[2], tri[1]])
        # returnable = [tri[0]]
        # returnable.append(tri[2])
        # returnable.append(tri[1])

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
    
def naiveTriangulate(dataSet):
    """Returns a list of vetices stored as tuples that make up the edges of 
    the triangulation of a data set."""
    convH = naiveConvexHull(dataSet)
    #Note that convH stores the first and last point twice
    convH.append(convH[0])    
    if(len(dataSet) < 3):
        return(convH)
    elif(len(dataSet) == 3):
        return(convH.append(convH[0]))
    #A list of the internal edges
    edges = []
    #Put in the hull edges
    edges.append(convH)
    #The internal vertices
    k = []
    #stores a list of three tuples that hold the vertices of the triangles
    tris = []
    #Adds in edges between the anchor vertex and non-adj hull points  
    for i in range(2, len(convH) - 1):
        #if convH[i] != convH[0] and v!= convH[1] and v != convH[-2]:
            new = []
            new.append(convH[0])
            new.append(convH[i])
            edges.append(new)
            new = []
            new.append(convH[0])
            new.append(convH[i-1])
            new.append(convH[i])
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
                    new = []
                    new.append(pt)
                    new.append(v)
                    edges.append(new)
                #Put three new triangles in tris
                for i in range(0, 3):
                    new = []
                    new.append(pt)
                    new.append(tris[t][i])
                    #If index is 3, go back to first point in tri
                    new.append(tris[t][(i+1)%3])
                    tris.append(new)
                tris.remove(tris[t])
                t = t - 1
                flag = False   
            t = t + 1
        
    return(edges)

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

def delaunayTriangulation(dataSet):
    """This function takes in a dataset and returns a list of the edges
    of the delaunay triangulation. """
    edgeDict = initialTriangulate(dataSet)
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

def isIncident(edge, tri):
    """This function returns True if a given triangle has edge as one of its 
    edges"""
    if edge[0] in tri and edge[1] in tri:
        return True
    else:
        return False

def edgesOfHull(pts):
    """This function takes in a list of vertices and returns a list
    of the edges that connect them."""
    convHEdges = []
    numPts = len(pts)
    for i in range(0, numPts):
        convHEdges.append((pts[i], pts[(i+1)%numPts]))
    return(convHEdges)

def initialTriangulate(dataSet):
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

###----------begin GUI code----------------

class DataTriangulationVis(Frame):
    def __init__(self,master):
        global method
        global MethodLabel

        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.canvas = Canvas(self,  cursor="cross",width=600,height=650)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)

        NaiveButton = Button ( self, command = self.naiveCall, text = "Naive Triangulation")

        IterativeButton = Button ( self, command = self.iterativeCall, text = "Iterative Triangulation")

        DelaunayButton = Button ( self, command = self.delaunayCall, text = "Delaunay Triangulation")

        ClearButton = Button ( self, command = self.clear, text = "Clear Data Points")

        NaiveButton.place(x=17, y=25)
        IterativeButton.place(x=17,y=50)
        ClearButton.place(x = 17, y = 100)
        DelaunayButton.place(x = 17, y = 75)

        MethodLabel = Label (self, text = "Current method: " + method)
        MethodLabel.place(x=17,y=6)

        self.master.title("Interactive Visualization for Data Triangulation")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        self.rect = None

        self.start_x = None
        self.start_y = None

    def updatePic(self):
            global method
            global line_ids
            global dataSet
            global MethodLabel

            if(line_ids != 1):
                for _id_ in line_ids:
                    self.canvas.delete(_id_)

            if(method != "None"):
                if(len(dataSet) == 3):
                    line_ids = [0] * 3
                    line_ids[0] = self.canvas.create_line(dataSet[0], dataSet[1])
                    line_ids[1] = self.canvas.create_line(dataSet[1], dataSet[2])
                    line_ids[2] = self.canvas.create_line(dataSet[2], dataSet[0])
                    
                if(len(dataSet) == 2):
                    line_ids = [0]
                    line_ids[0] = self.canvas.create_line(dataSet[0], dataSet[1])
            
            if(len(dataSet) > 3):
                if(method == "Naive Triangulation"):
                    tri = naiveTriangulate(dataSet) 
                if(method == "Iterative Triangulation"):
                    tri = iterativeTriangulate(dataSet)
                if(method == "Delaunay Triangulation"):
                    tri = delaunayTriangulation(dataSet)
                if(method != "None"):         
                    line_ids = [0] * len(tri)
                    for i in range(0, len(tri)):
                        line_ids[i] = self.canvas.create_line(tupleListToList(tri[i]))
            MethodLabel.configure(text = "Current method: " + method)

    def delaunayCall(self):
        global method
        method = "Delaunay Triangulation"
        self.updatePic()

    def naiveCall(self):
        global method 
        method = "Naive Triangulation"
        self.updatePic()

    def iterativeCall(self):
        global method
        method = "Iterative Triangulation"
        self.updatePic()

    def clear(self):
        global dataSet
        global line_ids
        global point_ids
        dataSet = []
        if(point_ids != []):
            for _id_ in point_ids:
                self.canvas.delete(_id_)
        point_ids = []
        if line_ids != []:
            for _id_ in line_ids:
                self.canvas.delete(_id_)
        line_ids = []



    def on_button_press(self,event):
        global dataSet
        global line_ids
        global poly_id
        global method
        global point_ids
        #print"({}, {})".format(event.x,event.y)
        
        if(not (event.x, event.y) in dataSet):
            if(line_ids != []):
                for _id_ in line_ids:
                    self.canvas.delete(_id_)
            pt_id = self.canvas.create_oval(event.x-2,event.y-2, event.x+2,event.y+2,fill='red')
            point_ids.append(pt_id)
            dataSet.append((event.x, event.y))
            self.updatePic()

#Initialize important objects
dataSet = []
line_ids = []
point_ids = []
method = "None" #While method is "None", won't triangulate

if __name__ == "__main__":
    root=Tk()
    app = DataTriangulationVis(root)
    app.pack()
    root.mainloop()

###----------end GUI code--------------