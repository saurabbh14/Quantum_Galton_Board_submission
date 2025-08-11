from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit


def circuit_initiator(num_rows):
    num_qubits = 2 * (num_rows +1)
    qr = QuantumRegister(num_qubits, name='q')
    cr = ClassicalRegister(num_qubits, name='c')
    qc = QuantumCircuit(qr,cr)
    return qc