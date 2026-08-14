import numpy as np

def is_valid(grid: np.ndarray, row: int, col: int, num: int) -> bool:
    """
    Check if placing `num` at grid[row][col] is valid under 6x6 Mini-Sudoku rules:
    - Unique in the row (1-6)
    - Unique in the column (1-6)
    - Unique in the 2x3 block
    """
    # 1. Check Row & Column
    if num in grid[row, :] or num in grid[:, col]:
        return False

    # 2. Check 2x3 Sub-grid
    # Block rows span 2 cells (0-1, 2-3, 4-5) -> (row // 2) * 2
    # Block cols span 3 cells (0-2, 3-5)      -> (col // 3) * 3
    start_row = (row // 2) * 2
    start_col = (col // 3) * 3

    sub_grid = grid[start_row : start_row + 2, start_col : start_col + 3]
    if num in sub_grid:
        return False

    return True


def solve_sudoku(grid: np.ndarray) -> bool:
    """
    Solves a 6x6 Mini-Sudoku grid in-place using Backtracking.
    Unfilled cells are represented by 0.

    Returns:
        True if the puzzle was solved, False if unsolvable.
    """
    # Find the next empty cell (value == 0)
    empty_pos = np.argwhere(grid == 0)
    if len(empty_pos) == 0:
        return True  # Puzzle completely solved!

    row, col = empty_pos[0]

    for num in range(1, 7):
        if is_valid(grid, row, col, num):
            grid[row, col] = num  # Tentatively place candidate

            if solve_sudoku(grid):
                return True

            grid[row, col] = 0  # Backtrack

    return False