import cv2
import numpy as np
import pandas as pd
import pyautogui
import mss
import time
from datetime import datetime

# Global variables for storing region and drawing status
region = {}          # Final selected region, as a dict with keys "top", "left", "width", "height"
drawing = False      # Flag: are we actively drawing?
ix, iy = -1, -1      # Initial mouse click coordinates
temp_rect = None     # Temporary rectangle during dragging
current_img = None   # Latest screenshot image for display

def draw_rectangle(event, x, y, flags, param):
    """
    Mouse callback that records the initial click and updates a temporary rectangle.
    It does NOT call any GUI functions (like imshow) so that all such calls run in the main thread.
    """
    global ix, iy, drawing, region, temp_rect
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        temp_rect = None  # Reset previous temporary value
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        # Update temporary rectangle coordinates
        temp_rect = (min(ix, x), min(iy, y), abs(x - ix), abs(y - iy))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # On release, finalize the selected region
        region = {
            "top": min(iy, y),
            "left": min(ix, x),
            "width": abs(x - ix),
            "height": abs(y - iy)
        }
        # Clear temporary rectangle once a region is set
        temp_rect = None

def get_screen_region():
    """
    Takes one screenshot and allows the user to select a region by dragging the mouse.
    All GUI calls occur in this main loop, thereby avoiding cross-thread Qt calls.
    """
    global current_img, temp_rect, region
    with mss.mss() as sct:
        # Grab a screenshot from the first monitor
        screen = np.array(sct.grab(sct.monitors[1]))
        # Convert from BGRA to BGR
        current_img = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        cv2.namedWindow("Draw Region")
        cv2.setMouseCallback("Draw Region", draw_rectangle, param=current_img)

        # Main loop: update window continuously until a region is selected or "q" is pressed.
        while not region:
            display_img = current_img.copy()
            if temp_rect is not None:
                (x, y, w, h) = temp_rect
                cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Draw Region", display_img)
            key = cv2.waitKey(1) & 0xFF
            # Exit if user presses 'q' (or 'Q')
            if key in (ord('q'), ord('Q')):
                break

        cv2.destroyWindow("Draw Region")

def start_capture():
    """
    Main function that first allows the user to select a region from the screen,
    then continuously captures that region, processes it, clicks on edge points,
    and saves the output as both a video and CSV of click coordinates.
    """
    get_screen_region()
    if not region:
        print("No region selected. Exiting.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"screen_capture_{timestamp}.avi"
    csv_filename = f"click_coordinates_{timestamp}.csv"

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(video_filename, fourcc, 10, (region["width"], region["height"]))
    coords = []

    print("Starting live capture... Press Ctrl+C or 'q' to stop.")
    try:
        with mss.mss() as sct:
            while True:
                # Grab the selected region
                frame = np.array(sct.grab(region))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                inverted = cv2.bitwise_not(gray)
                edges = cv2.Canny(inverted, 50, 150)

                # Get edge points: select a subset for clicking
                points = np.column_stack(np.where(edges > 0))
                step = max(1, len(points) // 50)
                for y, x in points[::step]:
                    screen_x = region["left"] + x
                    screen_y = region["top"] + y
                    pyautogui.click(x=screen_x, y=screen_y)
                    coords.append((screen_x, screen_y))
                    time.sleep(0.01)

                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                video_writer.write(frame_bgr)

                # Display edge preview in the main thread
                cv2.imshow("Edges", edges)
                key = cv2.waitKey(1) & 0xFF
                # Exit loop if 'q' (or 'Q') is pressed
                if key in (ord('q'), ord('Q')):
                    break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        video_writer.release()
        cv2.destroyAllWindows()
        pd.DataFrame(coords, columns=["x", "y"]).to_csv(csv_filename, index=False)
        print(f"Video saved to: {video_filename}")
        print(f"Click coordinates saved to: {csv_filename}")

if __name__ == "__main__":
    start_capture()

