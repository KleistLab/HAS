# H*igh* A*cceptance* S*ampling* (HAS) for spreading dynamics on adaptive networks

## System requirements 

### Operating System

This workflow was tested on macOS Sonoma Version 14.4.1 and CentOS Linux 7 (Core). 

### Prerequisites
#### Python

version 3.11.6

Packages:

numpy,
scipy,
pandas,
time,
sys,
cython

#### Compile

Before the first execution, the code must be compiled. Navigate to the folder [scripts/HAS_SID](https://github.com/KleistLab/HAS/tree/main/scripts/HAS_SID) or [scripts/HAS_SIDRS](https://github.com/KleistLab/HAS/tree/main/scripts/HAS_SIDRS) and execute the following command

```
python3 setup.py build_ext --inplace
```

## Input

The following files must be provided in order for the code to execute. All files contain agent specific parameters in an N-dimensional array:
- lambda_plus.npy (edge creation parameter $\lambda_i^+$)
- lambda_minus.npy (edge deletion parameter $\lambda_i^-$)
- r_diag_vector.npy (diagnosis rate (S $\to$ D) $\lambda_i^{\text{diag}}$)
- r_inf_vector.npy (infection rate (S+I $\to$ I+I) $\lambda_i^{\text{inf}}$)
- r_rec_vector.npy (recovery rate (I $\to$ R) $\lambda_i^{\text{rec}}$)
- r_sus_vector.npy (susceptible rate (R $\to$ S) $\lambda_i^{\text{sus}}$)
- status_vec.npy (initial status (S,I,D,R) for agent $i$)

These files need to be saved in a folder. The folder name needs to be specified in [`inputs.py`](https://github.com/KleistLab/HAS/blob/main/scripts/HAS_SIDRS/inputs.py). In this file, the following variables need to be defined
- N: number of agents
- name: name of the calculation
- path_to_results: file path where the outputs should be stored
- t_max: simulation time
- sims: number of stochastic repetitons
- seed: seed of random number generation
- beta: contact reduction after diagnosis
- path_to_parameters = file path to repository that keeps the agent specific parameter files



## Execution

Navigate to the repository that contains the code [scripts/HAS_SIDRS](https://github.com/KleistLab/HAS/tree/main/scripts/HAS_SIDRS) and execute
```
python3 run.py
```

## Output
The following files are created in the folder *results*, with the following structure:
```
|-- results
 	|-- has_feat_result_extended_*N*_*sims*_*t_max*.csv  # Number of agents per compartment at each (integer) time step, each row is one simulation
	|-- has_feat_network_result_*N*_*sims*_*t_max*.csv  # Average $\lambda_i^+$ at each (integer) time step, each row is one agent
	|-- has_feat_inf_result_*N*_*sims*_*t_max*.csv  # Probability for each agent to be infected at each (integer) time step, each row is one agent
```

## Demo
Demo datasets are provided in the repository folder [`demo`](https://github.com/KleistLab/VASIL/tree/main/demo)

If your environment is not yet activated, type



