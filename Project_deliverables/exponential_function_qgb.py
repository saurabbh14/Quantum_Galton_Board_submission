import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution

from Project_deliverables.circuit_initiator import circuit_initiator
from Project_deliverables.circuit_run import circuit_run
from Project_deliverables.helper_funcs import exp_dist_analysis, plot_counts


def theta_exponential_function(lam, to_right=True):
    if to_right:
        theta = 2 * np.arcsin(np.exp(-lam / 2))
    else:
        theta = np.pi - 2 * np.arcsin(np.exp(-lam / 2))
    return theta

def exponential_function_qgb_circuit_maker(num_rows, lam, to_right=True):
    '''
    Generates a QGB circuit for the exponential distribution function.
    One can choose decaying and rising distribution values.
    :param num_rows: Number of rows or layers in the Galton board
    :param lam: exponential function parameter (exp(lam))
    :param to_right: True => shift the outcomes to right resulting in rising exponential function
                     False => shift the outcomes to left resulting in decaying exponential function
    :return: qc: a qiskit circuit object
    '''
    theta_lam = theta_exponential_function(lam, to_right=to_right)
    qc = circuit_initiator(num_rows)
    qc.x(num_rows+1)
    qc.reset(0)
    reset_pos = num_rows + 2
    for i in range(num_rows):
        cx_pos = num_rows - i + 1
        for j in range(i+1):
            if to_right:
                if j == 0:
                  theta = theta_lam
                else:
                  theta = 0 #np.pi
            else:
                if j == i:
                  theta = theta_lam
                else:
                  theta = np.pi
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



