import numpy as np

from Project_deliverables.circuit_run import circuit_run
from Project_deliverables.helper_funcs import counts_vecs


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
        k, counts_new = counts_vecs(counts)
        count_new = []
        for i in range(len(counts)):
            count_new.append((i, counts_new[i]))
        counts_matrix.append(count_new)
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
