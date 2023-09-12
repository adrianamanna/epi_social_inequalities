**I. CONTENT**

- config_mats.yaml: configuration file to run the script run_compute_mat.
- config_sim.yaml: configuration file to run the script run_simulation.

- run_compute_mat.py: phyton script to build decoupled age contact matrices
- plt_matrices.py: phyton script to plot decoupled age contact matrices
- run_simulation_epi.py: phyton script to simulate the spread of an epidemic accounting for decoupled matrices. The model implemented is a SEIR model.
- run_simulation.py: phyton script to simulate the spread of an epidemic accounting for decoupled matrices. The model implemented is a SEIR model.
- plt_epi.py: phyton script to process and plot the results of the simulations

In the 'data' folder:
- data4th.pkl: sample file in pickle format
- data4th_a.pkl: sample file in pickle format (adult population)
- data4th_k.pkl: sample file in pickle format (children population)


In the 'utils':
- epi_models_age_1dim.py: epidemiological model (SEIRD with vaccination)
- epi_tools.py: functions to set up the epidemic simulation (ie. initialization of the population, vaccination coverage etc)
- fn_matrices.py: functions to compute the matrices
- labs.py: list of labels and color palettes
- plot_tools: function to plot the decoupled matrices
- simulation_prep: functions to preprocess the results of the simulations

The code will create three folders: '_matrices', '_res' and '_figure' where it stores 
respectively the matrices, the results of the simulations and the figures. 



________________________

**II. SAMPLE DATA** 

The sample data provided refers to the 4th COVID-19 wave and are represented by individuals.
In the 'data4th_a.pkl,' we only provide data regarding the adult population (>18 ya). 
In the 'data4th_k.pkl,' we only provide data regarding the children's population (<18 ya). 

The samples contain respectively 700, 500 and 200 random observations of the original data. 

To run the code on your data. You need to format the latter as the one that we provided. 

Variables:
- 'wave': number of data collection
- 'id': individial id
- 'tot_all_': total number of contacts
- 'age_group8': age group
- 'employed': employment status
- 'education3': education level [low, mid,high]
- 'settlement_cur_num': settlement [capital, rural,urban]
- 'fin_now3a': financial situation  [low, mid,high]
- 'w': weight of the individual
- 'all_0', 'all_1', 'all_2','all_3', 'all_4', 'all_5', 'all_6', 'all_7': number of contacts with each age group
_________________


**III. INSTRUCTIONS**

STEP 1: BUILD THE DECOUPLED AGE-CONTACT MATRICES

1. In the config_mats.yaml you can select the variables according to which you want to 
build the matrices. 

Configure the variable VARS as a list of lists. Where, in each element 
You can choose any number of variables simultaneously - we suggest a maximum of two dimensions to prevent the matrix from being too sparse. 
The possible dimensions are:
    - 'employed',
    - 'education3',
    - 'settlement_cur_num',
    - 'fin_now3a'
    - 'aggregate' (ie. no stratification)

NOTE: TO SIMULATE THE EPIDEMIC WITH ANY DECOUPLED MATRIX YOU NEED TO COMPUTE BEFORE THE AGGREGATE MATRIX AS WELL.

2. Run 'python run_compute_mat.py' This script computes and stores the decoupled matrices in the '_matrices' folder.

3. Run 'python plt_matrices.py' This script plots the decoupled matrices and stores the figures in the '_figures' folder.



STEP 2: SIMULATE THE EPIDEMIC
1. In the config_sim.yaml you can select the additional dimension that you want to take into account in the 
simulation. It has to be input as a list of one string.
In the same file, you can modify any epidemiological parameter.

2. Run 'python run_simulation_epi.py' This script runs the simulations of the epidemic model and stores the results in the '_res' folder.


3. Run 'python plt_epi.py' This script processes the output of the simulation and plots the infection curves and the attack rates. The plot is then stored in the '_figures' folder.


________________________

**IV. PACKAGES VERSIONS**

json5                     0.9.6              pyhd3eb1b0_0  
matplotlib                3.5.2            py39h06a4308_0  
matplotlib-base           3.5.2            py39hf590b9c_0  
matplotlib-inline         0.1.6            py39h06a4308_0  
numpy                     1.21.5           py39h6c91a56_3  
numpy-base                1.21.5           py39ha15fc14_3 
pandas                    1.4.4            py39h6a678d5_0   
pickleshare               0.7.5           pyhd3eb1b0_1003  
scipy                     1.9.1            py39h14f4228_0  
yaml                      0.2.5                h7b6447c_0 

________________________
- The installation on a normal desktop computer requires less than a minute.
- The installation does not require any non-standard hardware


 

