# This script is designed to generate a list of spreadsheet function parameters using OCR on tooltips.
#
# This script probably doesn't work on any OS other than Windows.
# 
# This script will probably work for any spreadsheet application with a function tooltip given the correct key sequence is used.
# 
# To stop execution, press BACKSPACE.
# 
# Run this script in an empty directory as it writes to and overwrites files with the following names:
#   `out.txt`
#   `err.txt`
#   `test.png`
# 
# For good measure, turn off 'View Gridlines'.
# 
# Try initial execution on a short list or keep an eye on the console.
# 
# Check the generated "test.png" file to make sure the tooltip is captured in full.
# 
# For configuration, see variables:
#   `tesseract_cmd`
#   `func_file`
#   `app_name`
#   `slp`
#   `snapshot`

import time as t
import win32com.client as comclt
from PIL import Image, ImageGrab
import pytesseract
import keyboard
import threading

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# File containing function names to be looped through.
func_file = "excel_funcs.txt"

# Name of the application to be interacted with.
app_name = "ExcelTooltipper.xlsx - Excel"

# Read function names from file
with open(func_file, "r") as file:
    func_list = [line.strip() for line in file]

# Open output and error files
o = open("out.txt", "w")
e = open("err.txt", "w")

# Sleep duration. 0.1 found to be reliable on a very fast computer (by 2025 standards).
# Erratic script behavior and frequent blank OCR readings may indicate that this number needs to be increased to match system performance.
slp = 0.1

# Activate application
wsh = comclt.Dispatch("WScript.Shell")
wsh.AppActivate(app_name)
t.sleep(slp)

# Global flag for stopping execution
stop_flag = False

def listen_for_stop():
    """Listens for Backspace key press to stop execution."""
    global stop_flag
    keyboard.wait("backspace")  # Blocks until Backspace is pressed
    stop_flag = True
    print("\n[INFO] Backspace pressed. Stopping execution...")

# Start the keyboard listener in a separate thread
threading.Thread(target=listen_for_stop, daemon=True).start()

# Main execution loop
for func_str in func_list:
    if stop_flag:
        break  # Stop execution when Backspace is pressed
    
    # Initialize cursor and cell state.
    wsh.SendKeys("{ESC}")
    wsh.SendKeys("^{HOME}")
    # Trigger function completion menu.
    wsh.SendKeys("=")
    wsh.SendKeys(func_str[0])
    t.sleep(slp)
    # Complete rest of function name.
    wsh.SendKeys(func_str[1:len(func_str)])
    t.sleep(slp)
    # Trigger tooltip with `(`, then send SPACE to close any sub tooltips (like those seen with `CELL(`)
    wsh.SendKeys("+9 ")
    t.sleep(slp)

    # Capture screen and process text.
    # Set this to match position of the tooltip on primary monitor in a spreadsheet on cell A1. Set right horizontal bound to go to edge of spreadsheet.
    # UI scale correlates with OCR reliability.
    snapshot = ImageGrab.grab(bbox=(110, 650, 2500, 685))
    out = pytesseract.image_to_string(snapshot).strip()
    
    if len(out) == 0:
        print("ERROR:", func_str)
        e.write(func_str + "\n")
    else:
        print(func_str + "~" + out)
        o.write(func_str + "~" + out + "\n")

# Cleanup
e.close()
o.close()
snapshot.save("test.png")
print("[INFO] Script execution completed.")
