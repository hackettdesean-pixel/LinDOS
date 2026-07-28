import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class LinDOSDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("LinDOS Prime Workspace")
        self.root.geometry("850x550")
        self.root.configure(bg="#0f111a")

        # Color Palette
        self.bg_color = "#0f111a"
        self.card_bg = "#1f2335"
        self.accent_color = "#7aa2f7"
        self.text_color = "#c0caf5"
        self.secondary_text = "#787c99"

        # Layout Construction
        self.create_top_bar()
        self.create_main_layout()

    def create_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.card_bg, height=45)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        title_label = tk.Label(
            top_bar, text=" LinDOS Prime  ", fg=self.accent_color, bg=self.card_bg, 
            font=("Segoe UI", 11, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=15)

        status_btn = tk.Button(
            top_bar, text="System Status", command=self.check_system, 
            bg=self.accent_color, fg="#1a1b26", font=("Segoe UI", 9, "bold"), 
            bd=0, padx=12, pady=4, activebackground="#89b4fa", cursor="hand2"
        )
        status_btn.pack(side=tk.RIGHT, padx=15)

    def create_main_layout(self):
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Welcome Header
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        welcome_lbl = tk.Label(
            header_frame, text="Control Center", fg=self.text_color, bg=self.bg_color, 
            font=("Segoe UI", 18, "bold")
        )
        welcome_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header_frame, text="Optimized performance interface for low-resource environments", 
            fg=self.secondary_text, bg=self.bg_color, font=("Segoe UI", 10)
        )
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # Application Grid Container
        grid_frame = tk.Frame(main_container, bg=self.bg_color)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        apps = [
            ("Terminal", "Access system shell", self.open_terminal),
            ("File Manager", "Browse system directories", self.open_file_manager),
            ("Run Optimizer", "Execute C++ hardware daemon", self.run_optimizer),
            ("Settings", "Configure environment", self.open_settings)
        ]

        for i, (name, desc, cmd) in enumerate(apps):
            row, col = divmod(i, 2)
            card = self.create_app_card(grid_frame, name, desc, cmd)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        grid_frame.rowconfigure(0, weight=1)
        grid_frame.rowconfigure(1, weight=1)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

    def create_app_card(self, parent, title, description, command):
        card = tk.Frame(parent, bg=self.card_bg, highlightbackground="#292e42", highlightthickness=1)
        card.pack_propagate(False)

        # Inner container for padding
        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_lbl = tk.Label(inner, text=title, fg=self.text_color, bg=self.card_bg, font=("Segoe UI", 12, "bold"))
        title_lbl.pack(anchor="w")

        desc_lbl = tk.Label(inner, text=description, fg=self.secondary_text, bg=self.card_bg, font=("Segoe UI", 9))
        desc_lbl.pack(anchor="w", pady=(4, 15))

        btn = tk.Button(
            inner, text="Launch", command=command, bg="#292e42", fg=self.accent_color, 
            font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=5, activebackground=self.accent_color, 
            activeforeground="#1a1b26", cursor="hand2"
        )
        btn.pack(anchor="w")

        return card

    def open_terminal(self):
        os.system("xterm &")

    def open_file_manager(self):
        os.system("pcmanfm &")

    def run_optimizer(self):
        try:
            result = subprocess.run(["./bin/lindos-optimizer"], capture_output=True, text=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            messagebox.showinfo("Optimizer Output", output)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_settings(self):
        messagebox.showinfo("Settings", "LinDOS Control Panel — Configured for low-resource performance.")

    def check_system(self):
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read(400)
            messagebox.showinfo("System & Memory Info", meminfo[:300])
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = LinDOSDesktop(root)
    root.mainloop()
