import time
import random
import cv2
import numpy as np
import pyautogui


def locate_board_on_screen() -> tuple[int, int, int, int] | None:
    """Captures the live screen and returns the bounding box (x, y, w, h) of the Sudoku grid."""
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    largest_square = None
    max_area = 0

    for c in contours:
        area = cv2.contourArea(c)
        if area > 20000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4 and area > max_area:
                largest_square = approx
                max_area = area

    if largest_square is not None:
        return cv2.boundingRect(largest_square)

    return None


def auto_fill_solution(
    initial_grid: np.ndarray, solved_grid: np.ndarray, delay: float = 0.08
) -> None:
    """Calculates center pixel coordinates for each missing cell and types the solution."""
    board_rect = locate_board_on_screen()
    if board_rect is None:
        print("❌ Error: Could not locate the grid on screen to type the solution.")
        return

    bx, by, bw, bh = board_rect
    cell_w = bw / 6.0
    cell_h = bh / 6.0

    print("\n[*] Locating grid and starting auto-typer...")
    pyautogui.PAUSE = delay

    for r in range(6):
        for c in range(6):
            # Only fill empty cells (where initial state was 0)
            if initial_grid[r, c] == 0:
                digit_to_type = solved_grid[r, c]

                # Center coordinates for cell (r, c)
                center_x = int(bx + (c + 0.5) * cell_w)
                center_y = int(by + (r + 0.5) * cell_h)

                pyautogui.click(center_x, center_y)
                time.sleep(random.uniform(0.12, 0.28))  # To Mimic human typing speed
                pyautogui.press(str(digit_to_type))

    print("Solution successfully typed into the puzzle!")