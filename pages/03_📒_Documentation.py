import streamlit as st
from PIL import Image
import numpy as np

# Title.
st.title("🔎Documentation🔍")

# Table of contents.
st.markdown("\
**Table of Contents**: <br>\
\
<ul>\
    <li>1. <a href=\"#1-introduction\">Introduction</a></li>\
    <li>2. <a href=\"#2-mathematical-model\">Mathematical Model</a></li>\
    <li>3. <a href=\"#3-algorithms\">Algorithms</a>\
        <ul>\
            <li>3.1. <a href=\"#3-1-k-means-clustering-based-node-selection-algorithm\">K-Means Clustering-Based Node Selection Algorithm</a></li>\
            <li>3.2. <a href=\"#3-2-hierarchical-clustering-based-node-selection-algorithm-ward-linkage\">Hierarchical Clustering Based Node Selection Algorithm (Ward-Linkage)</a></li>\
            <li>3.3. <a href=\"#3-3-hierarchical-clustering-based-node-selection-algorithm-complete-linkage\">Hierarchical Clustering Based Node Selection Algorithm (Complete-Linkage)</a></li>\
            <li>3.4. <a href=\"#3-4-hierarchical-clustering-based-node-selection-algorithm-average-linkage\">Hierarchical Clustering Based Node Selection Algorithm (Average-Linkage)</a></li>\
        </ul>\
    </li>\
    <li>4. <a href=\"#5-references\">References</a></li>\
</ul>\
", unsafe_allow_html=True)

# 1. Introduction.
st.markdown("## 1. Introduction")

st.write("\
    A MDVRP is a non-deterministic polynomial-hard (NP-hard) combinatorial optimization problem and \
    solving it by exact algorithm is time consuming and computationally intractable, [2] and constitutes\
    of more than one depot, a few customers that must be served, and a specified number of vehicles that \
    start and end in the same depot after serving customers. To solve a MDVRP, customers need to be assigned\
    first in a depot, and then the routing process can take place.\
    \
")

col1, col2 = st.columns(2)
with col1:
    image = np.asarray(Image.open("plot.jpeg"))
    st.image(image=image, width=650)

with col2:
    st.write("\
        In the example (left), the problem has: 2 depots ('01', and '02'), with 2 vehicles in each depot, and 50 customers\
        with each customer having a demand ranging from 1 to 3 units. The solution of the algorithm, proposes 2 routes\
        starting from depot '02' and one route starting from depot '01'.\
        ")

# 2. Mathematical Model.
st.markdown("## 2. Mathematical Model")
col1, col2 = st.columns(2)

with col1:
    st.markdown("Sets")
    st.markdown('* _D_: the set of all Depots')
    st.markdown('* _C_: the set of all Customers')
    st.markdown('* _V_: the set of all Vehicles')


    st.markdown("Indices")
    st.markdown("* _i_: depot index")
    st.markdown("* _j_: customer index")    
    st.markdown("* _k_: route index")

with col2:
    st.markdown("Parameters")
    st.markdown("* _NV_: the number of vehicles")
    st.markdown("* _ND_: the numbr of depots")    
    st.markdown("* _NC_: the number of customers")
    st.markdown("* _dj_: demand of customer i")
    st.markdown("* _r_: number of total routes")
    st.markdown("* _dj_: demand of customer i")  
    st.markdown("* _Qk_: capacity of vehicle/route k")
    st.markdown("* _Cij_: distance between point i and j")  

st.markdown("The objective function for the Multi-Depot Vehicle Routing Problem is given by the following formula:")
st.latex("min\int_{i \in D  \cup  V}\int_{j \in D  \cup  V}\int_{k \in V}Cij")

# Algorithms
st.markdown("## 3. Algorithms")

col1, col2 = st.columns(2)
with col1:
    st.write("\
        An MDVRP solution construction algorithm can be formulated as a two-phase process: a ***Selection*** phase can be implemented\
        first, in order to find which customers will be served by which depot, and then a ***Routing*** phase can be used in order to\
        solve all the distinct VRPs created by the first phase.4 different heuristics are suggested, where the first phase\
        (the Selection phase) is based on 4 different clustering methods (one for each heuristic), while the second phase\
        (the Routing phase) is the same in all four heuristics, in which a variation of the Clarke and Wright heuristic with\
        a vehicle number constraint is used. The methodology flow of the algorithms can be seen in the right.\
        ")
with col2:
    image = np.asarray(Image.open("flow.png"))
    st.image(image=image, width=350)

st.markdown("### 3.1. K-Means Clustering-Based Node Selection Algorithm")
st.write("\
    K-Means Clustering-Based Node Selection Algorithm is the first out of four different algorithms that are used in\
    the first phase (Selection Phase) of the proposed MDVRP heuristic. This algorithm utilizes the K-Means Clustering\
    algorithm that was suggested by Ball and Hall (1965) [1]. The goal of K-Means Algorithm is to correctly separate\
    observations in a dataset into groups based on objects properties, and in our case based on customer\
    x and y coordinates.\
    ")

st.write("\
    The algorithm works as follows: at first, centroids are randomly initialized whose number is equal to the number\
    of clusters/groups, and then each observation is assigned to each closest centroid based on a distance criterion\
    (Euclidean distance in our implementation). Then for each centroid, a new centroid/mean is calculated, and the initial\
    centroid of the corresponding cluster is moved into the position of the new centroid. If there was a movement, the algorithm\
    repeats itself, while if there was not move, the algorithm terminates.\
    ")

st.write("Time Complexity:")
st.latex("O(nkt))")

st.write("Space Complexity:")
st.latex("O(n(d + k))")
st.write("Where ***n*** is the size of the dataset, ***k*** is the number of clusters, ***t*** is the number of iterations\
        the algorithm needs to achieve converge, and ***d*** is the number of attributes.")
st.write(" ")

st.markdown("### 3.2. Hierarchical Clustering-Based Node Selection Algorithm (Ward Linkage)")
st.write("\
    In Hierarchical Clustering with Ward Linkage, a distance matrix is first calculated containing the distance of all\
    possible observation pairs, and then each individual observation is set as a cluster. Then, iteratively, the 2 closest\
    clusters are merged into one, and the distance matrix gets updated. The distance between two clusters is computed as the\
    increase in the ***'error sum of squares' (ESS)*** after merging two clusters into one, so the term 'closest', means the clusters\
    whose merging has the 'minimum' increase in the ESS of the newly created cluster. The algorithm terminates when the number\
    of clusters is equal to 1, or more if the user has specified so.\
    ")
st.write("Time Complexity:")
st.latex("O( n^{2} ) ")

st.write("Space Complexity:")
st.latex("O( n^{3} ) ")
st.write("Where ***n*** is the size of the dataset.")
st.write(" ")

st.markdown("### 3.3. Hierarchical Clustering-Based Node Selection Algorithm (Complete Linkage)")
st.write("In Hierarchical Clustering with Complete Linkage, a distance matrix is again first calculated containing the distance\
        of all possible observation pairs, and then each individual observation is set as a cluster. Then, iteratively, the 2 closest\
        clusters are merged into one, and the distance matrix gets updated. The distance between two clusters is now computed as the greatest\
        distance from any member of one cluster to any member of the other cluster, meaning that “distance” is now defined as the longest\
        distance between two points in each cluster.\
        ")
st.write("Time Complexity:")
st.latex("O( n^{2} ) ")

st.write("Space Complexity:")
st.latex("O( n^{3} ) ")
st.write("Where ***n*** is the size of the dataset.")
st.write(" ")

st.markdown("### 3.4. Hierarchical Clustering-Based Node Selection Algorithm (Average Linkage)")
st.write("In Hierarchical Clustering with Average Linkage, a distance matrix is once again first calculated containing the distance of\
        all possible observation pairs, and then each individual observation is set as a cluster. Then, iteratively, the 2 closest clusters\
        are merged into one, and the distance matrix gets updated. The distance between two clusters is now computed as the average of all\
        pairwise distances of observations/customers belonging in these two clusters.")
st.write("Time Complexity:")
st.latex("O( n^{2} ) ")

st.write("Space Complexity:")
st.latex("O( n^{3} ) ")
st.write("Where ***n*** is the size of the dataset.")
st.write(" ")

st.markdown("## 4. References")


st.write("\
    [1] Ball, G. H., & Hall, D. J. (1965). ISODATA, a novel method of data analysis and pattern\
    classification. Stanford Research Institute.\
    \
")

st.write("\
    [2] Geetha, S., Poonthalir, G., & Vanathi, P. T. (2013). Nested particle swarm optimisation \
    for multi-depot vehicle routing problem. Int. J. Operational Research, 16(3), 330.\
    \
")
