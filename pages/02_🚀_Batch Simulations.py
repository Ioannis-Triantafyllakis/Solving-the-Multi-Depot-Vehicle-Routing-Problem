import streamlit as st
from miscellanious_functions import *
from ClarkeAndWrightSavingsAlgorithm import ClarkeAndWrightSavingsAlgorithmWithVehConstraint
from MDVRP_KMeansFunc import KMeansClusteringBasedNodesSelection
from MDVRP_HierClustFunc import HierClusteringBasedNodeSelection
import datetime

st.set_page_config(page_title = "Multi-Depot Vehicle Routing Problem Simulator", 
page_icon="🚚", 
layout="wide"
)

st.title("Multi-Depot Vehicle Routing Problem Simulator")
st.subheader("Batch Simulations")


with st.sidebar:
    st.subheader("Problem Instances")

    noc = st.number_input('Insert number of clients 🏬',
    min_value=1, 
    max_value=1000, 
    value=50,   
    step=1, 
    help="Insert the total number of clients that need to be served"
    )

    nos = st.slider("Choose seed range 🌱", 
    min_value=1, 
    max_value=200, 
    value=20, 
    step=1,
    help="Seed range for which mass testing will be implemented")

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
    max_value=800, 
    value=50, 
    step=1, 
    help="The maximum capacity of each truck"
    )

    nomd = st.number_input('Insert maximum customer demand 📬',
    min_value=1, 
    max_value=20, 
    value=3, 
    step=1, 
    help="The maximum demand a customer can have"
    )


if st.button('Start Batch Simulations'):
    dir_path = os.getcwd() # Get the current working directory

    # Loop through all the files in the current directory
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".xlsx"):  # Check if the file is an xlsx file
            file_path = os.path.join(dir_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            
    with st.spinner('Wait for it...'):
        start_time = time.time()
        BatchTestingExcelWriter(7, 1, nos, noc, nov, nod, nog, novc, nomd) 
        st.write("..Done")
        end_time = time.time()
        st.write("Elapsed time:", str(datetime.timedelta(seconds=end_time-start_time)))

        dir_path = os.getcwd()
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'rb') as file:
                    file_contents = file.read()
                    if st.download_button(label='📥 Export Excel File', data=file, file_name="Simulations.xlsx", mime="text/xlsx", key=2):
                        break
        
        
        
