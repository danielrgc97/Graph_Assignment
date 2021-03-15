#!/usr/bin/env python3
import sys
import numpy as np

class MyClass(object):
    def __init__(self):
        # Importing graph data into the variables "first_line", "links", "reds_line" and "blues_line"
        lines = []
        f = open(str(sys.argv[1]), "r")
        lines = f.readlines()
        self.first_line = [int(i) for i in lines[0].split(" ")]
        self.links = np.zeros([self.first_line[0],2])
        for i in range(1, self.first_line[0] + 1):
            nums_fila = [int(j) for j in lines[i].split(" ")]
            self.links[i-1,0] = nums_fila[0]
            self.links[i-1,1] = nums_fila[1]
        string = lines[int(len(lines)-2)]
        if lines[int(len(lines)-2)][len(lines[int(len(lines)-2)]) - 2] == ' ': 
            lines[int(len(lines)-2)] = lines[int(len(lines)-2)][:-2]
        self.reds_line = [int(i) for i in lines[len(lines)-2].split(" ")]
        if lines[int(len(lines)-1)][len(lines[int(len(lines)-1)]) - 2] == ' ': 
            lines[int(len(lines)-1)] = lines[int(len(lines)-1)][:-2]
        self.blues_line = [int(i) for i in lines[len(lines)-1].split(" ")]

        # Other shared variables 
        self.orderedBuffer = 0
        self.link_ways = 0
        self.link_states = 0
        self.flagRB = True
        self.toRemove = []
        self.pathsNumber = 0
        self.originalSize = self.first_line[0]

    # Primary functions
    def graphWaysConstruction(self):
        # This function creates 2 matrices, one to save the information of the links in
        # an ordered matrix to spend less time searching "orderedBuffer", and another in which it saves for
        # each link the possible other 4 links to which it connects "link_ways".
        self.orderedBuffer = (np.zeros([self.originalSize + 1, 3]) - 1)
        self.link_ways = (np.zeros([self.first_line[0],4]))

        # Construction of "orderedBuffer" array
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
        
        # Construction of "link_ways" array
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
    def linkStatesCalculation(self):
        # This function is in charge of determining the state of the links, these states
        # consist of 4 bits, because there are 2 colors and 2 directions. These states allows to
        # know if a specific color can be found in a specific direction. If for example there are
        # both red and blue in both directions of that link, the status of that link will be "1 1 1 1".
        # This marking starts from each color found in the graph, and it marks all the links recursively.
        # If a markup process finds links that have already been marked in that color and direction, it stops
        # the markup in that direction.
        self.link_states = np.zeros([self.first_line[0],4])
        self.flagRB = True
        for x in self.reds_line:
            self.markLinkRecursive(self.orderedBuffer[x - 1,0])
        self.flagRB = False
        for x in self.blues_line:
            self.markLinkRecursive(self.orderedBuffer[x - 1,0])
    def findPaths(self):
        # Using the link states this function finds most of the possible paths. Once it finds them, it cuts those
        # paths of the graph as if it were pruning a tree, to restart the process again.
        self.toRemove = []
        for i in range(0,self.first_line[0]):
            if np.all(self.link_states[i] == 1):

                link1 = self.position(self.link_ways[i,0])[0]
                link2 = self.position(self.link_ways[i,1])[0]
                link3 = self.position(self.link_ways[i,2])[0]
                link4 = self.position(self.link_ways[i,3])[0]

                if np.any(self.link_states[int(link1)] == 0) and np.any(self.link_states[int(link2)] == 0):
                    self.toRemove.append(i+0.2)
                    self.pathsNumber += 1
                if np.any(self.link_states[int(link3)] == 0) and np.any(self.link_states[int(link4)] == 0):
                    self.toRemove.append(i+0.1)
                    self.pathsNumber += 1
        print("fin iteration, paths found:", len(self.toRemove))
        if len(self.toRemove) > 0: self.cutGraph() # If any path has been found proceed to cut them
        elif len(self.reds_line) > 0 and len(self.blues_line) > 0 : self.pathsNumber += 1 # If no more paths have been found, analyze if there is still one last.

        return 0 < len(self.toRemove)
    # Secondary functions
    def position(self,value):
        # The entire algorithm saves in which column each Edge is located within each link,
        # with ".1" in case it is on the left column and ".2" in case it is on the right column.
        # And this function returns 2 ints with the row and column associated with that value.
        value = round(value - 0.1, 1)
        row = value // 1
        col =  round(value % 1, 2) * 10
        return [row,col]
    def markLinkRecursive(self,value):
        # This function takes care of marking a link in a specific direction and color, and propagates the marking by calling itself
        # in case the following links are not marked yet.
        rowcol = self.position(value)
        direction = rowcol[1]
        if self.flagRB == False: direction += 2 # Depending on this flag it marks Reds or Blues
        if self.link_states[int(rowcol[0]),int(direction)] == 0: # Condition for stop the marking if that directions are already marked
            self.link_states[int(rowcol[0]),int(direction)] = 1
            if rowcol[1] == 0:
                if self.link_ways[int(rowcol[0]),2] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),2])
                if self.link_ways[int(rowcol[0]),3] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),3])
            else:
                if self.link_ways[int(rowcol[0]),0] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),0])
                if self.link_ways[int(rowcol[0]),1] != -1: self.markLinkRecursive(self.link_ways[int(rowcol[0]),1])
    def cutGraph(self):
        # It is in charge of cutting the graph, as if a tree were being pruned. Eliminate the links that are a
        # vertex in each of the paths found
        for x in self.toRemove:
            self.findColorsRecursive(x)
        self.toRemove.sort(reverse=True)
        for x in self.toRemove:
            self.links = np.delete(self.links,int(x//1),0)
            self.first_line[0] -= 1
    def findColorsRecursive(self,value):
        # This function is in charge of finding the colors that belong to the path that has been erased, to be
        # able to erase them from the arrays "reds_line" and "blues_line".
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
        # This function is in charge of eliminating the colors that were found in the previous function into
        # the arrays "reds_line" and "blues_line".
        position = np.where(self.reds_line == edge)[0]
        if len(position) > 0 :
            self.reds_line = np.delete(self.reds_line,position)
        position = np.where(self.blues_line == edge)[0]
        if len(position) > 0 :
            self.blues_line = np.delete(self.blues_line,position)


# This is the main part of the process, where in each iteration these three functions are called until no more paths are found
a = MyClass()
morePathsToFind = True 
while(morePathsToFind == True):
    a.graphWaysConstruction()
    a.linkStatesCalculation()
    morePathsToFind = a.findPaths()

print("Total number of paths found:",a.pathsNumber)
