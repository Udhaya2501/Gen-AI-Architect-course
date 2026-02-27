import pyautogui
import time

time.sleep(3)  # time to prepare

# 1️⃣ Press Windows key
pyautogui.press("win")
time.sleep(1)

# 2️⃣ Type "updates"
pyautogui.write("updates", interval=0.05)
time.sleep(1)

# 3️⃣ Press Enter (opens first result)
pyautogui.press("enter")
time.sleep(4)  # wait for window to open

# 4️⃣ Press Enter again (to trigger Check for updates)
pyautogui.press("enter")