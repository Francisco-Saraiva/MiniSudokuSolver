# Automated 6x6 Mini-Sudoku Solver

An end-to-end Python automation script that captures, solves, and types solutions for 6x6 Mini-Sudoku games (such as those found on LinkedIn Games) in real time.

---

## How Mini-Sudoku Works
Unlike standard 9x9 Sudoku:
* The board is a **6x6 grid**.
* Numbers range from **1 to 6**.
* Sub-grids are **2x3 rectangles** (2 rows, 3 columns).

---

## Project Architecture

The project is structured into three modular components:

```text
mini_sudoku_project/
├── boards/                  # Sample screenshots/excel sheets of boards for testing
├── step1_ocr_vision/        # Screen capture & image parsing (CV/OCR)
│   ├── __init__.py
│   ├── capture_grid.py     # Grid extraction & OCR functions
│   └── test_ocr_vision.py   # Standalone test script for Step 1
├── step2_solver/            # 6x6 Backtracking solver logic
│   ├── __init__.py
│   ├── sudoku_solver.py     # Pure solver functions
│   └── test_solver.py       # Standalone test script for Step 2
├── step3_automation/        # Keyboard & mouse simulation
│   ├── __init__.py
│   ├── type_solution.py     # Automation logic (pyautogui)
│   └── test_solution.py     # Standalone test script for Step 3
├── main.py                  # Pipeline coordinator
└── README.md                # Project documentation
