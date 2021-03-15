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
        self.orderedBuffer = 0
        self.link_ways = 0
        self.link_states = 0
        self.flagRB = True
        self.toRemove = []
        self.waysNumber = 1
        self.tamOriginal = self.first_line[0]

    # Functions
    def graphWaysConstruction(self):
        
        self.orderedBuffer = (np.zeros([self.tamOriginal + 1, 3]) - 1)
        self.link_ways = (np.zeros([self.first_line[0],4]))

        for i in range(0,self.first_line[0]):
            num1 = int(self.links[i,0])
            num2 = int(self.links[i,1])
            pos = 0
            while(self.orderedBuffer[num1 - 1, pos] != -1):
                pos +=1
            self.orderedBuffer[num1 - 1,pos] = i + 0.1
            pos = 0
            while(self.orderedBuffer[num2 - 1, pos] != -1):
                pos +=1
            self.orderedBuffer[num2 - 1,pos] = i + 0.2
        
        for i in range(0,self.first_line[0]):
            line = self.orderedBuffer[int(self.links[i,0] - 1)]
            j = 0
            while(len(line)>2):
                if line[j] == i + 0.1 :
                    line = np.delete(line,j)
                j += 1
            self.link_ways[i,0] = line[0]
            self.link_ways[i,1] = line[1]

            line = self.orderedBuffer[int(self.links[i,1] - 1)]
            j = 0
            while(len(line)>2):
                if line[j] == i + 0.2 :
                    line = np.delete(line,j)
                j += 1
            self.link_ways[i,2] = line[0]
            self.link_ways[i,3] = line[1]


        # self.link_ways = (np.zeros([self.first_line[0],4]) - 1)
        # for i in range(0,self.first_line[0]):
        #     for j in range(0,self.first_line[0]):
        #         if i != j:
        #             x = 0.1
        #             if self.links[i,0] == self.links[j,0] or self.links[i,0] == self.links[j,1]:
        #                 if self.links[i,0] == self.links[j,1]: x = 0.2
        #                 if self.link_ways[i,0] == -1 : self.link_ways[i,0] = j + x
        #                 elif self.link_ways[i,1] == -1 : self.link_ways[i,1] = j + x
        #             if self.links[i,1] == self.links[j,0] or self.links[i,1] == self.links[j,1]:
        #                 if self.links[i,1] == self.links[j,1]: x = 0.2
        #                 if self.link_ways[i,2] == -1 : self.link_ways[i,2] = j + x
        #                 elif self.link_ways[i,3] == -1 : self.link_ways[i,3] = j + x
    def linkStatesCalculation(self):
        self.link_states = np.zeros([self.first_line[0],4])
        self.flagRB = True
        for x in self.reds_line:
            self.markLinkRecursive(self.findColor(x))
        self.flagRB = False
        for x in self.blues_line:
            self.markLinkRecursive(self.findColor(x))
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
    def findPaths(self):
        self.toRemove = []
        for i in range(0,self.first_line[0]):
            if np.all(self.link_states[i] == 1):

                link1 = self.position(self.link_ways[i,0])[0]
                link2 = self.position(self.link_ways[i,1])[0]
                link3 = self.position(self.link_ways[i,2])[0]
                link4 = self.position(self.link_ways[i,3])[0]

                if np.any(self.link_states[int(link1)] == 0) and np.any(self.link_states[int(link2)] == 0):
                    self.toRemove.append(i+0.2)
                    self.waysNumber += 1
                if np.any(self.link_states[int(link3)] == 0) and np.any(self.link_states[int(link4)] == 0):
                    self.toRemove.append(i+0.1)
                    self.waysNumber += 1
        if len(self.toRemove) > 0: self.cutGraph()
        return 0 < len(self.toRemove)
    def cutGraph(self):
        for x in self.toRemove:
            self.findColorsRecursive(x)
        self.toRemove.sort(reverse=True)
        for x in self.toRemove:
            self.links = np.delete(self.links,int(x//1),0)
            self.first_line[0] -= 1
    def findColorsRecursive(self,value):
        rowcol = self.position(value)
        if rowcol[1] == 0:
            if self.link_ways[int(rowcol[0]),2] != -1: self.findColorsRecursive(self.link_ways[int(rowcol[0]),2])
            if self.link_ways[int(rowcol[0]),3] != -1: self.findColorsRecursive(self.link_ways[int(rowcol[0]),3])
            if self.link_ways[int(rowcol[0]),2] == -1 and self.link_ways[int(rowcol[0]),3] == -1:
                self.deleteColor(self.links[int(rowcol[0]),1])
        else:
            if self.link_ways[int(rowcol[0]),0] != -1: self.findColorsRecursive(self.link_ways[int(rowcol[0]),0])
            if self.link_ways[int(rowcol[0]),1] != -1: self.findColorsRecursive(self.link_ways[int(rowcol[0]),1])
            if self.link_ways[int(rowcol[0]),0] == -1 and self.link_ways[int(rowcol[0]),1] == -1:
                 self.deleteColor(self.links[int(rowcol[0]),0])
    def deleteColor(self,edge):
        position = np.where(self.reds_line == edge)[0]
        if len(position) > 0 :
            self.reds_line = np.delete(self.reds_line,position)
        position = np.where(self.blues_line == edge)[0]
        if len(position) > 0 :
            self.blues_line = np.delete(self.blues_line,position)



a = MyClass()
morePathsToFind = True 
while(morePathsToFind == True):
    a.graphWaysConstruction()
    a.linkStatesCalculation()
    morePathsToFind = a.findPaths()
print(a.waysNumber)


