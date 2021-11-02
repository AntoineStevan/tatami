import sys
import facile


def tatami_solve(xmax: int, ymax: int):# -> list[facile.Solution]:
    return facile.solve_all([], backtrack=True)


if __name__ == "__main__":
    if len(sys.argv[1:]) not in [0, 2]:
        print("you should give exactly 2 or no integer arguments... Aborting!")
        exit()

    xmax, ymax = (4, 3) if len(sys.argv[1:]) == 0 else map(int, sys.argv[1:])

    tatami_solve(xmax, ymax)

