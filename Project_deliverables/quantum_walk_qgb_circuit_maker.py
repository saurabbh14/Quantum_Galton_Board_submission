import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution

from Project_deliverables.circuit_initiator import circuit_initiator
from Project_deliverables.circuit_run import circuit_run


def quantum_walk_qgb_circuit_maker(num_rows):
    theta = np.pi/2 # Hadamard rotation
    qc = circuit_initiator(num_rows)
    qc.reset(0)
    for i in range(num_rows):
        qc.h(0)
        #qc.rx(theta, 0)
        if i == 0:
           qc.x(num_rows+1)
           qc.cswap(0, num_rows,num_rows+1)
           qc.cx(num_rows+1,0)
           qc.cswap(0,num_rows+1,num_rows+2)
        else:
           cx_pos_z = num_rows - i + 1
           for j in range(i + 1):
               qc.cswap(0, cx_pos_z - 1, cx_pos_z)
               qc.cx(cx_pos_z, 0)
               qc.cswap(0, cx_pos_z, cx_pos_z + 1)
               if j != i:
                   qc.cx(cx_pos_z + 1, 0)
               cx_pos_z += 2
        qc.barrier()
    # No reset
    for i in range(1,2*(num_rows+1),2):
        qc.measure(i,i//2)
    return qc

