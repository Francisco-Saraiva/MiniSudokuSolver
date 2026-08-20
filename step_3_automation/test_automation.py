import os
import sys
import time
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from type_solution import auto_fill_solution


def run_typer_test():
    print("========================================")
    print("   Running Step 3 Standalone Typer Test ")
    print("========================================")
    
    # Initial state matching your exact Excel grid setup
    initial_grid = np.array([
        [1, 0, 0, 2, 0, 3],
        [0, 0, 2, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 6, 0, 0],
        [0, 0, 0, 3, 0, 0],
        [5, 0, 4, 0, 0, 2]
    ])

    # Complete solution matrix
    solved_grid = np.array([
        [1, 4, 5, 2, 6, 3],
        [3, 6, 2, 5, 1, 4],
        [6, 3, 1, 4, 2, 5],
        [4, 2, 3, 6, 5, 1],
        [2, 5, 6, 3, 4, 1],
        [5, 1, 4, 1, 3, 2]
    ])

    print("\n[!] Switch to your LinkedIn Sudoku browser window!")
    for i in range(3, 0, -1):
        print(f"    Starting auto-typer in {i}...")
        time.sleep(1)

    auto_fill_solution(initial_grid, solved_grid, delay=0.08)


if __name__ == "__main__":
    run_typer_test()