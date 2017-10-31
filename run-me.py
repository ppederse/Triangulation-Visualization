#Run this file when you want to activate the visualization. All the GUI code is contained within
#this file. 
#
#Made by Scott Pedersen
#October 2017

from Tkinter import *
from triangleSplitting import *
from generalFunctions import *
from iterativeTriangulation import *
from delaunayTriangulation import *

class DataTriangulationVis(Frame):
    def __init__(self,master):
        global method
        global MethodLabel

        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.canvas = Canvas(self,  cursor="cross",width=650,height=650)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)

        SplittingButton = Button ( self, command = self.splittingCall, text = "Triangle Splitting")

        IterativeButton = Button ( self, command = self.iterativeCall, text = "Iterative Triangulation")

        DelaunayButton = Button ( self, command = self.delaunayCall, text = "Delaunay Triangulation")

        ClearButton = Button ( self, command = self.clear, text = "Clear Data Points")

        RandomPointsButton = Button( self, command = self.randomCall, text = "Generate 50 random points")

        SplittingButton.place(x=17, y=25)
        IterativeButton.place(x=17,y=50)
        ClearButton.place(x = 17, y = 125)
        DelaunayButton.place(x = 17, y = 75)
        RandomPointsButton.place(x=17,y=100)

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
                if(method == "Triangle Splitting"):
                    tri = triangleSplitting(dataSet) 
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

    def splittingCall(self):
        global method 
        method = "Triangle Splitting"
        self.updatePic()

    def iterativeCall(self):
        global method
        method = "Iterative Triangulation"
        self.updatePic()

    def randomCall(self):
        global dataSet
        global point_ids
        self.clear()
        dataSet = buildH(50)
        for i in dataSet:
            pt_id = self.canvas.create_oval(i[0]-2,i[1]-2, i[0]+2,i[1]+2,fill='red')
            point_ids.append(pt_id)
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