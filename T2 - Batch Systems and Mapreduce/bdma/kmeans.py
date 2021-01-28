import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as sci
import re

def saveResultForIteration (result_i, iter_ID, assignments):
    if iter_ID not in result_i.keys():
        result_i[iter_ID] = {}
    for i in range (0, len(assignments)):
        clusterID = assignments[i][0]
        if clusterID not in result_i[iter_ID].keys():
            result_i[iter_ID][clusterID] = ClusterData(clusterID)
        result_i[iter_ID][clusterID].appendToX(assignments[i][1][0])
        result_i[iter_ID][clusterID].appendToY(assignments[i][1][1])


# Just for Plotting ----------------------------------------------------------------------------
class ClusterData:
    def __init__(self, id):
        self.clusterID = id
        self.x = []
        self.y = []

    def appendToX (self, value):
        self.x.append(value)

    def appendToY (self, value):
        self.y.append(value)

    def setClusterId (self, value):
        self.clusterID = value

