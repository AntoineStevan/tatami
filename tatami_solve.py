import sys
import facile
import numpy as np
import matplotlib.pyplot as plt


def tatami_solve(xmax: int, ymax: int):# -> list[facile.Solution]:
    n = xmax * ymax // 2

    # 1. variables definition.
    # origin is at in bottom left corner.
    x = [facile.variable(0, xmax-1) for _ in range(n)]
    y = [facile.variable(0, ymax-1) for _ in range(n)]
    d = [facile.variable(1, 2) for _ in range(n)]  # 1: vertical, 2: horizontal.

    # 2. auxiliary variables.
    auxs = np.empty(shape=(n,2), dtype=facile.core.Variable)
    for i in range(n):
        auxs[i,0] = x[i] + d[i]
        auxs[i,1] = y[i] + 3 - d[i]

    # 3. no tile outside the box.
    for i in range(n):
        facile.constraint(auxs[i,0] <= xmax)
        facile.constraint(auxs[i,1] <= ymax)

    # 4. no overlap.
    for i in range(n-1):
        for j in range(i+1, n):
            left = x[j] >= auxs[i,0]
            right= auxs[j,0] <= x[i]
            below = auxs[j,1] <= y[i]
            above = y[j] >= auxs[i,1]
            facile.constraint(left | right | above | below)

    # 5. lexicographic ordering.
    for i in range(n-1):
        facile.constraint(x[i] <= x[i+1])
        facile.constraint(
                (x[i] != x[i+1]) |
                (y[i] < y[i+1])
                )

    # 6. no 4 tiles at same corner.
    for i in range(n):
        for j in range(i+1, n):
            facile.constraint(
                    (auxs[i,0] != x[j]) |
                    (auxs[i,1] != y[j])
                    )

    # 7. first diagonal symmetry.
    if xmax == ymax:
        facile.constraint(d[0] == 1)

#    # 8. search goals to guide the resolution.
#    gx = facile.Goal.forall(x, assign="assign")
#    gy = facile.Goal.forall(y, assign="assign")
#    gy = facile.Goal.forall(y, assign="assign")
#    return facile.solve(gx & gy & gd)

    return facile.solve_all(x+y+d, backtrack=True)


def pretty_grid(sol, xmax, ymax):
    if sol is None:
        return

    n = len(sol) // 3
    x = sol[:n]
    y = sol[n : 2 * n]
    xs = sol[2 * n :]

    fig, ax = plt.subplots()

    for (xi, yi, xsi) in zip(x, y, xs):
        ysi = 3 - xsi
        ax.fill([xi, xi, xi + xsi, xi + xsi], [yi, yi + ysi, yi + ysi, yi])

    ax.set_xlim((0, xmax))
    ax.set_ylim((0, ymax))
    ax.set_aspect(1)
    ax.set_xticks(range(xmax + 1))
    ax.set_yticks(range(ymax + 1))

    plt.show()


if __name__ == "__main__":
    if len(sys.argv[1:]) not in [0, 2]:
        print("you should give exactly 2 or no integer arguments... Aborting!")
        exit()

    xmax, ymax = (4, 3) if len(sys.argv[1:]) == 0 else map(int, sys.argv[1:])

    sols = tatami_solve(xmax, ymax)
    print("nb solutions:", len(sols) -1)
    print(sols[-1])
    for sol in sols:
        pretty_grid(sol.solution, xmax, ymax)

