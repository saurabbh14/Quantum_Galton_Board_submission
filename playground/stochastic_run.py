import numpy as np
from matplotlib import pyplot as plt

from playground.circuit_initiator import circuit_initiator
from playground.circuit_run import circuit_run
from playground.fine_grained_qgb import fine_grained_biased_qgalton_board_circuit_maker


def tensor_sum(u, v):
    m = len(u)
    n = len(v)
    result = [0 for _ in range(n*m)]

    for i in range(m):
        for j in range(n):
            result[i * n + j] = u[i] + v[j]

    return result

def counts_multi_run(num_runs, qc):
    counts_matrix = []
    for _ in range(num_runs):
        result = circuit_run(qc)
        counts = result[0].data.c.get_counts()
        counts_new = []
        counts_keys = list(counts.keys())
        counts_keys = sorted(counts_keys)
        for i in range(len(counts)):
            counts_new.append((i, counts[counts_keys[i]]))
        counts_matrix.append(counts_new)
    return counts_matrix

def sum_over_independent_runs(num_runs, qc):
    counts_matrix = counts_multi_run(num_runs, qc)
    a0, a1 = zip(*counts_matrix[0])
    for i in range(1, num_runs):
        b0, b1 = zip(*counts_matrix[i])
        a0 = tensor_sum(a0, b0)
        a1 = tensor_sum(a1, b1)
    return list(zip(a0, a1))

def stochastic_sum_bin_sorting(num_runs, qc):
    count = sum_over_independent_runs(num_runs, qc)
    num_rows = qc.num_qubits//2
    count_i = []
    count_bin = []
    for i in range(num_rows* num_runs+1):
        bin_count = 0
        for j in range(len(count)):
            if count[j][0] == i:
                bin_count += count[j][1]
        count_i.append(i)
        count_bin.append(bin_count)
    count_bin = np.array(count_bin) / sum(count_bin) # normalizing / probability distribution
    new_count = list(zip(count_i, count_bin))
    return new_count

num_runs = 8
num_rows = 4
qc = circuit_initiator(num_rows)
#qgb_circuit_maker(qc, num_rows)
#biased_qgalton_board_circuit_maker(qc, num_rows,np.pi/2)
thetas = [[np.pi/2 for j in range(i+1)] for i in range(num_rows)]
fine_grained_biased_qgalton_board_circuit_maker(qc, num_rows, thetas)
stoc_dist = stochastic_sum_bin_sorting(num_runs, qc)
print(stoc_dist)
a, b = zip(*stoc_dist)
plt.bar(a,b)
plt.show()