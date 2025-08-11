import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution
from scipy.stats import binom

from Project_deliverables.circuit_initiator import circuit_initiator
from Project_deliverables.circuit_run import circuit_run
from Project_deliverables.helper_funcs import counts_vecs, mse_calc, plot_counts, normal_dist_analysis, \
    plot_stochastic_run_distribution, stochastic_run_analysis
from Project_deliverables.stochastic_run import stochastic_sum_bin_sorting


def one_peg_circuit_maker():
    '''
    A single peg circuit is created, just to test the waters
    :return: qc: a qiskit circuit object
    '''
    qc = circuit_initiator(1)
    qc.h(0)
    qc.x(2)
    qc.cswap(0, 1, 2)
    qc.cx(2, 0)
    qc.cswap(0, 2, 3)
    qc.measure(1, 0)
    qc.measure(3, 1)
    return qc

def fine_grained_qgb_circuit_maker(num_rows, bias_level=0, theta_param=None):
    '''
    Generates a fine-grained biased qgb circuit as explained in https://arxiv.org/abs/2202.01735
    :param num_rows: number of rows in the Galton board
    :param bias_level: how much bias at each peg?
                        bias_level = 0 (all pegs have the same probability mass function) (default)
                        bias_level = 1 (pegs in each row have the same probability mass function)
                        bias_level = 2 (each peg has different probability mass function)

    :param theta_param: The bias to be introduced by which angle?
                        = None (Hadamard gate applied) (default)
                        = single theta value (all gates are rotated by theta) (must: bias_level=0)
                        = a list of ´num_rows´ theta values (must: bias_level=1)
                        = a list of the lists of the theta values for each peg (must: bias_level=2)
    :return: qc: a qiskit circuit object
    '''
    qc = circuit_initiator(num_rows)
    qc.x(num_rows+1)
    qc.reset(0)
    reset_pos = num_rows + 2
    for i in range(num_rows):
        cx_pos = num_rows - i + 1
        for j in range(i+1):
            if theta_param is None:
                theta = np.pi/2  # Hadamard gate unbiased circuit
            else:
                if bias_level == 0:
                    theta = theta_param # single rotation to all pegs
                elif bias_level == 1:
                    theta = theta_param[i] # single rotation at each row
                else:
                    theta = theta_param[i][j] # different rotations at each peg
            qc.rx(theta, 0)
            qc.cswap(0, cx_pos-1,cx_pos)
            qc.cx(cx_pos,0)
            qc.cswap(0, cx_pos,cx_pos+1)
            cx_pos += 2
            qc.reset(0)
        qc.barrier()
        if i > 0:
            for  j in range(i):
                qc.cx(reset_pos,reset_pos-1)
                qc.reset(reset_pos)
                reset_pos -= 2
            reset_pos = num_rows + i +2

    for i in range(1,2*(num_rows+1),2):
        qc.measure(i,i//2)
    return qc


