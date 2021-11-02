def tatami_solve(xmax: int, ymax: int) -> list[facile.Solution]:
        return facile.solve_all([], backtrack=True)


if __name__ == "__main__":
    tatami_solve(6, 6)
