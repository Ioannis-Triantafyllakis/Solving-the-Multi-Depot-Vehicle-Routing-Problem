from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import math
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)
import os
os.environ["OMP_NUM_THREADS"] = '1'


def KMeansClusteringBasedNodesSelection(Instances):
    '''
    This function gets as inputs the problem instances the user selects, and implements a K-Means Clustering algorithm. More specifically, the algorithtm 
    clusters all customer nodes based on their x and y coordinates, where the number of clusters is equal to the number of clusters with the maximum Silhouette score, 
    then the centroid of each cluster is found, and each depot is assigned to one cluster centroid exactly. This assignment happens iteratively: for every depot, 
    we calculate the distance between the depot and each centroid, and the closest centroid is assigned to the depot. Before the next iteration, all distances between 
    the centroid that was just selected, with each depot left is updated to a very large number, so it will never get selected again.At last, each depot will serve
    the nodes that belong to the cluster whose centroid was assigned to the depot. It must be noted that as the assignment gets done iteratively, it is not 
    always guaranteed that each depot will be assigned to its closest centroid.
    Inputs:
    1) AllCustomers: a list of lists, where the length of the list is equal to the number of customers, and each sublist corresponds to a customer and has
       the following format: [id, x-coord, y-coord]
    2) AllDepots: a list of lists, where the length of the list is equal to the number of depots, and each sublist corresponds to a depot and has the following 
       format: [id, x-coord, y-coord]
    3) AllIds: a list that contains the id of all nodes existing (whether they are depots or customers)
    4) Seed: This is the seed with which the problem instances were initialized. This is used when fitting the KMeans algorithm, so it will always initialize
       the same centroids in the 1st iteration, for each seed, so every clustering process is reproducible.
    
    Outputs:
    1) ClientAllocationToDepots: A dictionary where keys are depot id's, and values are a list of the nodes that will be served from the depot that corresponds
       to the key. For example, if the function returns {'01': [1, 2, 3, 4], '02': [5, 6]}, it means that clients 5, and 6 will be served by depot "02", while
       clients 1, 2, 3, and 4 will be served by depot "01".        
    '''

    X = pd.DataFrame(list(Instances["allCustomers"]),
               columns =['id', 'x', 'y'])

    SilhouetteScoresDict = dict() # Here we will store each possible pair of number of clusters and it's silhouette score

    for n_clusters in range(2, len(Instances["AllDepots"])+1):
        clusterer = KMeans(n_clusters=n_clusters, random_state=int(Instances["Seed"]))
        preds = clusterer.fit_predict(X[["x", "y"]])
        #centers = clusterer.cluster_centers_

        score = silhouette_score(X[["x", "y"]], preds)
        
        SilhouetteScoresDict[n_clusters] = score

    # Finding the number of clusters with the highest silhouette score
    NoOfClusters = max(SilhouetteScoresDict, key=SilhouetteScoresDict.get)

    # Kmeans algorithm will be fitted with the afforementioned number of clusters.
    Kmean = KMeans(n_clusters=NoOfClusters, random_state=int(Instances["Seed"]))

    Kmean.fit(X[["x", "y"]])

    AllClusterCenters = Kmean.cluster_centers_ # Array
    AllClusterCentersList = []
    for j in AllClusterCenters:
        j = list(j)
        AllClusterCentersList.append(j)

    AllDepots = Instances["AllDepots"]

    counter = 0
    for i in AllClusterCentersList:
        i.insert(0, counter)
        counter = counter+1

    AllDepotsDict = {}
    for i in AllDepots:
        AllDepotsDict[i[0]] = [i[1], i[2]]

    AllClustersCentersDict = {}
    for i in AllClusterCentersList:
        AllClustersCentersDict[i[0]] = [round(i[1], 2), round(i[2], 2)]

    CentroidToDepotsAssignment = {}
    for i in range(0, len(AllDepots)):
        CentroidToDepotsAssignment[i] = None

    # In this matrix we will add the distances between all possible depot-cluster center pairs.
    matrix = [[0 for row in range(0, len(AllDepots))] for col in range(0, len(AllClusterCentersList))]

    # Populating the distance matrix
    for i in AllDepots:
        for j in AllClusterCentersList:
            matrix[j[0]][(int(i[0]))-1] = round(math.dist([ i[1], i[2] ], [ j[1], j[2] ]), 2)
        

    matrix_array = np.array([np.array(xi) for xi in matrix]) # Converting the matrix (that is a list of lists) to a numpy array

    for i in range(0, len(matrix_array)):
        
        ColIndexOfMin = np.where(matrix_array[i] == np.min(matrix_array[i]))[0] # Getting the column index with the minimum value in the row
        CentroidToDepotsAssignment[i] = int(ColIndexOfMin)
        matrix_array[:, ColIndexOfMin] =  100000 # We set all values of the column whose index has the minimum value in the row to a very large number

    SelectionsDict = {"0" + str(key + 1): value for key, value in CentroidToDepotsAssignment.items()}

    FinalSelectionsDict = dict()

    for key, value in SelectionsDict.items():
        if value != None:
            FinalSelectionsDict[key] = value


    ListOfIds = Instances["allIds"]

    NoOfDepots = len(Instances["AllDepots"])


    ListOfCustIds = []  # List with only customers' Ids 
    for i in range(NoOfDepots, len(ListOfIds)):
        ListOfCustIds.append(ListOfIds[i])

    CentroidsList = list(Kmean.labels_)

    ClusterCentroidSelectionDict = {}
    PositionCounter = 0
    for i in list(Kmean.labels_):
        index = CentroidsList.index(i)
        PositionCounter += 1
    
        if index in ClusterCentroidSelectionDict:
            ClusterCentroidSelectionDict[index].append(PositionCounter)
        else:
            ClusterCentroidSelectionDict[index] = [PositionCounter]

    ClientAllocationToDepots = {}

    values = list(ClusterCentroidSelectionDict.values())
    for i,(k,v) in enumerate(FinalSelectionsDict.items()):
        ClientAllocationToDepots[k] = values[i]

    # A dictionary containing the pairing between depots and clients will be returned.
    return ClientAllocationToDepots 
