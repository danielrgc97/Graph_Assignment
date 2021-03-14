#!/usr/bin/env python3
import numpy as np

class MyClass(object):
    def __init__(self):
        # Extracting values from the file
        lines = []
        f = open("./data_cases/case_04.in", "r")
        lines = f.readlines()
        self.first_line = [int(i) for i in lines[0].split(" ")]
        self.links = np.zeros([self.first_line[0],2])
        for i in range(1, self.first_line[0] + 1):
            nums_fila = [int(j) for j in lines[i].split(" ")]
            self.links[i-1,0] = nums_fila[0]
            self.links[i-1,1] = nums_fila[1]
        self.reds_line = [int(i) for i in lines[len(lines)-2].split(" ")] 
        self.blues_line = [int(i) for i in lines[len(lines)-1].split(" ")]

        # Variables for the algorithm
        self.link_ways = (np.zeros([self.first_line[0],4]) - 1)
        self.link_states = np.zeros([self.first_line[0],4])
        self.flagRB = True
        self.toRemove = []
        self.waysNumber = 0

    # Primary functions
    def graphWaysConstruction(self):
        for i in range(0,self.first_line[0]):
            for j in range(0,self.first_line[0]):
                if i != j:
                    x = 0.1
                    if self.links[i,0] == self.links[j,0] or self.links[i,0] == self.links[j,1]:
                        if self.links[i,0] == self.links[j,1]: x = 0.2
                        if self.link_ways[i,0] == -1 : self.link_ways[i,0] = j + x
                        elif self.link_ways[i,1] == -1 : self.link_ways[i,1] = j + x
                    if self.links[i,1] == self.links[j,0] or self.links[i,1] == self.links[j,1]:
                        if self.links[i,1] == self.links[j,1]: x = 0.2
                        if self.link_ways[i,2] == -1 : self.link_ways[i,2] = j + x
                        elif self.link_ways[i,3] == -1 : self.link_ways[i,3] = j + x
    def linkStatesCalculation(self):

        self.flagRB = True
        for x in self.reds_line:
            self.markLinkRecursive(self.findColor(x))
        self.flagRB = False
        for x in self.blues_line:
            self.markLinkRecursive(self.findColor(x))

    # Secondary functions
    def findColor(self,value):
        position = np.where(self.links[:,0] == value)[0]
        if len(position) > 0 : 
            return np.ndarray.item(position + 0.1)
        else: 
            position = np.where(self.links[:,1] == value)[0]
            return np.ndarray.item(position + 0.2)
    def position(self,value):
        value = round(value - 0.1, 1)
        row = value // 1
        col =  round(value % 1, 2) * 10
        return [row,col]
    def markLinkRecursive(self,value):
        rowcol = self.position(value)
        direction = rowcol[1]
        if self.flagRB == False: direction += 2
        if self.link_states[int(rowcol[0]),int(direction)] == 0:
            self.link_states[int(rowcol[0]),int(direction)] = 1
            if rowcol[1] == 0:
                if self.link_ways[int(rowcol[0]),2] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),2])
                if self.link_ways[int(rowcol[0]),3] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),3])
            else:
                if self.link_ways[int(rowcol[0]),0] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),0])
                if self.link_ways[int(rowcol[0]),1] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),1])
    def findVertices(self):
        for i in range(0,self.first_line[0]):
            if np.all(self.link_states[i] == 1):
                print(self.links,self.links.shape[0])

                link1 = self.position(self.link_ways[i,0])[0]
                link2 = self.position(self.link_ways[i,1])[0]
                link3 = self.position(self.link_ways[i,2])[0]
                link4 = self.position(self.link_ways[i,3])[0]

                if np.any(self.link_states[int(link1)] == 0) and np.any(self.link_states[int(link2)] == 0):
                    self.toRemove.append(i+0.1)
                    self.waysNumber += 1
                if np.any(self.link_states[int(link3)] == 0) and np.any(self.link_states[int(link4)] == 0):
                    self.toRemove.append(i+0.2)
                    self.waysNumber += 1
        
        print(self.toRemove)

        return self.waysNumber
    # def findColors(self,value):

        


a = MyClass()
a.graphWaysConstruction()
a.linkStatesCalculation()
a.findVertices()



