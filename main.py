import numpy as np

from step_1_ocr_vision.capture_grid import capture_screen_and_get_grid
from step_2_solver.sudoku_solver import solve_sudoku
from step_3_automation.type_solution import auto_fill_solution


def print_board(matrix: np.ndarray) -> None:
    """Helper to cleanly display a 6x6 Sudoku matrix in the terminal."""
    for row_idx, row in enumerate(matrix):
        if row_idx > 0 and row_idx % 2 == 0:
            print("-" * 23)  # Horizontal block separator for 2x3 subgrids

        formatted_row = []
        for col_idx, val in enumerate(row):
            if col_idx > 0 and col_idx % 3 == 0:
                formatted_row.append("|")  # Vertical block separator
            formatted_row.append(str(val) if val != 0 else ".")

        print(" ".join(formatted_row))


def main():
    print("==========================================")
    print("      LinkedIn Mini-Sudoku Auto-Bot       ")
    print("==========================================")

    # 1. Capture live puzzle from screen using Step 1
    print("\n[Step 1] Capturing grid from screen...")
    initial_grid = capture_screen_and_get_grid(delay_seconds=3)

    print("\nParsed Board (From Screen):")
    print_board(initial_grid)

    # 2. Make a copy and solve using Step 2
    solved_grid = initial_grid.copy()
    print("\n[Step 2] Solving puzzle...")

    if not solve_sudoku(solved_grid):
        print("\n❌ No valid solution could be found for the detected board.")
        return  

    print("\n SOLUTION FOUND!")
    print_board(solved_grid)

    # 3. Auto-type digits using Step 3
    print("\n[Step 3] Auto-typing solution onto screen...")
    auto_fill_solution(initial_grid, solved_grid, delay=0.20)

    print("\n==========================================")
    print("   Mini-Sudoku Fully Solved!   ")
    print("==========================================")


if __name__ == "__main__":
    main()