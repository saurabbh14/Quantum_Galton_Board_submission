def qgb_circuit_maker(qc, num_rows):
    for i in range(num_rows):
        qc.h(0)
        if i == 0:
           qc.x(num_rows+1)
           qc.cswap(0, num_rows,num_rows+1)
           qc.cx(num_rows+1,0)
           qc.cswap(0,num_rows+1,num_rows+2)
        elif i == num_rows-1:
           for j in range(i+num_rows):
              qc.cswap(0, j+1,j+2)
              qc.cx(j+2,0)
           qc.cswap(0,num_rows+i+1,num_rows+i+2)
        else:
           cx_pos = num_rows + i + 1
           for j in range(i+1):
              if j == 0:
                cx_pos_z = num_rows - i + 1
                qc.cswap(0, cx_pos_z-1,cx_pos_z)
                qc.cx(cx_pos_z,0)
                qc.cswap(0, cx_pos_z,cx_pos_z+1)
                qc.cx(cx_pos_z+1,0)

              else:
                qc.cswap(0,cx_pos,cx_pos+1)
                qc.cx(cx_pos,0)
                qc.cswap(0, cx_pos-1,cx_pos)
                if j != i:
                  qc.cx(cx_pos-1,0)
                cx_pos -= 2

        if i < num_rows-1:
            qc.reset(0)

    for i in range(1, 2 * (num_rows + 1), 2):
        qc.measure(i, i)
    return qc

