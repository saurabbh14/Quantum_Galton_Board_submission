from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit


def circuit_initiator(num_rows):
    '''
    Initiates the circuit qubits with Quantum and classical registers.
    :param num_rows: number of rows or layers in the Galton board
    :return: qc: QuantumCircuit object with 2*num_rows+1 qubits and
    num+1 classical bits
    '''
    num_qubits = 2 * (num_rows +1)
    num_clbits = num_rows +1
    qr = QuantumRegister(num_qubits, name='q')
    cr = ClassicalRegister(num_clbits, name='c')
    qc = QuantumCircuit(qr,cr)
    return qc