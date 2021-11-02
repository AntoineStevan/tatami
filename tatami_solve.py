import sys
import facile
import numpy as np


def tatami_solve(xmax: int, ymax: int):# -> list[facile.Solution]:
    n = xmax * ymax // 2

    # 1.
    variables = facile.Array.variable((n, 4), 0, max(xmax, ymax))  # x, y, sx, sy
    for i in range(n):
        facile.constraint((variables[i,0] <= xmax) & (variables[i,1] <= ymax))
        facile.constraint((variables[i,2] == 1) | (variables[i,2] == 2))
        facile.constraint((variables[i,3] == 1) | (variables[i,3] == 2))
        facile.constraint(variables[i,2] + variables[i,3] == 3)

    # 2.
    auxs = facile.Array.variable((n, 2), 0, max(xmax, ymax))
    auxs = np.empty(shape=(n,2), dtype=facile.core.Variable)
    for i in range(n):
        auxs[i,0] = variables[i,0] + variables[i,2]
        auxs[i,1] = variables[i,1] - variables[i,3]

    # 3.
    for i in range(n):
        facile.constraint((auxs[i,0] >= 1) & (auxs[i,0] <= xmax))
        facile.constraint((auxs[i,1] >= 0) & (auxs[i,1] < ymax))

    # 4.
    for i in range(n):
        for j in range(i+1, n):
            facile.constraint(
                    (auxs[j,0] <= variables[i,0]) |
                    (variables[j,0] >= auxs[i,0]) |
                    (auxs[j,1] >= variables[i,1]) |
                    (variables[j,1] <= auxs[i,1])
                    )

    # 5.
#    for i in range(n-1):
#        facile.constraint((variables[i,0] < variables[i+1,0]) | (variables[i,1] < variables[i+1,1]))

    return facile.solve_all(variables, backtrack=True)

def grid(sol, xmax, ymax):
    if sol is None:
        return
    n = xmax * ymax // 2
    grid_ = np.empty(shape=(xmax, ymax), dtype=str)
    for i in range(xmax):
        for j in range(ymax):
            grid_[i,j] = '.'

    for i in range(n):
        x, y, sx, sy = sol[4*i:4*(i+1)]
        print(x, y, sx, sy, end=" - ")
        if sx == 1:
            grid_[y-1,x] = chr(i+97)
            grid_[y-2,x] = chr(i+97)
        else:
            grid_[y-1,x] = chr(i+97)
            grid_[y-1,x+1] = chr(i+97)
    print()

    msg = '\n'.join([' '.join(line) for line in grid_])
    print(msg)
    print('-'*2*xmax)


if __name__ == "__main__":
    if len(sys.argv[1:]) not in [0, 2]:
        print("you should give exactly 2 or no integer arguments... Aborting!")
        exit()

    xmax, ymax = (4, 3) if len(sys.argv[1:]) == 0 else map(int, sys.argv[1:])

    sols = tatami_solve(xmax, ymax)
    for sol in sols:
        grid(sol.solution, xmax, ymax)
    print("nb solutions:", len(sols) -1)

