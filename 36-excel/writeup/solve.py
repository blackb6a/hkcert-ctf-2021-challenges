from z3 import *

def weight(l):
    result = []
    for i in range(len(l)):
        result.append((i+1)*l[i])
    return result

flag_len = 25

x = [BitVec('x_{}'.format(i),9) for i in range(flag_len)]

y = [ [ BitVec("y_{}_{}".format(i, j), 9) for j in range(8) ]
      for i in range(flag_len) ]

bitmap = [[(x[i]>>j)&1 for j in range(8)] for i in range(flag_len)]

ascii_range = [ And(0x20 <= x[i], x[i] <= 0x7f) for i in range(flag_len) ]

xor_relation = [(bitmap[i][j] ^ bitmap[(i+1)%flag_len][(j+1)%8]) == y[i][j]
                for i in range(flag_len) for j in range(8)]

column_sum = [28, 26, 21, 19, 11, 21, 20, 15, 11, 27, 9, 17, 22, 25, 29, 17, 20, 21, 15, 18, 18, 15, 21, 19, 12]
row_sum = [152, 130, 102, 184, 135, 49, 310, 174]

column = [Sum(weight(y[i])) == column_sum[i] for i in range(flag_len)]
row = [Sum(weight(zip(*y)[j])) == row_sum[j] for j in range(8)]

flag = [x[0] == ord('h'), x[1] == ord('k'), x[2] == ord('c'), x[3] == ord('e'), x[4] == ord('r'), x[5] == ord('t'),
    x[6] == ord('2'), x[7] == ord('1'), x[8] == ord('{'), x[-1] == ord('}')]

s = Solver()
s.add(ascii_range)
s.add(flag)
s.add(xor_relation)
s.add(column)
s.add(row)

if s.check() == sat:
    m = s.model()
    r = [ m.evaluate(x[i]).as_long() for i in range(flag_len) ]
    print(''.join(map(chr,r)))
else:
    print("unsat")