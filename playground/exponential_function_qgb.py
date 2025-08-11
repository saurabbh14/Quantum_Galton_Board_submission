import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution

from playground.circuit_initiator import circuit_initiator
from playground.circuit_run import circuit_run
from playground.fine_grained_qgb import fine_grained_biased_qgalton_board_circuit_maker


def theta_exponential_function(lam, to_right=True):
    if to_right:
        theta = 2 * np.arcsin(np.exp(-lam / 2))
    else:
        theta = np.pi - 2 * np.arcsin(np.exp(-lam / 2))
    return theta

def exponential_function_qgalton_board_circuit_maker(qc, num_rows, lam, to_right=True):
    theta_lam = theta_exponential_function(lam, to_right=to_right)
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
        qc.measure(i,i)
    return qc

num_rows = 4
lam = 1 # exp(-x)
direction = "right"
qc = circuit_initiator(num_rows)
exponential_function_qgalton_board_circuit_maker(qc, num_rows, lam, to_right=False)
result = circuit_run(qc)
counts = result[0].data.c.get_counts()

plot_distribution(counts)
plt.show()