from qiskit_aer import AerSimulator
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import Options, Session, SamplerV2 as Sampler



def circuit_run(qc, shots=2000):
    '''
    Samples the given circuit on all to all simulator, namely AerSimulator
    :param qc: circuit to run
    :param shots: number of samples
    :return: gives the sampler.run.result object
    '''
    # use simulator
    backend = AerSimulator()
    # make quantum circuit compatible to the backend
    pm = generate_preset_pass_manager(backend = backend, optimization_level=3)

    qgalton = pm.run(qc)
    #run and get counts
    sampler = Sampler(mode=backend)
    job = sampler.run([qgalton], shots=shots)
    result = job.result()
    return result

