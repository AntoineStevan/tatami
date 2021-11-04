# tatami
Constraint programming projet for the SDD class in Supaero.

# 1. Requirements.
Follow the steps, based on your setup, to install all needed python packages [here](https://www.xoolive.org/constraints/).

# 2. Run the code.
To run the code as main code, run
```python
python tatami_solve.py <xmax> <ymax>
```
Notes:
- one should give exactly 2 arguments or none, otherwise the program aborts.
- for instance, to give a room size, write and execute `python tatami_solve.py 4 4`, for a square room of side 4.
- by default, i.e. when no arguments are given to `tatami_solve.py`, a room of size 4x3 is considered.

Otherwise, one can import the `tatami_solve` function from the `tatami_solve.py` file and use it as described above, i.e. by giving it `xmax` and `ymax` as arguments.
