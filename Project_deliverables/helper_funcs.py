import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_distribution
from scipy.stats import binom


# Circuit related
def draw_circuit(qc):
    qc.draw('mpl',fold=100)

def get_counts(result):
    counts = result[0].data.c.get_counts()
    return counts

def counts_vecs(counts):
    keys = sorted(list(counts.keys()))
    shots = sum(list(counts.values()))
    key_vec = []
    count_vec = []
    for i, key in enumerate(keys):
        key_vec.append(i)
        count_vec.append(counts[key]/ shots)
    return key_vec, count_vec

def plot_counts(result):
    counts = get_counts(result)
    k, v = counts_vecs(counts)
    plt.bar(k,v)
    plt.show()

# Data analysis related
def mse_calc(u, v):
    mse_vec = [(u[i] - v[i])**2 for i in range(len(u))]
    return sum(mse_vec)

def tvd_calc(u, v):
    u = np.array(u)
    v = np.array(v)
    return 0.5 * np.sum(np.abs(u - v))

def normal_dist_analysis(counts):
    k, count_vec = counts_vecs(counts)
    num_rows = len(k)-1
    exp_dist = binom.pmf(k, num_rows, 0.5)
    mse = mse_calc(count_vec, exp_dist)
    print("Normal Distribution Analysis")
    print("Measured mean:", np.mean(count_vec))
    print("Measured variance:", np.var(count_vec))
    print("Expected mean:", np.mean(exp_dist))
    print("Expected variance:", np.var(exp_dist))
    print("Mean Squared Error:", mse)
    print()

def exp_pmf(k, lam):
    e = [np.exp(-lam * k[i]) for i in range(len(k))]
    p = [e[i] / sum(e) for i in range(len(e))]
    return p

def exp_dist_analysis(counts, lam, to_right=True):
    k, count_vec = counts_vecs(counts)
    num_rows = len(k)-1
    lam = -lam if to_right else lam
    exp_dist = exp_pmf(k, lam)
    mse = mse_calc(count_vec, exp_dist)
    tvd = tvd_calc(count_vec, exp_dist)
    print("Exponential Distribution Analysis")
    print("Measured mean:", np.mean(count_vec))
    print("Measured variance:", np.var(count_vec))
    print("Expected mean:", np.mean(exp_dist))
    print("Expected variance:", np.var(exp_dist))
    print("Mean Squared Error:", mse)
    print("Total Variation Distatnce:", tvd)
    print()

def plot_stochastic_run_distribution(dist):
    a, b = zip(*dist)
    plt.bar(a, b)
    plt.show()

def stochastic_run_analysis(dist):
    a, b = zip(*dist)
    num_rows = len(a)-1
    exp_dist = binom.pmf(a, num_rows, 0.5)
    mse = mse_calc(b, exp_dist)
    print("Normal Distribution Analysis (Stochastic Run)")
    print("Measured mean:", np.mean(b))
    print("Measured variance:", np.var(b))
    print("Expected mean:", np.mean(exp_dist))
    print("Expected variance:", np.var(exp_dist))
    print("Mean Squared Error:", mse)
    print()