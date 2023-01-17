## Understanding Dynamics of Polarization via Multiagent Social Simulation

Understanding polarization in social networks is challenging because it depends not only on user attitudes but also their interactions and exposures to information. We adopt Social Judgment Theory to operationalize attitude shift and model user behavior based on empirical evidence from past studies. We design a social simulation to analyze how content sharing affects user satisfaction and polarization in a social network. We investigate the influence of varying tolerance in users and selectively exposing users to congenial views. We find that (1) higher user tolerance slows down polarization and leads to lower user satisfaction; (2) higher selective exposure leads to higher polarization and lower user reach; and (3) both higher tolerance and higher selective exposure lead to a more homophilic social network.

### Data and Code

This repository contains the data and code to reproduce the results of our experimentats. In additions the repository also contains the results generated over multiple simulation runs along with statistical analysis of the results.

The seed data used in the simulation can be found under the *'data'* directory. 
- *initial_data_x.csv* files contain the attributes of all agents at the start of the simulation
- *facebook_graph.txt* files contain the information about the social network (i.e., connections in the graph)
- *post_conf.csv* files contain the list of all posts (messages exchanged between users) used in the simulation (each post has an associated issue it discusses, and a stance score towards that issue)

The code for the data can be found under the *'src'* directory.
- *Exp1_SE.ipynb* contains code to run the experiment 1 (with different levels of selective exposure)
- *Exp2_TOL.ipynb* contains code to run the experiment 2 (with different levels of user tolerance)

The results can be found under the *'results'* directory. Results for experiment 1 can be found under the folder *SE*, and for experiment 2 under the folder *TOL* (results are for each simulation run). SE_avg and TOL_avg contains the average from all the results (i.e., average of multiple simulation runs). 
- *final_data_xx.csv* files contain the final attribute values of all agents after 5k posts have been shared.
- *results_xx.csv* files contain all the primary and secondary metrics after each post has been shared in the social network.
