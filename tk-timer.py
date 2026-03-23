#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""tk-timer.py for the simple yet powerful Pomodoro Technique for improving focus.

From https://medium.com/pythoneers/i-wrote-100-python-automation-scripts-these-11-changed-everything-431009f96d6b
The method created by Francesco Cirillo back in the late 1980s. The idea is to break your work into focused 25-minute sessions, separated by short, intentional breaks. Each session is called a “Pomodoro” — the Italian word for tomato — inspired by the quirky tomato-shaped timer Cirillo used while studying. This timer also locks my device automatically when the time is up, making sure I actually step away and recharge.

BEFORE RUNNING, on Terminal:
   # cd to a folder to receive
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate
   # tkinter is part of Python's standard library — it's not a PyPI package. So uv add tkinter is not needed.  requires Tcl/Tk.
   # On macOS (via Homebrew)
   brew install python-tk
   # On Ubuntu/Debian: sudo apt install python3-tk
   # On Fedora/RHEL:   sudo dnf install python3-tkinter

   ruff check tk-timer.py
   chmod +x tk-timer.py
   uv run tk-timer.py    # Terminal freezes.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__
"""
__last_change__ = "26-03-23 v001 new :tk-timer.py"
__status__ = "WORKS on macOS Sequoia 15.6.1"

import tkinter as tk
import ctypes
import os

class PomodoroTimer:
    """Class structure for timer."""

    def __init__(self, root):
        """Initialize all."""
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        self.time_var = tk.StringVar()
        self.time_var.set("25:00")
        self.running = False
        self.paused = False
        self.remaining_time = 25 * 60  # 25 minutes
        
        self.label = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 48))
        self.label.pack(pady=20)
        
        # Three buttons in the UI: Start, Pause, Reset
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=10)
    
    def update_time(self):
        """Update time."""
        if self.running:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.time_var.set(f"{minutes:02}:{seconds:02}")
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.update_time)
            else:
                self.running = False
                self.lock_screen()
    
    def start_timer(self):
        """Start timer."""
        if not self.running:
            self.running = True
            self.paused = False
            self.update_time()
    
    def pause_timer(self):
        """Pause timer."""
        if self.running:
            self.running = False
            self.paused = True
    
    def reset_timer(self):
        """Reset timer."""
        self.running = False
        self.paused = False
        self.remaining_time = 25 * 60
        self.time_var.set("25:00")
    
    def lock_screen(self):
        """Lock screen."""
        if os.name == 'nt':  # Windows
            ctypes.windll.user32.LockWorkStation()
        elif os.name == 'posix':  # macOS and Linux
            # This is a placeholder, as locking the screen in macOS/Linux typically requires different handling
            # For macOS, use: os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')
            # For Linux, use: os.system('gnome-screensaver-command --lock')
            print("Locking screen on macOS/Linux is not implemented in this script.")
    
if __name__ == "__main__":
    """Main caller."""

    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()