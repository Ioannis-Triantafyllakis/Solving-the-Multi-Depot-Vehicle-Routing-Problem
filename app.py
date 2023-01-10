import streamlit as st
import time
from miscellanious_functions import DepotsAndNodesPairsLists, MDVRPModelInstances, RoutingInfoContainer, SolutionPlot, SolutionMetricsFinder
from ClarkeAndWrightSavingsAlgorithm import ClarkeAndWrightSavingsAlgorithmWithVehConstraint
from MDVRP_KMeansFunc import KMeansClusteringBasedNodesSelection
from MDVRP_HierClustFunc import HierClusteringBasedNodeSelection


st.set_page_config(page_title = "Multi-Depot Vehicle Routing Problem Simulator", 
page_icon="🚚", 
layout="wide"
)

st.title("Multi-Depot Vehicle Routing Problem Simulator")

with st.sidebar:
    st.subheader("Problem Instances")

    noc = st.number_input('Insert number of clients 🏬',
    min_value=1, 
    max_value=1000, 
    value=50,   
    step=1, 
    help="Insert the total number of clients that need to be served"
    )

    nos = st.number_input('Insert seed number 🌱',
    min_value=1, 
    max_value=1000,  
    value=38, 
    step=1, 
    help="Seed is a number which makes python generate the same data in each execution"
    )

    nov = st.number_input('Insert number of vehicles 🚚',
    min_value=1, 
    max_value=20, 
    value=2, 
    step=1, 
    help="The number of vehicles each depot has"
    )

    nod = st.number_input('Insert number of depots 🏭',
    min_value=2, 
    max_value=20, 
    value=2, 
    step=1, 
    help="The total number of exisitng depots"
    )

    nog = st.number_input('Insert grid size 📏',
    min_value=20, 
    max_value=200, 
    value=100, 
    step=5, 
    help="Grid is the size of the plot's height and width. It is also the maximum value a node's x and y coordinates can be equal to"
    )

    novc = st.number_input('Insert vehicle capacity 📦',
    min_value=2, 
    max_value=500, 
    value=50, 
    step=1, 
    help="test"
    )

    nomd = st.number_input('Insert maximum customer demand 📬',
    min_value=1, 
    max_value=200, 
    value=4, 
    step=1, 
    help="test"
    )
 
    st.subheader("Heuristics")

    option = st.selectbox(
    'Choose a Construction Algorithm:',
    ('KMeans-Clustering-Based Clarke & Wright Heuristic ', 
     'Hierarchical-Clustering-Based Clarke & Wright Heuristic (Ward Linkage) ',
     'Hierarchical-Clustering-Based Clarke & Wright Heuristic (Complete Linkage) ',
     'Hierarchical-Clustering-Based Clarke & Wright Heuristic (Average Linkage) '))


# Initializing the problem instances
inst = MDVRPModelInstances(noc, nos, nov, nod, nog, novc, nomd) 
xx = inst["allxs"]        
yy = inst["allys"]
all_ids = inst["allIds"]
print("All Customers", inst["allCustomers"])
print("All Nodes", inst["allNodes"])
print("Number Of Vehicles", inst["NoOfVehicles"])
print("All ids", inst["allIds"])
print("All x's", inst["allxs"])
print("All y's", inst["allys"])
print("All depots", inst["AllDepots"])
print("Number of customers", inst["NoOfCusts"])
print()

stime = time.time()
cpu_stime = time.process_time()

# Creating the dictionary with depots-nodes pairs (Selection phase)
DictOfDepotsAndNodesPairs = None

if option == "KMeans-Clustering-Based Clarke & Wright Heuristic ":
    DictOfDepotsAndNodesPairs = KMeansClusteringBasedNodesSelection(inst) 
elif option == "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Ward Linkage) ":
    DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "ward")
elif option == "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Complete Linkage) ":
    DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "complete")
elif option == "Hierarchical-Clustering-Based Clarke & Wright Heuristic (Average Linkage) ":
    DictOfDepotsAndNodesPairs = HierClusteringBasedNodeSelection(inst, "average")


print(DictOfDepotsAndNodesPairs)

ListsOfPairs = DepotsAndNodesPairsLists(DictOfDepotsAndNodesPairs, inst["allNodes"])
print(ListsOfPairs)
print()

NoOfVehicles = inst["NoOfVehicles"]
Cap = inst["VehicleCap"]
all_dem = inst["all_dem"]
try:
    Container = RoutingInfoContainer(ListsOfPairs, ClarkeAndWrightSavingsAlgorithmWithVehConstraint, NoOfVehicles, Cap, all_dem)
    Metrics = SolutionMetricsFinder(Container["CostsContainer"], Container["TotalCostsContainer"], all_dem, Container["RoutesContainer"], DictOfDepotsAndNodesPairs)
    print(Container["RoutesContainer"])  # Returns a list of all routes
    etime = time.time()
    cpu_etime = time.process_time()

except KeyError:
    st.warning('Warning : Either 1) The number of clients chosen is less than the number of Vehicles multiplied by the Number Of Depots.', icon="⚠️")
    st.warning("Warning : Or 2) The clustering assignment proccess assigned nodes that are less than the number of each depot's vehicles, \n \
                because even if (No Of Clients) >= (vehicles x depots), the clustering-based node-to-depot assignment algorithms may fail (for specific python seeds) to \n \
                assign enough nodes to each depot so all vehicles can be used in serving them. This usually happens when the number of clients is close to the number (vehicles*depots)"
                , icon="⚠️")

tab1, tab2 = st.tabs(["Overview", "Documentation"])

with tab1:
   
    try:
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.metric("Total Cost", Metrics["TotalCost"], delta=None, delta_color="normal", help="Total Cost of all routes combined") 
        with col2:
            st.metric("Avg. Route Cost", Metrics["AvgRouteCost"], delta=None, delta_color="normal", help="Average Cost of all routes")
        with col3:
            st.metric("Median Route Cost", Metrics["MedianRouteCost"], delta=None, delta_color="normal", help="Median Cost of all routes")
        with col4:            
            st.metric("Avg. Depot Cost", Metrics["AvgDepotCost"], delta=None, delta_color="normal", help="Average Cost of all depots")
        with col5:        
            st.metric("Median Depot Cost", Metrics["MedianDepotCost"], delta=None, delta_color="normal", help="Median Cost of all depots")
        with col6:
            st.metric("% Of Demand Satisfied", Metrics["PctOfTotalDemandSatisfied"], delta=None, delta_color="normal", help="Demand of Customers served, divided by total demand")
        with col7:
            st.metric("% Of Customers Visited", Metrics["PctOfCustomersVisited"], delta=None, delta_color="normal", help="No. of Customers served, divided by No. of all Customers")
    except NameError:
        pass

    try:
        col1, col2 = st.columns(2)

        with col1:   
            st.header("Routing Plot")
            figure = SolutionPlot(xx, yy, all_ids, Container["RoutesContainer"], nog) #     
            st.pyplot(fig=figure)
            figure.savefig('plot.jpeg')

            st.download_button(
            label="Download plot ⬇",
            data='plot.jpeg',
            file_name='plot.jpeg',
            mime = "application/octet-stream"
    )

        with col2:
            st.header("Routing information") 

            st.write('You selected:', option)

            with st.container():
                st.subheader('Solution Routes')
                for r in Container["RoutesContainer"]:     
                    for i in r:
                        st.write(str(i)) 

            elapsed_time = round(etime - stime, 3)
            cpu_elapsed_time = round((cpu_etime - cpu_stime)/100, 3)
        
            st.metric("Execution Time (sec)", elapsed_time, delta=None, delta_color="normal", help="Total Execution time") 
            st.metric("CPU Time (sec)", cpu_elapsed_time, delta=None, delta_color="normal", help="CPU time") 

    except NameError:
        pass
        
with tab2:
    st.write("test")
        
