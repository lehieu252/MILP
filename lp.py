
import time
from ortools.linear_solver import pywraplp

def main():
    start = round(time.time() * 1000)
    f = open('output.txt', 'w')

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    s = []
    n = 11
    p = [9800,  28200,  33000,  36450,  47000,  52400,  52800,  59000,  89000,  94000,  4079500]
    q = [20,    15,     8,      9,      11,     10,     7,      11,     6,      5,      1]
    r = [100,   100,    100,    10,     10,     100,    100,    10,     100,    100,    1]

    infinity = solver.infinity()
    for i in range(0, n) :
        s.append(solver.IntVar(0.0, infinity, 's{i}'))

    solver.Add( p[0]*s[0]*r[0] +
                p[1]*s[1]*r[1] +
                p[2]*s[2]*r[2] +
                p[3]*s[3]*r[3] +
                p[4]*s[4]*r[4] +
                p[5]*s[5]*r[5] +
                p[6]*s[6]*r[6] +
                p[7]*s[7]*r[7] +
                p[8]*s[8]*r[8] +
                p[9]*s[9]*r[9] +
                p[10]*s[10]*r[10] == 600000000)

    solver.Maximize(p[0]*s[0]*r[0] +
                    p[1]*s[1]*r[1] +
                    p[2]*s[2]*r[2] +
                    p[3]*s[3]*r[3] +        
                    p[4]*s[4]*r[4] +
                    p[5]*s[5]*r[5] +
                    p[6]*s[6]*r[6] +
                    p[7]*s[7]*r[7] +
                    p[8]*s[8]*r[8] +
                    p[9]*s[9]*r[9] +
                    p[10]*s[10]*r[10])

    upperbound = [36,       22,         13,     18,     1000,       14,        1000,       16,      1000,     8,     1000]
    lowerbound = [0,        0,          13,     18,     20,       14,        14,       16,          11,         0,      0]

    for l in range(0, 1000):
        for i in range(0, n):
            solver.Add(s[i] >= lowerbound[i])
            solver.Add(s[i] <= upperbound[i])

        status = solver.Solve()
    
        if status == pywraplp.Solver.OPTIMAL:
            ratio = []
            for i in range(0, n): 
                ratio.append(s[i].solution_value() / q[i])

            average = 0
            for i in range(0, n):
                average += ratio[i]
            average = average / n;

            max = 0
            idx = 0
            for i in range(0, n): 
                if (abs(ratio[i] - average)) >= max :
                    max = abs(ratio[i] - average)
                    idx = i

            if(ratio[idx] > average) :
                upperbound[idx] = s[idx].solution_value() - 1 
            else :
                lowerbound[idx] = s[idx].solution_value() + 1

            f.write(str(s[0].solution_value())+ ' ' + str(s[1].solution_value()) + ' ' + str(s[2].solution_value())+ ' ' + str(s[3].solution_value()) + ' ' + str(s[4].solution_value()) + ' ' + str(s[5].solution_value()) + ' ' + str(s[6].solution_value()) + ' ' + str(s[7].solution_value()) +' ' + str(s[8].solution_value()) + ' ' + str(s[9].solution_value()) + ' ' + str(s[10].solution_value()) + '\n' )

        else:
            print('The problem does not have an optimal solution.')
            break
    
    print(round(time.time() * 1000) - start)

if __name__ == '__main__':
    main()