import numpy as np
from matplotlib import pyplot as plt

from playground.biased_qgb import biased_qgalton_board_circuit_maker
from playground.circuit_initiator import circuit_initiator
from playground.crude_qgb import qgb_circuit_maker

num_rows = 1
qc = circuit_initiator(num_rows)
#qgb_circuit_maker(qc, num_rows)
biased_qgalton_board_circuit_maker(qc, num_rows,np.pi/2)
#qc.draw('mpl')
#plt.show()
