# Sudoku-Solver

This sudoku solver is written with the backtracking search algorithm and has several versions with different heuristics. To run a file, use the command `file.py, ./path/to/init_state.txt ./output/output.txt`.

The different versions are:
* Backtracking search
* Backtracking search + Most Constrained Variable
* Backtracking search + AC3
* Backtracking search + Most Constrained Variable + AC3
* Backtracking search + Most Constrained Variable + AC3 + Tie Breaker
* Backtracking search + Most Constrained Variable + AC3 + Tie Breaker with a variation that runs AC3 only every 10 iterations. (fastest)
