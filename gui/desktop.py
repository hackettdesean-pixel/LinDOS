import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import datetime
import random

class HybridDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("LinDOS Prime Desktop")
        self.attributes('-fullscreen', True)
        
        self.themes = {
            "Catppuccin": {"bg": "#1e1e2e", "top": "#11111b", "task": "#181825", "accent": "#89b4fa", "card": "#313244", "fg": "#cdd6f4"},
            "Cyberpunk": {"bg": "#0f051d", "top": "#05010d", "task": "#18092e", "accent": "#ff007f", "card": "#2a085c", "fg": "#00f0ff"},
            "Matrix Green": {"bg": "#000f08", "top": "#000503", "task": "#001a0e", "accent": "#00ff66", "card": "#00331c", "fg": "#80ffb3"},
            "Nord": {"bg": "#2e3440", "top": "#2e3440", "task": "#3b4252", "accent": "#88c0d0", "card": "#434c5e", "fg": "#eceff4"}
        }
        self.current_theme = self.themes["Catppuccin"]
        
        self.configure(bg=self.current_theme["bg"])
        self.start_menu_open = False
        self.current_dir = os.path.expanduser("~")
        self.terminal_cwd = os.path.expanduser("~")
        
        self.create_top_bar()
        self.create_desktop_workspace()
        self.create_bottom_taskbar()
        self.create_mac_dock()
        self.create_start_menu()
        
        self.update_clock_and_stats()

    def create_top_bar(self):
        self.top_bar = tk.Frame(self, bg=self.current_theme["top"], height=30)
        self.top_bar.pack(side="top", fill="x")
        
        self.title_lbl = tk.Label(self.top_bar, text=" ❖ LinDOS 3GB Prime", fg=self.current_theme["fg"], bg=self.current_theme["top"], font=("Segoe UI", 10, "bold"))
        self.title_lbl.pack(side="left", padx=10)
        
        self.stats_label = tk.Label(self.top_bar, text="RAM: Reading...", fg=self.current_theme["accent"], bg=self.current_theme["top"], font=("Segoe UI", 9))
        self.stats_label.pack(side="left", padx=20)
        
        self.clock_label = tk.Label(self.top_bar, text="", fg=self.current_theme["fg"], bg=self.current_theme["top"], font=("Segoe UI", 10))
        self.clock_label.pack(side="right", padx=15)

    def update_clock_and_stats(self):
        now = datetime.datetime.now().strftime("%I:%M:%S %p | %b %d, %Y")
        self.clock_label.config(text=now)
        
        try:
            mem_info = subprocess.getoutput("free -m | grep Mem").split()
            if len(mem_info) >= 3:
                used, total = mem_info[2], mem_info[1]
                self.stats_label.config(text=f"RAM: {used}MB / {total}MB")
        except Exception:
            self.stats_label.config(text="RAM: Active")
            
        self.after(1000, self.update_clock_and_stats)

    def create_desktop_workspace(self):
        self.workspace = tk.Frame(self, bg=self.current_theme["bg"])
        self.workspace.pack(side="top", fill="both", expand=True)
        self.refresh_desktop_shortcuts()

    def refresh_desktop_shortcuts(self):
        for widget in self.workspace.winfo_children():
            widget.destroy()
            
        shortcuts = [
            ("💻", "Terminal", self.open_terminal),
            ("📁", "Files", self.open_file_manager),
            ("🎮", "Games", self.open_games_center),
            ("⚙", "Settings", self.open_settings),
            ("ℹ", "Sys Info", self.open_system_info)
        ]
        
        col = 0
        for icon, name, cmd in shortcuts:
            frame = tk.Frame(self.workspace, bg=self.current_theme["bg"], width=80, height=80)
            frame.grid(row=0, column=col, padx=20, pady=20)
            
            btn = tk.Button(frame, text=icon, font=("Segoe UI", 24), bg=self.current_theme["bg"], fg=self.current_theme["accent"], bd=0, activebackground=self.current_theme["card"], command=cmd)
            btn.pack()
            
            lbl = tk.Label(frame, text=name, bg=self.current_theme["bg"], fg=self.current_theme["fg"], font=("Segoe UI", 9))
            lbl.pack()
            col += 1

    def create_base_window(self, title, width=520, height=380):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(f"{width}x{height}+80+60")
        win.configure(bg=self.current_theme["bg"])
        win.overrideredirect(True)
        
        titlebar = tk.Frame(win, bg=self.current_theme["card"], height=30)
        titlebar.pack(fill="x", side="top")
        
        title_lbl = tk.Label(titlebar, text=f"  {title}", bg=self.current_theme["card"], fg=self.current_theme["fg"], font=("Segoe UI", 9, "bold"))
        title_lbl.pack(side="left", padx=5)
        
        close_btn = tk.Button(titlebar, text=" ✕ ", bg="#f38ba8", fg="#11111b", relief="flat", bd=0, command=win.destroy)
        close_btn.pack(side="right", padx=5, pady=2)
        
        def start_drag(event):
            win._drag_x = event.x
            win._drag_y = event.y
            
        def do_drag(event):
            x = win.winfo_x() + (event.x - win._drag_x)
            y = win.winfo_y() + (event.y - win._drag_y)
            win.geometry(f"+{x}+{y}")
            
        titlebar.bind("<Button-1>", start_drag)
        titlebar.bind("<B1-Motion>", do_drag)
        title_lbl.bind("<Button-1>", start_drag)
        title_lbl.bind("<B1-Motion>", do_drag)
        
        body = tk.Frame(win, bg=self.current_theme["bg"])
        body.pack(expand=True, fill="both")
        return win, body

    def open_terminal(self):
        win, body = self.create_base_window("Terminal - LinDOS Shell", 600, 380)
        
        output_area = tk.Text(body, bg="#05050a", fg="#a6e3a1", font=("Courier", 10), insertbackground="#cdd6f4", bd=0)
        output_area.pack(fill="both", expand=True, padx=5, pady=5)
        output_area.insert("end", f"LinDOS Interactive Shell v1.0\nCurrent Dir: {self.terminal_cwd}\nType Linux commands (ls, pwd, cd, uname, cat):\n" + "-"*55 + "\n")
        
        input_frame = tk.Frame(body, bg=self.current_theme["task"])
        input_frame.pack(fill="x", padx=5, pady=5)
        
        prompt_lbl = tk.Label(input_frame, text="root@lindos:~$ ", bg=self.current_theme["task"], fg=self.current_theme["accent"], font=("Courier", 10, "bold"))
        prompt_lbl.pack(side="left")
        
        entry = tk.Entry(input_frame, bg=self.current_theme["task"], fg=self.current_theme["fg"], font=("Courier", 10), insertbackground=self.current_theme["fg"], bd=0)
        entry.pack(side="left", fill="x", expand=True, ipady=3)
        entry.focus_set()
        
        def run_cmd(event=None):
            cmd = entry.get().strip()
            if not cmd:
                return
            entry.delete(0, "end")
            output_area.insert("end", f"\nroot@lindos:~$ {cmd}\n")
            
            if cmd == "clear":
                output_area.delete("1.0", "end")
                return
            elif cmd.startswith("cd "):
                target = cmd[3:].strip()
                try:
                    os.chdir(os.path.expanduser(target))
                    self.terminal_cwd = os.getcwd()
                    output_area.insert("end", f"Directory changed to: {self.terminal_cwd}\n")
                except Exception as e:
                    output_area.insert("end", f"cd error: {e}\n")
            else:
                try:
                    res = subprocess.getoutput(f"cd {self.terminal_cwd} && {cmd}")
                    output_area.insert("end", res + "\n")
                except Exception as e:
                    output_area.insert("end", f"Error: {e}\n")
                    
            output_area.see("end")
            
        entry.bind("<Return>", run_cmd)

    def open_file_manager(self):
        win, body = self.create_base_window("File Manager", 520, 380)
        
        path_var = tk.StringVar(value=self.current_dir)
        path_entry = tk.Entry(body, textvariable=path_var, bg=self.current_theme["card"], fg=self.current_theme["fg"], font=("Segoe UI", 9), bd=0)
        path_entry.pack(fill="x", padx=5, pady=5, ipady=3)
        
        listbox = tk.Listbox(body, bg="#11111b", fg=self.current_theme["fg"], selectbackground=self.current_theme["card"], selectforeground=self.current_theme["accent"], font=("Segoe UI", 10), bd=0)
        listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        def load_dir():
            listbox.delete(0, "end")
            listbox.insert("end", ".. (Up Parent Directory)")
            try:
                items = sorted(os.listdir(path_var.get()))
                for item in items:
                    full_path = os.path.join(path_var.get(), item)
                    prefix = "📁 " if os.path.isdir(full_path) else "📄 "
                    listbox.insert("end", f"{prefix}{item}")
            except Exception as e:
                listbox.insert("end", f"Error: {e}")
                
        def on_double_click(event):
            selection = listbox.curselection()
            if not selection:
                return
            item = listbox.get(selection[0])
            if item.startswith(".."):
                path_var.set(os.path.dirname(path_var.get()))
                load_dir()
            else:
                clean_name = item.replace("📁 ", "").replace("📄 ", "")
                target = os.path.join(path_var.get(), clean_name)
                if os.path.isdir(target):
                    path_var.set(target)
                    load_dir()
                elif os.path.isfile(target):
                    self.open_text_viewer(target)
                    
        listbox.bind("<Double-Button-1>", on_double_click)
        load_dir()

    def open_text_viewer(self, filepath):
        v_win, v_body = self.create_base_window(f"Viewer - {os.path.basename(filepath)}", 480, 320)
        text = tk.Text(v_body, bg="#11111b", fg=self.current_theme["fg"], font=("Courier", 9), bd=0)
        text.pack(fill="both", expand=True, padx=5, pady=5)
        try:
            with open(filepath, 'r') as f:
                text.insert("1.0", f.read(5000))
        except Exception as e:
            text.insert("1.0", f"Cannot preview file: {e}")

    def open_games_center(self):
        win, body = self.create_base_window("LinDOS Games - Retro Snake", 420, 440)
        
        score_lbl = tk.Label(body, text="Score: 0", bg=self.current_theme["bg"], fg=self.current_theme["accent"], font=("Segoe UI", 11, "bold"))
        score_lbl.pack(pady=2)
        
        canvas = tk.Canvas(body, bg="#000000", width=300, height=300, highlightthickness=0)
        canvas.pack()
        
        snake = [(60, 60), (40, 60), (20, 60)]
        direction = ["Right"]
        food = [140, 140]
        score = [0]
        game_running = [True]
        
        def spawn_food():
            food[0] = random.randint(0, 14) * 20
            food[1] = random.randint(0, 14) * 20

        def move_snake():
            if not game_running[0] or not win.winfo_exists():
                return
            
            head_x, head_y = snake[0]
            if direction[0] == "Up": head_y -= 20
            elif direction[0] == "Down": head_y += 20
            elif direction[0] == "Left": head_x -= 20
            elif direction[0] == "Right": head_x += 20
            
            if head_x < 0 or head_x >= 300 or head_y < 0 or head_y >= 300 or (head_x, head_y) in snake:
                game_running[0] = False
                canvas.create_text(150, 150, text="GAME OVER", fill="#f38ba8", font=("Segoe UI", 16, "bold"))
                return
            
            snake.insert(0, (head_x, head_y))
            
            if head_x == food[0] and head_y == food[1]:
                score[0] += 10
                score_lbl.config(text=f"Score: {score[0]}")
                spawn_food()
            else:
                snake.pop()
                
            canvas.delete("all")
            canvas.create_rectangle(food[0], food[1], food[0]+20, food[1]+20, fill="#a6e3a1", outline="")
            for sx, sy in snake:
                canvas.create_rectangle(sx, sy, sx+20, sy+20, fill=self.current_theme["accent"], outline="#11111b")
                
            win.after(150, move_snake)

        def change_dir(new_d):
            opps = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if new_d != opps.get(direction[0]):
                direction[0] = new_d

        dpad = tk.Frame(body, bg=self.current_theme["bg"])
        dpad.pack(pady=5)
        
        tk.Button(dpad, text="▲", bg=self.current_theme["card"], fg=self.current_theme["fg"], width=4, command=lambda: change_dir("Up")).grid(row=0, column=1)
        tk.Button(dpad, text="◀", bg=self.current_theme["card"], fg=self.current_theme["fg"], width=4, command=lambda: change_dir("Left")).grid(row=1, column=0)
        tk.Button(dpad, text="▶", bg=self.current_theme["card"], fg=self.current_theme["fg"], width=4, command=lambda: change_dir("Right")).grid(row=1, column=2)
        tk.Button(dpad, text="▼", bg=self.current_theme["card"], fg=self.current_theme["fg"], width=4, command=lambda: change_dir("Down")).grid(row=2, column=1)

        win.bind("<Up>", lambda e: change_dir("Up"))
        win.bind("<Down>", lambda e: change_dir("Down"))
        win.bind("<Left>", lambda e: change_dir("Left"))
        win.bind("<Right>", lambda e: change_dir("Right"))
        
        move_snake()

    def open_settings(self):
        win, body = self.create_base_window("System Settings", 450, 300)
        
        tk.Label(body, text="Select Theme Preset:", bg=self.current_theme["bg"], fg=self.current_theme["fg"], font=("Segoe UI", 11, "bold")).pack(pady=10)
        
        def apply_theme(name):
            self.current_theme = self.themes[name]
            self.configure(bg=self.current_theme["bg"])
            self.top_bar.configure(bg=self.current_theme["top"])
            self.title_lbl.configure(bg=self.current_theme["top"], fg=self.current_theme["fg"])
            self.stats_label.configure(bg=self.current_theme["top"], fg=self.current_theme["accent"])
            self.clock_label.configure(bg=self.current_theme["top"], fg=self.current_theme["fg"])
            self.taskbar.configure(bg=self.current_theme["task"])
            self.dock.configure(bg=self.current_theme["card"])
            self.refresh_desktop_shortcuts()
            win.destroy()
            
        for theme_name in self.themes:
            btn = tk.Button(body, text=f"🎨 Apply {theme_name}", bg=self.current_theme["card"], fg=self.current_theme["fg"], activebackground=self.current_theme["accent"], font=("Segoe UI", 10), bd=0, command=lambda t=theme_name: apply_theme(t))
            btn.pack(fill="x", padx=30, pady=5, ipady=4)

    def open_system_info(self):
        win, body = self.create_base_window("System Information", 460, 290)
        uname = subprocess.getoutput("uname -a")
        disk = subprocess.getoutput("df -h / | tail -n 1")
        
        info = (
            f"❖ LinDOS 3GB Prime Desktop\n"
            f"----------------------------------------\n"
            f"Kernel: {uname}\n\n"
            f"Storage: {disk}\n\n"
            f"GUI Framework: Tkinter Desktop Engine\n"
            f"Target Display: X11 / VNC Server :1"
        )
        
        lbl = tk.Label(body, text=info, bg=self.current_theme["bg"], fg=self.current_theme["fg"], font=("Segoe UI", 9), justify="left", wraplength=420)
        lbl.pack(fill="both", expand=True, padx=15, pady=15)

    def create_bottom_taskbar(self):
        self.taskbar = tk.Frame(self, bg=self.current_theme["task"], height=44)
        self.taskbar.pack(side="bottom", fill="x")
        
        start_btn = tk.Button(self.taskbar, text=" ❖ Start ", bg=self.current_theme["accent"], fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", bd=0, command=self.toggle_start_menu)
        start_btn.pack(side="left", padx=8, pady=5)

    def create_start_menu(self):
        self.start_menu = tk.Frame(self, bg=self.current_theme["task"], bd=1, relief="solid", highlightbackground=self.current_theme["card"], highlightthickness=1)
        header = tk.Label(self.start_menu, text="LinDOS Prime", bg=self.current_theme["card"], fg=self.current_theme["fg"], font=("Segoe UI", 10, "bold"), anchor="w", padx=10)
        header.pack(fill="x", pady=(0, 5))
        
        apps = [
            ("💻 Terminal", self.open_terminal),
            ("📁 File Manager", self.open_file_manager),
            ("🎮 Games Center", self.open_games_center),
            ("⚙ Settings", self.open_settings),
            ("ℹ System Info", self.open_system_info),
            ("🔴 Shutdown", self.quit)
        ]
        
        for name, cmd in apps:
            btn = tk.Button(
                self.start_menu, text=f"  {name}", bg=self.current_theme["task"], fg=self.current_theme["fg"], 
                activebackground=self.current_theme["card"], activeforeground=self.current_theme["accent"],
                font=("Segoe UI", 9), relief="flat", anchor="w", bd=0,
                command=lambda c=cmd: [c(), self.toggle_start_menu()]
            )
            btn.pack(fill="x", ipady=4)

    def toggle_start_menu(self):
        if self.start_menu_open:
            self.start_menu.place_forget()
            self.start_menu_open = False
        else:
            self.start_menu.place(x=8, y=self.winfo_height() - 280, width=220, height=230)
            self.start_menu.lift()
            self.start_menu_open = True

    def create_mac_dock(self):
        self.dock = tk.Frame(self, bg=self.current_theme["card"], height=50)
        self.dock.place(relx=0.5, rely=0.92, anchor="s", width=280, height=48)
        
        items = [
            ("💻", self.open_terminal),
            ("📁", self.open_file_manager),
            ("🎮", self.open_games_center),
            ("⚙", self.open_settings)
        ]
        
        for icon, cmd in items:
            btn = tk.Button(self.dock, text=icon, bg=self.current_theme["card"], fg=self.current_theme["fg"], activebackground=self.current_theme["accent"], font=("Segoe UI", 14), relief="flat", bd=0, command=cmd)
            btn.pack(side="left", expand=True, fill="both", padx=3, pady=3)

if __name__ == "__main__":
    app = HybridDesktop()
    app.mainloop()
