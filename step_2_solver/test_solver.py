import time
import numpy as np
from sudoku_solver import solve_sudoku, is_valid


def solve_and_benchmark(board: np.ndarray, test_name: str):
    """Helper function to solve a board, time the execution, and print results."""
    print(f"\n--- {test_name} ---")
    print("Initial Board:")
    print(board)

    board_copy = board.copy()
    start_time = time.perf_counter()
    success = solve_sudoku(board_copy)
    end_time = time.perf_counter()

    elapsed_ms = (end_time - start_time) * 1000

    if success:
        print(f"\nSolved Board (Execution time: {elapsed_ms:.3f} ms):")
        print(board_copy)
        assert np.all(board_copy > 0), "Board still contains empty cells!"
        print("✅ Test Passed: Board solved successfully.")
    else:
        print("\n❌ Failed to find a solution!")


def run_tests():
    print("========================================")
    print("   Running Step 2 Standalone Tests")
    print("========================================")

    # Board 1
    test_board_1 = np.array(
        [
            [1, 0, 0,  2, 0, 3],
            [0, 0, 2,  0, 0, 0],
            [0, 0, 1,  0, 0, 0],
            [0, 0, 0,  6, 0, 0],
            [0, 0, 0,  3, 0, 0],
            [5, 0, 4,  0, 0, 2],
        ]
    )

    # Board 2
    test_board_2 = np.array(
        [
            [4, 0, 0,  0, 1, 0],
            [3, 0, 0,  2, 0, 0],
            [0, 6, 4,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 6],
            [0, 0, 1,  0, 0, 3],
        ]
    )

    # Run both tests
    solve_and_benchmark(test_board_1, "Test 1: Board 1")
    solve_and_benchmark(test_board_2, "Test 2: Board 2")


if __name__ == "__main__":
    run_tests()