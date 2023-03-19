from scipy.spatial import distance_matrix
import pandas as pd
import re


def ClarkeAndWrightSavingsAlgorithmWithVehConstraint(DepotNodePair, Cap, all_dem, Vehicles):
    '''
    This function takes as inputs: 
    1) The list with all nodes id's, x and y coordinates of a single VRP, 
    2) The Vehicle Capacity, 
    3) The list with each customer's demand, 
    4) The number of vehicles, 
    and implements the Clarke & Wright Savings Algorithm with a vehicle number constraint. For each customer pair, the savings value is 
    calculated, and each customer pair along with the savings value is inserted into a list, which is sorted in descending order. Then, 
    individual and unique (one-customer) routes are initialized (one for each customer). Iteratively, starting from the pairs with the 
    highest saving value, the routes in which the nodes of the examined pair appear, are merged if: 1) these 2 nodes are not in the same
    route, and 2) these 2 nodes are in the end or the beginning of their corresponding routes, and 3) the vehicle capacity is not violated
    by the merging of the 2 routes these nodes belong to. The algorithm creates a number of routes, which if is greater than the number 
    of the existing vehicles, then the most expensive routes will be removed until this number is now equall to the number of vehicles. 
    If this number is less than the number of existing vehicles though, it is kept as is, and not all vehicles will be mobilized. 
    This architecture "favors" keeping low total costs, but avoids achieving the serving of all customers.
    '''
    def DistMatrixCreator(ListOfAllNodes):
        '''
        This function gets as input the list with all nodes of the distinct VRP to be solved, and creates a distance matrix.
        '''
        data = []
        ListOfAllIds = []
        for i in range(0, len(ListOfAllNodes)):
            pair = []
            x = ListOfAllNodes[i][1]
            pair.append(x)
            y = ListOfAllNodes[i][2]
            pair.append(y)
            data.append(pair)
        
            global DepotNamePlaceholder
        
            if type(ListOfAllNodes[i][0]) == str:
                DepotNamePlaceholder = ListOfAllNodes[i][0] 
                ListOfAllNodes[i][0] = 0 # We convert the depot's id datatype to integer so we can use it in the distance matrix
            ListOfAllIds.append(ListOfAllNodes[i][0])
    
        df = pd.DataFrame(data, columns=['x', 'y'], index=ListOfAllIds)
        DfDistMatrix = round(pd.DataFrame(distance_matrix(df.values, df.values, p = 2), index=df.index, columns=df.index), 1)
        ArrayDistMatrix = DfDistMatrix.to_numpy()
    
        return {"DataFrameOfDistMatrix": DfDistMatrix, 
                "ArrayOfDistMatrix": ArrayDistMatrix
                }

    a = DepotNodePair
    mat = DistMatrixCreator(a)["DataFrameOfDistMatrix"]

    savings = dict()

    for r in mat.index:
        if r == 0:
            continue
        for c in mat.columns:
            if c == 0:
                continue
            if int(c) != int(r):            
                a = max(int(r), int(c))
                b = min(int(r), int(c))
                key = '(' + str(a) + ',' + str(b) + ')'
                savings[key] = mat[0][int(r)] + mat[0][int(c)] - mat[c][r]
                list_to_append = [a, b]

    # put savings in a pandas dataframe, and sort by descending
    sv = pd.DataFrame.from_dict(savings, orient = 'index')
    sv.rename(columns = {0:'saving'}, inplace = True)
    sv.sort_values(by = ['saving'], ascending = False, inplace = True)


    savings_list = list()

    for i, row in sv.iterrows():        
        savings_pair = re.findall(r"[\w']+", i) # Removing all non numeric characters
        savings_sublist = [int(savings_pair[0]), int(savings_pair[1])] # Converting the nodes' ids from strings to integers
        savings_list.append(savings_sublist)

    all_ids = list()
    for node in DepotNodePair:
        all_ids.append(node[0])

    all_ids.pop(0)

    Routes = list()

    for ind in all_ids:
        initial_route = [0, ind, 0]
        Routes.append(initial_route)

    def NodesInSameRouteOrNotCondition(node1, node2, routeslist):
        '''
        This function gets 2 nodes and a list of the routes as input, and checks whether these 2 nodes are in the same route or not.
        '''
        RouteOfFirstNode = None
        RouteOfSecondNode = None
        condition = None
        for route in routeslist:
            if node1 in route:
                RouteOfFirstNode = route
            if node2 in route:
                RouteOfSecondNode = route
        if set(RouteOfFirstNode) == set(RouteOfSecondNode):
            condition = False
        else:
            condition = True
        return condition

    def NodesInEndOrBeginningOfRoute(node1, node2, routeslist):
        '''
        This function gets 2 nodes and a list of the routes as input, and checks whether these 2 nodes are locatd in the end or in the
        beginning of the routes they belong to.
        '''
        condition1 = False
        condition2 = False
        condition = None #False

        for route in routeslist:
            if node1 in route:
                if (node1 == route[1]) or (node1 == route[-2]):
                    condition1 = True
            if node2 in route:
                if (node2 == route[1]) or (node2 == route[-2]):
                    condition2 = True
                
        if (condition1 == True) and (condition2 == True):
            condition = True
        else:
            condition = False
        return condition 

    def CapacityConstraintChecker(all_dem, r1, r2, cap):
        '''
        This function takes as input the list of lists of each customer's demand, the maximum vehicle capacity, and 2 routes that 
        are about to be merged in the Clarke & Wright Heuristic, and checks whether the merging of these 2 routes will violate 
        the capacity constraint per vehicle. If the constraint is violated it returns "False", and if not, it returns "True".
        '''
        totalcap = 0
        for node in r1:
            for node_dem_pair in all_dem:
                if node == node_dem_pair[0]:
                    totalcap = totalcap + node_dem_pair[1]
        for node in r2:
            for node_dem_pair in all_dem:
                if node == node_dem_pair[0]:
                    totalcap = totalcap + node_dem_pair[1]

        cap_constraint = None
        if totalcap <= cap:
            cap_constraint = True
        else:
            cap_constraint = False
    
        return cap_constraint

    for pair in savings_list:
            item_1 = pair[0] 
            item_2 = pair[1]

            cond1 = NodesInSameRouteOrNotCondition(item_1, item_2, Routes)
            cond2 = NodesInEndOrBeginningOfRoute(item_1, item_2, Routes)
            
            if (cond1 == True) and (cond2 == True):
                # Finding the list where item_1, and item_2 are
                FirstRouteToMerge = list()
                SecondRouteToMerge = list()

                for route in Routes:
                    if item_1 in route:
                        FirstRouteToMerge = route
                    if item_2 in route:
                        SecondRouteToMerge = route

                if CapacityConstraintChecker(all_dem, FirstRouteToMerge, SecondRouteToMerge, Cap) == True:
            
                    if (FirstRouteToMerge[1] == item_1) and (SecondRouteToMerge[-2] == item_2):
                        FirstRouteToMerge[1:1] = SecondRouteToMerge[1:len(SecondRouteToMerge) - 1]
                    elif (FirstRouteToMerge[1] == item_1) and (SecondRouteToMerge[1] == item_2):
                        FirstRouteToMerge[1:1] = SecondRouteToMerge[len(SecondRouteToMerge) - 2:0:-1]
                    elif (FirstRouteToMerge[-2] == item_1) and (SecondRouteToMerge[1] == item_2):
                        FirstRouteToMerge[len(FirstRouteToMerge) - 1:len(FirstRouteToMerge) - 1] = SecondRouteToMerge[1:len(SecondRouteToMerge) - 1]
                    elif (FirstRouteToMerge[-2] == item_1) and (SecondRouteToMerge[-2] == item_2):
                        FirstRouteToMerge[len(FirstRouteToMerge) - 1:len(FirstRouteToMerge) - 1] = SecondRouteToMerge[len(SecondRouteToMerge) - 2:0:-1]

                    for route in Routes:
                        if route == SecondRouteToMerge:
                            Routes.remove(route)
                else:
                    continue
            

    def Costfinder(Routes, mat):
        ListOfAllCosts = list()
        for route in Routes:
            cost = 0
        
            for i in range(0, len(route[:-1])):
                cost = cost + mat[route[i]][route[i+1]]
            ListOfAllCosts.append(round(cost, 2))
        return ListOfAllCosts


    ListOfRoutesCosts = Costfinder(Routes, mat)

    TotalCost = 0
    for c in ListOfRoutesCosts:
        TotalCost = TotalCost + c

    for route in Routes:
        for n, i in enumerate(route):
            if i == 0:
                route[n] = DepotNamePlaceholder

    for idx in mat.index:
        if idx == 0:
            mat.rename(index={idx: DepotNamePlaceholder}, inplace=True)

    for colname in mat.columns:
        if colname == 0:
            mat.rename(columns = {colname:DepotNamePlaceholder}, inplace = True)

    if len(Routes) > Vehicles:

        NoOfRoutesToBeRemoved = len(Routes) - Vehicles

        for i in range(0, NoOfRoutesToBeRemoved):
            RouteToBeRemoved = ListOfRoutesCosts.index(max(ListOfRoutesCosts))
            del Routes[RouteToBeRemoved]
            del ListOfRoutesCosts[RouteToBeRemoved]


    ListOfAllRoutesCosts = Costfinder(Routes, mat)

    TotalCost = 0
    for c in ListOfAllRoutesCosts:
        TotalCost = TotalCost + c
        TotalCost = round(TotalCost, 2)

    return {"Routes":Routes, 
            "AllCosts":ListOfAllRoutesCosts,
            "TotalCost":TotalCost,
            "Distance_Matrix": mat}

