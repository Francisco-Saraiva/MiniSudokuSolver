import os
import sys
import numpy as np

# Import live screen capture function
from capture_grid import capture_screen_and_get_grid


def run_test():
    print("========================================")
    print("   Running Step 1 Standalone Vision Test")
    print("========================================")

    # Automatically locate project root relative to this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print("Preparing live screen capture...\n")

    # Capture live board from screen with a 3-second delay
    parsed_grid = capture_screen_and_get_grid(delay_seconds=3)

    print("Extracted Grid Matrix (Step 1 Output):")
    print(parsed_grid)
    print("\n✅ Step 1 test complete.")


if __name__ == "__main__":
    run_test()