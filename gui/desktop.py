import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import datetime

class HybridDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LinDOS Prime Desktop")
        self.attributes('-fullscreen', True)
        
        self.theme = {
            "bg": "#1e1e2e", "top": "#11111b", "task": "#181825", 
            "accent": "#89b4fa", "card": "#313244", "fg": "#cdd6f4"
        }
        self.configure(bg=self.theme["bg"])
        
        self.create_top_bar()
        self.create_desktop_workspace()
        self.create_bottom_taskbar()
        self.update_clock_and_stats()

    def create_top_bar(self):
        self.top_bar = tk.Frame(self, bg=self.theme["top"], height=30)
        self.top_bar.pack(side="top", fill="x")
        self.title_lbl = tk.Label(self.top_bar, text=" ❖ LinDOS Prime", fg=self.theme["fg"], bg=self.theme["top"], font=("Segoe UI", 10, "bold"))
        self.title_lbl.pack(side="left", padx=10)
        self.stats_label = tk.Label(self.top_bar, text="RAM: Active", fg=self.theme["accent"], bg=self.theme["top"], font=("Segoe UI", 9))
        self.stats_label.pack(side="left", padx=20)
        self.clock_label = tk.Label(self.top_bar, text="", fg=self.theme["fg"], bg=self.theme["top"], font=("Segoe UI", 10))
        self.clock_label.pack(side="right", padx=15)

    def update_clock_and_stats(self):
        now = datetime.datetime.now().strftime("%I:%M:%S %p | %b %d, %Y")
        self.clock_label.config(text=now)
        try:
            mem_info = subprocess.getoutput("free -m | grep Mem").split()
            if len(mem_info) >= 3:
                self.stats_label.config(text=f"RAM: {mem_info[2]}MB / {mem_info[1]}MB")
        except Exception:
            pass
        self.after(1000, self.update_clock_and_stats)

    def create_desktop_workspace(self):
        self.workspace = tk.Frame(self, bg=self.theme["bg"])
        self.workspace.pack(side="top", fill="both", expand=True)
        
        shortcuts = [
            ("💻", "Terminal", lambda: self.open_window("Terminal")),
            ("📁", "Files", lambda: self.open_window("Files")),
            ("🎮", "Games", lambda: self.open_window("Games")),
            ("⚙", "Settings", lambda: self.open_window("Settings"))
        ]
        
        col = 0
        for icon, name, cmd in shortcuts:
            frame = tk.Frame(self.workspace, bg=self.theme["bg"], width=90, height=90)
            frame.grid(row=0, column=col, padx=25, pady=25, sticky="nw")
            tk.Button(frame, text=icon, font=("Segoe UI", 26), bg=self.theme["card"], fg=self.theme["accent"], bd=0, command=cmd).pack(ipadx=10, ipady=5)
            tk.Label(frame, text=name, bg=self.theme["bg"], fg=self.theme["fg"], font=("Segoe UI", 9, "bold")).pack(pady=4)
            col += 1

    def open_window(self, title):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("550x380+120+120")
        win.configure(bg=self.theme["bg"])
        tk.Label(win, text=f"LinDOS {title} Environment Active", fg=self.theme["fg"], bg=self.theme["bg"], font=("Segoe UI", 12, "bold")).pack(expand=True)

    def create_bottom_taskbar(self):
        self.taskbar = tk.Frame(self, bg=self.theme["task"], height=48)
        self.taskbar.pack(side="bottom", fill="x")
        tk.Button(self.taskbar, text=" ❖ Exit Desktop ", bg=self.theme["accent"], fg="#11111b", font=("Segoe UI", 10, "bold"), bd=0, command=self.quit).pack(side="left", padx=12, pady=6)

if __name__ == "__main__":
    app = HybridDesktop()
    app.mainloop()
