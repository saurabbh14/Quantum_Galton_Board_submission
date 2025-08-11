def fine_grained_biased_qgalton_board_circuit_maker(qc, num_rows, theta_param):
    qc.x(num_rows+1)
    qc.reset(0)
    reset_pos = num_rows + 2
    for i in range(num_rows):
        cx_pos = num_rows - i + 1
        for j in range(i+1):
            theta = theta_param[i][j]
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