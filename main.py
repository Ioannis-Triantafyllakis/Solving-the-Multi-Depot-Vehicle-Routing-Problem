import time

st = time.time()
cpu_st = time.process_time()

from miscellanious_functions import DepotsAndNodesPairsLists, MDVRPModelInstances, RoutingInfoContainer, SolutionPlot, SolutionMetricsFinder, MDVRP_BenchmarkInstances
#from ClarkeAndWrightHeuristic import ClarkeAndWrightSavingsAlgorithm
from ClarkeAndWrightSavingsAlgorithm import ClarkeAndWrightSavingsAlgorithmWithVehConstraint
from MDVRP_KMeansFunc import KMeansClusteringBasedNodesSelection
from MDVRP_HierClustFunc import HierClusteringBasedNodeSelection

inst = MDVRPModelInstances(50, 9, 2, 2, 100, 20, 5) 

# Uncomment only one from the 4 selection algorithms below

DictOfDepotsAndNodesPairs = KMeansClusteringBasedNodesSelection(inst) # "KMeans-Clustering-Based Clarke & Wright Heuristic"
# DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "ward") # "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Ward Linkage)"
# DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "complete") # "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Complete Linkage)"
# DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "average") # "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Average Linkage)"

print("Depots and the clients each one will serve:")
print(DictOfDepotsAndNodesPairs)
print()

ListsOfPairs = DepotsAndNodesPairsLists(DictOfDepotsAndNodesPairs, inst["allNodes"])
print("****************", ListsOfPairs)
xx = inst["allxs"]        
yy = inst["allys"]
all_ids = inst["allIds"]
NoOfVehicles = inst["NoOfVehicles"]
Cap = inst["VehicleCap"]
all_dem = inst["all_dem"]

Container = RoutingInfoContainer(ListsOfPairs, ClarkeAndWrightSavingsAlgorithmWithVehConstraint, NoOfVehicles, Cap, all_dem)
print()
print("All Routes:")
print(Container["RoutesContainer"])  # Returns a list of all routes

figure = SolutionPlot(xx, yy, all_ids, Container["RoutesContainer"], 100)     
figure.savefig('plot.jpeg')

Metrics = SolutionMetricsFinder(Container["CostsContainer"], Container["TotalCostsContainer"], all_dem, Container["RoutesContainer"], DictOfDepotsAndNodesPairs)
print("Total Solution Cost: ", Metrics["TotalCost"])
print("Average Route Cost: ", Metrics["AvgRouteCost"])
print("Median Route Cost: ", Metrics["MedianRouteCost"])
print("Average Depot Cost: ", Metrics["AvgDepotCost"])
print("Median Depot Cost: ", Metrics["MedianDepotCost"])
print("Percentage of the total demand satisfied: ", Metrics["PctOfTotalDemandSatisfied"])
print("Percentage of customers served: ", Metrics["PctOfCustomersVisited"])


et = time.time()
cpu_et = time.process_time()

elapsed_time = round(et - st, 3)
cpu_elapsed_time = round((cpu_et - cpu_st)/100, 3)

print('Execution time:', elapsed_time, 'seconds')
print('CPU time:', cpu_elapsed_time, 'seconds')

