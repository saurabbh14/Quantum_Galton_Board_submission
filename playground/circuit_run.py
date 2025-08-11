from qiskit_aer import AerSimulator
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import Options, Session, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram, plot_distribution
import matplotlib.pyplot as plt

from playground.circuit_demo import qc

def circuit_run(qc):
    # use simulator
    backend = AerSimulator()
    # make quantum circuit compatible to the backend
    pm = generate_preset_pass_manager(backend = backend, optimization_level=3)

    qgalton = pm.run(qc)
    #run and get counts
    sampler = Sampler(mode=backend)
    job = sampler.run([qgalton], shots=10000)
    result = job.result()
    return result

