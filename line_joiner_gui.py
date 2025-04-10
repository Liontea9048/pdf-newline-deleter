import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import tkinter.font as tkfont
import threading
import time
import platform

class LineJoinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Joiner")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # App states
        self.is_auto_mode = True
        self.last_processed = ""
        self.is_dark_mode = self.detect_dark_mode()
        self.spinner_index = 0
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        # Font setup
        self.preferred_fonts = [
            "Noto Sans", "Open Sans", "Roboto", "Inter", "DejaVu Sans", "Arial"
        ]
        self.available_fonts = sorted(set(tkfont.families()))
        self.default_font = self.find_default_font()
        self.current_font = tk.StringVar(value=self.default_font)

        # Top frame (mode + settings)
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill=tk.X, pady=(10, 0), padx=10)

        # Mode toggle button
        self.mode_button = tk.Button(
            self.top_frame,
            text="AUTO MODE 🔄",
            font=(self.default_font, 12, "bold"),
            command=self.toggle_mode,
            bg="lightblue"
        )
        self.mode_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        # Dark mode toggle button
        self.theme_button = tk.Button(
            self.top_frame,
            text="Dark Mode 🌙" if not self.is_dark_mode else "Light Mode ☀️",
            font=(self.default_font, 12),
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.RIGHT)

        # Font dropdown
        self.font_frame = tk.Frame(root)
        self.font_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(self.font_frame, text="Font:").pack(side=tk.LEFT)
        self.font_dropdown = ttk.Combobox(
            self.font_frame, values=self.available_fonts,
            textvariable=self.current_font, state="readonly", width=30
        )
        self.font_dropdown.pack(side=tk.LEFT, padx=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.update_fonts)

        # Status + spinner frame
        self.status_frame = tk.Frame(root)
        self.status_frame.pack(pady=5)
        self.spinner_label = tk.Label(self.status_frame, text="", font=(self.default_font, 14))
        self.spinner_label.pack(side=tk.LEFT)
        self.status_label = tk.Label(self.status_frame, text="Waiting...", font=(self.default_font, 14))
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Input box (manual mode)
        self.input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=(self.default_font, 12))
        self.input_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Process button (manual mode)
        self.process_button = tk.Button(
            root, text="📋 Paste & Copy", command=self.manual_process, font=(self.default_font, 12, "bold")
        )
        self.process_button.pack(padx=10, pady=5, fill=tk.X)

        # Output box (manual mode)
        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=(self.default_font, 12), state="disabled")
        self.output_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.apply_mode()
        self.apply_theme()

        # Start clipboard watcher
        self.monitoring = True
        self.spinner_running = False
        self.clipboard_thread = threading.Thread(target=self.clipboard_watcher, daemon=True)
        self.clipboard_thread.start()

    def find_default_font(self):
        for font in self.preferred_fonts:
            if font in self.available_fonts:
                return font
        return "TkDefaultFont"

    def detect_dark_mode(self):
        if platform.system() == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
            except:
                return False
        return False

    def apply_theme(self):
        bg = "#2e2e2e" if self.is_dark_mode else "white"
        fg = "white" if self.is_dark_mode else "black"
        widget_bg = "#444444" if self.is_dark_mode else "SystemButtonFace"

        self.root.configure(bg=bg)
        self.status_label.configure(bg=bg, fg=fg)
        self.spinner_label.configure(bg=bg, fg=fg)
        self.status_frame.configure(bg=bg)
        self.mode_button.configure(bg="#5577cc" if self.is_auto_mode else "#cc7755")
        self.font_frame.configure(bg=bg)
        self.theme_button.configure(bg=widget_bg, fg=fg)
        self.input_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.output_box.configure(bg=bg, fg=fg, insertbackground=fg)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_button.configure(
            text="Dark Mode 🌙" if not self.is_dark_mode else "Light Mode ☀️"
        )
        self.apply_theme()

    def update_fonts(self, event=None):
        font_name = self.current_font.get()
        self.input_box.configure(font=(font_name, 12))
        self.output_box.configure(font=(font_name, 12))
        self.status_label.configure(font=(font_name, 14))
        self.spinner_label.configure(font=(font_name, 14))
        self.mode_button.configure(font=(font_name, 12, "bold"))
        self.process_button.configure(font=(font_name, 12, "bold"))
        self.theme_button.configure(font=(font_name, 12))

    def toggle_mode(self):
        self.is_auto_mode = not self.is_auto_mode
        self.apply_mode()
        self.apply_theme()

    def apply_mode(self):
        if self.is_auto_mode:
            self.mode_button.config(text="AUTO MODE 🔄", bg="lightblue")
            self.input_box.pack_forget()
            self.output_box.pack_forget()
            self.process_button.pack_forget()
            self.status_label.config(text="Waiting...")
        else:
            self.mode_button.config(text="MANUAL MODE ✍️", bg="orange")
            self.input_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
            self.process_button.pack(padx=10, pady=5, fill=tk.X)
            self.output_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def start_spinner(self):
        if not self.spinner_running:
            self.spinner_running = True
            self.animate_spinner()

    def stop_spinner(self):
        self.spinner_running = False
        self.spinner_label.config(text="")

    def animate_spinner(self):
        if self.spinner_running:
            self.spinner_label.config(text=self.spinner_chars[self.spinner_index])
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
            self.root.after(100, self.animate_spinner)

    def clipboard_watcher(self):
        while self.monitoring:
            if self.is_auto_mode:
                try:
                    text = self.root.clipboard_get()
                    if not isinstance(text, str) or text == self.last_processed:
                        time.sleep(0.5)
                        continue

                    self.update_status("Processing...", spinner=True)
                    joined = " ".join(line.strip() for line in text.splitlines() if line.strip())

                    self.root.clipboard_clear()
                    self.root.clipboard_append(joined)
                    self.root.update()

                    self.last_processed = joined
                    self.update_status("Done ✅", spinner=False)

                except tk.TclError:
                    self.update_status("Waiting...", spinner=False)
            time.sleep(1)

    def update_status(self, msg, spinner=False):
        def callback():
            self.status_label.config(text=msg)
            if spinner:
                self.start_spinner()
            else:
                self.stop_spinner()
        self.root.after(0, callback)

    def manual_process(self):
        try:
            text = self.root.clipboard_get()
            if not isinstance(text, str):
                messagebox.showerror("Error", "Clipboard does not contain text.")
                return
        except tk.TclError:
            messagebox.showerror("Error", "Failed to access clipboard.")
            return

        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, text)

        joined = " ".join(line.strip() for line in text.splitlines() if line.strip())

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, joined)
        self.output_box.configure(state="disabled")

        self.root.clipboard_clear()
        self.root.clipboard_append(joined)
        self.root.update()
        self.update_status("Done ✅", spinner=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = LineJoinerApp(root)
    root.mainloop()