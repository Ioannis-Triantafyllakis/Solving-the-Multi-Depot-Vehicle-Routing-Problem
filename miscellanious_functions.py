import matplotlib.pyplot as plt
import random
import statistics
import pandas as pd

def MDVRPModelInstances(NoOfCustomers, Seed, NoOfVehicles, NoOfDepots, Grid, VehicleCap, MaximumDem):
    '''
    This function takes as input: 1) The number of customers, 2) a Seed, 3) The number of vehicles, 4) The number of depots, 
    5) A grid, which is the maximum value a customer's coordinates can get, and the length of x and y axis at the same time, 
    6) The Vehicle Capacity, and 7) The maximum demand a customer can have. By using a Seed number with the "random" framework, 
    reproducible MDVRP instances are created in the form of a dictionary.
    '''
    random.seed(Seed)

    AllDepots = []
    for i in range(1, int(NoOfDepots)+1):
        dep = ["0"+str(i), random.randint(1, Grid), random.randint(1, Grid)]        
        AllDepots.append(dep)
    
    all_Customers = [] # Lists with customers
    all_Nodes = []     # List with all Nodes (customers + depots)

    for i in AllDepots: # Appending the depots to the list of lists that includes all nodes
        all_Nodes.append(i)
    
    for i in range(1, int(NoOfCustomers)+1):
        cust = []
        cust = [i, random.randint(1, Grid), random.randint(1, Grid)]
        all_Customers.append(cust)
        all_Nodes.append(cust)

    all_ids = []
    all_x = []
    all_y = []
    all_custs_ids = []
    all_dem = []

    for i in range(0, len(all_Customers)):
        dem = [ all_Customers[i][0], random.randint(1, MaximumDem)]
        all_dem.append(dem)


    for i in range(0, len(all_Nodes)):
        id = all_Nodes[i][0]
        all_ids.append(id)
        x = all_Nodes[i][1]
        all_x.append(x)
        y = all_Nodes[i][2]
        all_y.append(y)
        if i==0:
            continue
        else:
            cust_id = all_Nodes[i][0]
            all_custs_ids.append(cust_id)

    DictOfVehiclesRoutes = {}
    for i in range(1, int(NoOfVehicles)+1):
        DictOfVehiclesRoutes['RouteOfVehicle_%s' % i] = []
        
    return {"allCustomers": all_Customers, 
            "allNodes": all_Nodes, 
            "allIds": all_ids, 
            "allxs": all_x, 
            "allys": all_y, 
            "NoOfCusts":NoOfCustomers,
            "AllDepots": AllDepots,
            "NoOfVehicles": NoOfVehicles,
            "all_dem": all_dem,
            "VehicleCap": VehicleCap, 
            "Seed": Seed}
    # all_Customers and All_Nodes are lists of lists. Format is [id, x, y].    


def DepotsAndNodesPairsLists(SelectionDict, AllNodesList):
    '''
    This function creates a list of lists of lists, where each sublist corresponds to a node with a [id, x coord, y coord]
    format, the second level lists are a depot with the nodes assigned to it, and the main list is a "container" list.
    Inputs:
    1) Dictionary of depots-nodes's pairs (created by the "selection" phase)
    2) A list of lists of all existing nodes' info with a [id, x coord, y coord] format
    The list it returns contains other lists, that are the input for distinct VRP's
    '''
    ListOfAllDepotsNodesPairs = list()

    for key, value in SelectionDict.items():
        DepotNodesPair = list()
        for i in AllNodesList:
            if i[0] in value or i[0] == key:
                DepotNodesPair.append([i[0], i[1], i[2]])
        ListOfAllDepotsNodesPairs.append(DepotNodesPair)

    return ListOfAllDepotsNodesPairs


def RoutingInfoContainer(ListOfPairs, RoutingHeuristic, NoOfVehicles, Cap, all_dem):
    '''
    This function gets as input: 1) The list with all nodes of each distinct VRP, 2) The routing heuristic function, 3)
    The number of vehicles, 4) the total capacity of each vehicle, and 5), the list with each customer's demand.
    This function works as "container" that stores the results of all distinct VRP's solved.
    '''
    RoutesContainer = []
    CostsContainer = []
    TotalCostsContainer = []
    DistMatricesContainer = []

    for list in ListOfPairs:        
        RoutesContainer.append(RoutingHeuristic(list, Cap, all_dem, NoOfVehicles)["Routes"])
        CostsContainer.append(RoutingHeuristic(list, Cap, all_dem, NoOfVehicles)["AllCosts"])
        TotalCostsContainer.append(RoutingHeuristic(list, Cap, all_dem, NoOfVehicles)["TotalCost"])
        DistMatricesContainer.append(RoutingHeuristic(list, Cap, all_dem, NoOfVehicles)["Distance_Matrix"])

    return {"RoutesContainer":RoutesContainer,
            "CostsContainer":CostsContainer,
            "TotalCostsContainer":TotalCostsContainer, 
            "DistMatricesContainer":DistMatricesContainer}


def SolutionPlot(all_xs, all_ys, all_Ids, RoutesContainer, GridSize):
    '''
    This function creates a "matplotlib" figure with the MDVRP solution.
    '''
    fig, ax = plt.subplots()

    for route in RoutesContainer:
        for subroute in route:
            route_xcoords = list()
            route_ycoords = list()
            for node in subroute:
                idx = all_Ids.index(node)
                xcoord = all_xs[idx]
                ycoord = all_ys[idx]
                route_xcoords.append(xcoord)
                route_ycoords.append(ycoord)
            ax.plot(route_xcoords, route_ycoords, '-o')

    for xi, yi, pidi in zip(all_xs, all_ys, all_Ids):
            ax.annotate(str(pidi), xy=(xi,yi), fontsize = 13)

    # Show the plot.
    fig.set_size_inches(8, 8)

    plt.xlim([0, GridSize])
    plt.ylim([0, GridSize])
    plt.style.use("default") # seaborn, default, seaborn-pastel

    return fig


def SolutionMetricsFinder(CostsContainer, TotalCostsContainer, all_dem, RoutesContainer, DictOfDepotsAndNodesPairs):
    '''
    This function gets results from the distinct VRP's solved, and calculates and returns 9 metrics related to the MDVRP solution.
    '''
    AllRoutesCost = list()
    for RouteList in CostsContainer:
        for RouteCost in RouteList:
            AllRoutesCost.append(RouteCost)

    DemandSatisfied = 0
    NoOfCustsVisited = 0
    for route in RoutesContainer:
        for subroute in route:
            for r in subroute:
                if subroute[-1] == r or subroute[0] == r:
                    continue
                else:
                    NoOfCustsVisited = NoOfCustsVisited + 1
                    for cust in all_dem:
                        if r == cust[0]:
                            DemandSatisfied = DemandSatisfied + cust[1]

    TotalDemand = 0
    NoOfCustsToBeVisited = 0
    for k, v in DictOfDepotsAndNodesPairs.items():
        for node in v:
            NoOfCustsToBeVisited = NoOfCustsToBeVisited + 1
            for i in all_dem:
                if node == i[0]:
                    TotalDemand = TotalDemand + i[1]

    PctOfTotalDemandSatisfied = round((DemandSatisfied/TotalDemand)*100, 2)
    PctOfCustomersVisited = round((NoOfCustsVisited/NoOfCustsToBeVisited)*100, 2)

    AvgRouteCost = round(sum(AllRoutesCost)/len(AllRoutesCost), 2)
    MedianRouteCost = round(statistics.median(AllRoutesCost), 2) 

    AvgDepotCost = round(sum(TotalCostsContainer)/len(TotalCostsContainer), 2)
    MedianDepotCost = round(statistics.median(TotalCostsContainer), 2)
    TotalCost = round(sum(TotalCostsContainer), 2)

    return {"TotalCost" : TotalCost,
            "AvgRouteCost" : AvgRouteCost,
            "MedianRouteCost" : MedianRouteCost,
            "AvgDepotCost" : AvgDepotCost,
            "MedianDepotCost" : MedianDepotCost,
            "PctOfTotalDemandSatisfied" : PctOfTotalDemandSatisfied,
            "DemandSatisfied" : DemandSatisfied,
            "TotalDemand" : TotalDemand, 
            "PctOfCustomersVisited" : PctOfCustomersVisited}


def MDVRP_BenchmarkInstances(Instance, Seed):

    with open(Instance) as f:
        lines = f.readlines()

    df = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    InstanceList = list()
    for item in lines:
        InstanceList.append(list(item.split()))
    df = pd.DataFrame(InstanceList)

    NoOfVehicles = int(df[1][0])
    NoOfCusts = int(df[2][0])
    NoOfDepots = int(df[3][0])

    VehicleCap = int(df[1][1])

    all_Customers = list()
    all_Nodes = list()
    allIds = list()
    all_dem = list()
    allxs = list()
    allys = list()
    allDepots = list()

    for row in range(NoOfVehicles+1, NoOfCusts+NoOfVehicles+1):
        cust = df[row:row+1]

        cust_id = int(cust[0].astype("int"))
        cust_x = int(cust[1].astype("int"))
        cust_y = int(cust[2].astype("int"))
        cust_dem = int(cust[4].astype("int"))

        customer = [cust_id, cust_x, cust_y]
        demand = [cust_id, cust_dem]
    
        all_Customers.append(customer)
        all_dem.append(demand)

    counter = 1
    for row in range(NoOfVehicles+1, NoOfCusts+NoOfVehicles+NoOfDepots+1):
        node = df[row:row+1]
        node_id = int(node[0].astype("int"))
        if node_id > NoOfCusts:
            node_id = "0" + str(counter)
            counter = counter + 1
            allIds.append(node_id)
            node_x = int(node[1].astype("int"))
            node_y = int(node[2].astype("int"))

            allxs.append(node_x)
            allys.append(node_y)
            #all_Nodes.append([node_id, node_x, node_y])
            all_Nodes.insert(0, [node_id, node_x, node_y])
            depot = [node_id, node_x, node_y]
            allDepots.append(depot)

        else:
            node_x = int(node[1].astype("int"))
            node_y = int(node[2].astype("int"))
            allxs.append(node_x)
            allys.append(node_y)
            all_Nodes.append([node_id, node_x, node_y])
            allIds.append(node_id)

    return {"allCustomers": all_Customers, 
            "allNodes": all_Nodes, 
            "allIds": allIds, 
            "allxs": allxs, 
            "allys": allys, 
            "NoOfCusts":NoOfCusts,
            "AllDepots": allDepots,
            "NoOfVehicles": NoOfVehicles,
            "all_dem": all_dem,
            "VehicleCap": VehicleCap, 
            "Seed": Seed}
