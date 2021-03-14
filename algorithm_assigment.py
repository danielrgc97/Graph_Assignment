#!/usr/bin/env python3
import numpy as np

class MyClass(object):
    def __init__(self):

        # Extracting values from the file
        lines = []
        f = open("case_01.in", "r")
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

    def graphWaysConstruction(self):
        # self.links = np.concatenate((self.links, (np.zeros([self.first_line[0],4])-1)), axis=1)
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
        print(np.where(self.links[:,1] == 7).shape)  



a = MyClass()
a.graphWaysConstruction()
a.linkStatesCalculation()



