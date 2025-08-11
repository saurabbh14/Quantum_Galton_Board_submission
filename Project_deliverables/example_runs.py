from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution

from Project_deliverables.circuit_run import circuit_run
from Project_deliverables.exponential_function_qgb import exponential_function_qgb_circuit_maker
from Project_deliverables.general_qgb import fine_grained_qgb_circuit_maker
from Project_deliverables.helper_funcs import normal_dist_analysis, plot_stochastic_run_distribution, \
    stochastic_run_analysis, plot_counts, exp_dist_analysis
from Project_deliverables.quantum_walk_qgb_circuit_maker import quantum_walk_qgb_circuit_maker
from Project_deliverables.stochastic_run import stochastic_sum_bin_sorting

# Task: General QGB implementation
print("General QGB")
num_rows = 4
print("Number of rows: ", num_rows)
qc = fine_grained_qgb_circuit_maker(num_rows, bias_level=0, theta_param=None)
result = circuit_run(qc, shots=10000)
counts = result[0].data.c.get_counts()
#plot_counts(result) # uncomment to see the plot
normal_dist_analysis(counts)
print()

# Bonus task: Stochastic QGB implementation
print("Stochastic QGB run")
num_rows = 4
num_runs = 8
print("Number of rows: ", num_rows)
print("Number of runs: ", num_runs)
qc = fine_grained_qgb_circuit_maker(num_rows, bias_level=0, theta_param=None)
stoc_dist = stochastic_sum_bin_sorting(num_runs,qc)
#plot_stochastic_run_distribution(stoc_dist) # uncomment to see the plot
stochastic_run_analysis(stoc_dist)
print()

#Task Exponential distribution function QGB
print("Exponential QGB")
num_rows = 4
lam = 1
print("Number of rows: ", num_rows)
print("Number of lambda: ", lam)
qc = exponential_function_qgb_circuit_maker(num_rows, lam, to_right=False)
result = circuit_run(qc)
counts = result[0].data.c.get_counts()
#plot_counts(result) # uncomment for plot
exp_dist_analysis(counts, lam, to_right=False)
print()

#Task Quantum walk QGB
print("Quantum Walk QGB")
num_rows = 4
print("Number of rows: ", num_rows)
qc = quantum_walk_qgb_circuit_maker(num_rows)
result = circuit_run(qc)
counts = result[0].data.c.get_counts()
#plot_counts(result) # uncomment for plot.
