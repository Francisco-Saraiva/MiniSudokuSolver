import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageGrab


def find_and_crop_board(img: np.ndarray) -> np.ndarray:
    """Detects the main square Sudoku grid inside a full-screen image and crops it."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    
    # Threshold to isolate high-contrast lines/borders
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
        if area > 20000:  # Ignore small UI elements
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            
            # Find a 4-sided polygon with maximum square area
            if len(approx) == 4 and area > max_area:
                largest_square = approx
                max_area = area

    if largest_square is not None:
        x, y, w, h = cv2.boundingRect(largest_square)
        return gray[y : y + h, x : x + w]

    # Fallback: return grayscale image as-is if no clear outer grid contour found
    return gray


def capture_screen_and_get_grid(delay_seconds: int = 3) -> np.ndarray:
    """Gives you time to switch windows, takes a screenshot, crops the board, and returns the 6x6 matrix."""
    print(
        f"\n[!] Starting countdown... Switch to your Sudoku browser window now!"
    )

    # Countdown loop
    for i in range(delay_seconds, 0, -1):
        print(f"    Capturing screen in {i}...")
        time.sleep(1)

    print("[*] Capturing screen now!\n")

    # Capture main screen
    screenshot = ImageGrab.grab()
    screen_np = np.array(screenshot)
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

    # Auto-detect, crop, and parse
    cropped_board = find_and_crop_board(screen_bgr)
    cell_matrix = extract_cell_images(cropped_board, grid_size=6)

    grid = np.zeros((6, 6), dtype=int)
    for r in range(6):
        for c in range(6):
            grid[r, c] = recognize_digit(cell_matrix[r][c])

    return grid


def render_font_variations(size: int = 40) -> dict[int, list[np.ndarray]]:
    """Renders reference digit templates across multiple font styles and weights."""
    font_names = [
        "arial.ttf",
        "times.ttf",
        "cour.ttf",
        "trebuc.ttf",
        "verdana.ttf",
    ]
    templates = {d: [] for d in range(1, 7)}

    for digit in range(1, 7):
        text = str(digit)
        for font_name in font_names:
            try:
                font = ImageFont.truetype(font_name, 28)
            except OSError:
                font = ImageFont.load_default()

            img = Image.new("L", (size, size), color=0)
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = (size - w) // 2
            y = (size - h) // 2

            draw.text((x, y), text, fill=255, font=font)
            arr = np.array(img)

            # Crop tightly to the rendered digit body then pad back to a square
            contours, _ = cv2.findContours(
                arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if contours:
                c = max(contours, key=cv2.contourArea)
                bx, by, bw, bh = cv2.boundingRect(c)
                cropped = arr[by : by + bh, bx : bx + bw]

                # Preserve aspect ratio on a square canvas
                max_dim = max(bw, bh)
                sq = np.zeros((max_dim, max_dim), dtype=np.uint8)
                sq[
                    (max_dim - bh) // 2 : (max_dim - bh) // 2 + bh,
                    (max_dim - bw) // 2 : (max_dim - bw) // 2 + bw,
                ] = cropped
                resized = cv2.resize(sq, (size, size))
                templates[digit].append(resized)

    return templates


# Generate multi-font template dictionary once at import
MULTI_TEMPLATES = render_font_variations()


def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """Loads an image and converts it to grayscale."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at path: {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def extract_cell_images(
    grid_img: np.ndarray, grid_size: int = 6
) -> list[list[np.ndarray]]:
    """Splits a cropped grid image into a 6x6 matrix of individual cell images."""
    height, width = grid_img.shape
    cell_h = height // grid_size
    cell_w = width // grid_size

    cells = []
    for r in range(grid_size):
        row_cells = []
        for c in range(grid_size):
            y1, y2 = r * cell_h, (r + 1) * cell_h
            x1, x2 = c * cell_w, (c + 1) * cell_w

            # 14% padding strips grid border lines cleanly
            margin_y = int(cell_h * 0.14)
            margin_x = int(cell_w * 0.14)

            cell = grid_img[
                y1 + margin_y : y2 - margin_y, x1 + margin_x : x2 - margin_x
            ]
            row_cells.append(cell)
        cells.append(row_cells)

    return cells


def pad_to_square(roi: np.ndarray, target_size: int = 40) -> np.ndarray:
    """Pads a cropped digit with black background to preserve original aspect ratio."""
    h, w = roi.shape
    max_dim = max(h, w)

    square = np.zeros((max_dim, max_dim), dtype=np.uint8)
    y_offset = (max_dim - h) // 2
    x_offset = (max_dim - w) // 2
    square[y_offset : y_offset + h, x_offset : x_offset + w] = roi

    return cv2.resize(square, (target_size, target_size))


def recognize_digit(cell_img: np.ndarray) -> int:
    """Matches a cell image against multi-font templates using normalized correlation."""
    _, thresh = cv2.threshold(
        cell_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    non_zero = cv2.countNonZero(thresh)
    total_pixels = thresh.shape[0] * thresh.shape[1]
    if non_zero / total_pixels < 0.015:
        return 0

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return 0

    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 15:
        return 0

    x, y, w, h = cv2.boundingRect(c)
    digit_roi = thresh[y : y + h, x : x + w]

    padded_digit = pad_to_square(digit_roi, target_size=40)

    best_match = 0
    highest_score = -1.0

    for digit, font_variants in MULTI_TEMPLATES.items():
        for template in font_variants:
            res = cv2.matchTemplate(
                padded_digit, template, cv2.TM_CCOEFF_NORMED
            )
            _, max_val, _, _ = cv2.minMaxLoc(res)

            if max_val > highest_score:
                highest_score = max_val
                best_match = digit

    return best_match


def image_to_grid(image_path: str) -> np.ndarray:
    """Main pipeline: Cropped Image Path -> 6x6 Matrix."""
    gray_img = load_and_preprocess_image(image_path)
    cell_matrix = extract_cell_images(gray_img, grid_size=6)

    grid = np.zeros((6, 6), dtype=int)
    for r in range(6):
        for c in range(6):
            grid[r, c] = recognize_digit(cell_matrix[r][c])

    return grid