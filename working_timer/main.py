import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from working_time import working
from scary_effect import show_scary_effect

class WorkingTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Working Time - Focus & Productivity")
        self.root.geometry("550x900")
        self.root.configure(bg='#0f172a')
        self.root.resizable(False, False)

        self.remaining_seconds = 0
        self.is_running = False
        self.timer_thread = None
        self.is_paused = False
        self.stop_event = threading.Event()

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#0f172a')
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)

        header_frame = tk.Frame(main_frame, bg='#0f172a')
        header_frame.pack(fill='x', pady=(0, 15))

        title_label = tk.Label(
            header_frame,
            text="⚡ WORKING TIME",
            font=('Segoe UI', 32, 'bold'),
            fg='#f59e0b',
            bg='#0f172a'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Focused countdown timer for productive work",
            font=('Segoe UI', 12),
            fg='#94a3b8',
            bg='#0f172a'
        )
        subtitle_label.pack(pady=(5, 0))

        separator = tk.Frame(main_frame, height=2, bg='#334155')
        separator.pack(fill='x', pady=15)

        timer_container = tk.Frame(main_frame, bg='#1e293b', highlightbackground='#f59e0b',
                                highlightthickness=2, bd=0)
        timer_container.pack(pady=20, padx=40)

        self.timer_display = tk.Label(
            timer_container,
            text="00:00",
            font=('Segoe UI', 80, 'bold'),
            fg='#f59e0b',
            bg='#1e293b',
            padx=40,
            pady=25
        )
        self.timer_display.pack()

        input_card = tk.Frame(main_frame, bg='#1e293b', relief='flat', bd=0)
        input_card.pack(pady=15, fill='x', padx=20)

        minute_icon = tk.Label(
            input_card,
            text="⏱️",
            font=('Segoe UI', 20),
            bg='#1e293b',
            fg='#f59e0b'
        )
        minute_icon.pack(side='left', padx=10)

        minute_label = tk.Label(
            input_card,
            text="Duration (minutes):",
            font=('Segoe UI', 14, 'bold'),
            fg='#e2e8f0',
            bg='#1e293b'
        )
        minute_label.pack(side='left', padx=10)

        self.minutes_entry = tk.Entry(
            input_card,
            font=('Segoe UI', 16),
            width=8,
            bg='#0f172a',
            fg='#f59e0b',
            insertbackground='#f59e0b',
            relief='flat',
            justify='center'
        )
        self.minutes_entry.pack(side='left', padx=10)
        self.minutes_entry.insert(0, "25")
        self.minutes_entry.bind('<FocusOut>', self.validate_input)

        button_frame = tk.Frame(main_frame, bg='#0f172a')
        button_frame.pack(pady=15)

        self.start_button = self.create_styled_button(
            button_frame, "▶  START", '#10b981', '#059669', self.start_timer
        )
        self.start_button.pack(side='left', padx=8)

        self.pause_button = self.create_styled_button(
            button_frame, "⏸  PAUSE", '#f59e0b', '#d97706', self.pause_timer, state='disabled'
        )
        self.pause_button.pack(side='left', padx=8)

        self.resume_button = self.create_styled_button(
            button_frame, "▶  RESUME", '#3b82f6', '#2563eb', self.resume_timer, state='disabled'
        )
        self.resume_button.pack(side='left', padx=8)

        self.status_frame = tk.Frame(main_frame, bg='#1e293b', relief='flat')
        self.status_frame.pack(pady=15, fill='x', padx=40)

        self.status_icon = tk.Label(
            self.status_frame,
            text="💼",
            font=('Segoe UI', 18),
            bg='#1e293b',
            fg='#10b981'
        )
        self.status_icon.pack(side='left', padx=15, pady=8)

        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to start working",
            font=('Segoe UI', 12),
            fg='#cbd5e1',
            bg='#1e293b'
        )
        self.status_label.pack(side='left', padx=10, pady=8)

        self.progress = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate',
            style='TProgressbar'
        )
        self.progress.pack(pady=15)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar",
                    thickness=8,
                    troughcolor='#1e293b',
                    background='#f59e0b',
                    bordercolor='#0f172a',
                    lightcolor='#f59e0b',
                    darkcolor='#f59e0b')

        reset_frame = tk.Frame(main_frame, bg='#0f172a')
        reset_frame.pack(pady=(5, 15))
        self.reset_button = self.create_styled_button(
            reset_frame, "🔄  RESET", '#ef4444', '#dc2626', self.reset_timer
        )
        self.reset_button.pack()

        footer_label = tk.Label(
            main_frame,
            text="⚡ Work focused | Get better results",
            font=('Segoe UI', 9),
            fg='#64748b',
            bg='#0f172a'
        )
        footer_label.pack(pady=(10, 0))

        self.center_window()

    def create_styled_button(self, parent, text, bg_color, hover_color, command, state='normal'):
        button = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 12, 'bold'),
            bg=bg_color,
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=command,
            state=state
        )

        def on_enter(e):
            if button['state'] == 'normal':
                button.config(bg=hover_color)

        def on_leave(e):
            if button['state'] == 'normal':
                button.config(bg=bg_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def center_window(self):
        self.root.update_idletasks()
        width = 550
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def validate_input(self, event=None):
        try:
            value = int(self.minutes_entry.get())
            if value <= 0:
                self.minutes_entry.delete(0, tk.END)
                self.minutes_entry.insert(0, "1")
            elif value > 999:
                self.minutes_entry.delete(0, tk.END)
                self.minutes_entry.insert(0, "999")
        except ValueError:
            self.minutes_entry.delete(0, tk.END)
            self.minutes_entry.insert(0, "25")

    def start_timer(self):
        if self.is_running:
            return

        try:
            minutes = int(self.minutes_entry.get())
            if minutes <= 0:
                messagebox.showwarning("Invalid Input", "Enter number >0")
                return

            self.remaining_seconds = minutes * 60
            self.update_display()
            self.is_running = True
            self.is_paused = False
            self.stop_event.clear()

            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.resume_button.config(state='disabled')
            self.minutes_entry.config(state='disabled')

            self.status_icon.config(text="⚡", fg='#f59e0b')
            self.status_label.config(text="Working...", fg='#f59e0b')

            self.total_time = self.remaining_seconds
            self.progress['maximum'] = self.total_time
            self.progress['value'] = 0

            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()

            def run_backend():
                working(minutes)
            backend_thread = threading.Thread(target=run_backend, daemon=True)
            backend_thread.start()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def run_timer(self):
        while self.is_running and self.remaining_seconds > 0:
            while self.is_paused and self.is_running:
                time.sleep(0.1)
                continue
            if self.stop_event.wait(1):
                break
            if not self.is_running:
                break
            if self.is_paused:
                continue
            self.remaining_seconds -= 1
            self.root.after(0, self.update_display)
            self.root.after(0, self.update_progress)
        if self.remaining_seconds == 0 and self.is_running:
            self.root.after(0, self.timer_complete)

    def update_progress(self):
        if hasattr(self, 'total_time') and self.total_time > 0:
            elapsed = self.total_time - self.remaining_seconds
            self.progress['value'] = elapsed

    def update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_display.config(text=time_str)

        if self.remaining_seconds <= 10 and self.remaining_seconds > 0:
            self.timer_display.config(fg='#ef4444')
        else:
            self.timer_display.config(fg='#f59e0b')

    def timer_complete(self):
        self.is_running = False
        self.is_paused = False
        self.stop_event.set()
        
        self.status_icon.config(text="✅", fg='#10b981')
        self.status_label.config(text="Time's up! 🎉", fg='#10b981')
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='disabled')
        self.minutes_entry.config(state='normal')

        self.timer_display.config(text="00:00", fg='#10b981')
        self.progress['value'] = 0

        try:
            import winsound
            winsound.Beep(1000, 500)
            winsound.Beep(1500, 300)
        except:
            pass

        # نمایش افکت ترسناک
        show_scary_effect('scary.png', 'scary.wav')

        messagebox.showinfo("Time's Up!", f"Your {self.minutes_entry.get()}-minute session is complete! 🎉")

    def pause_timer(self):
        if not self.is_running or self.is_paused:
            return
        self.is_paused = True
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='normal')
        self.status_icon.config(text="⏸", fg='#f59e0b')
        self.status_label.config(text="Paused", fg='#f59e0b')

    def resume_timer(self):
        if not self.is_running or not self.is_paused:
            return
        self.is_paused = False
        self.pause_button.config(state='normal')
        self.resume_button.config(state='disabled')
        self.status_icon.config(text="⚡", fg='#f59e0b')
        self.status_label.config(text="Working...", fg='#f59e0b')

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.stop_event.set()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=0.5)

        try:
            minutes = int(self.minutes_entry.get())
            self.remaining_seconds = minutes * 60
            self.update_display()
            if hasattr(self, 'total_time'):
                self.total_time = self.remaining_seconds
                self.progress['value'] = 0
        except:
            self.remaining_seconds = 25 * 60
            self.update_display()

        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='disabled')
        self.minutes_entry.config(state='normal')

        self.status_icon.config(text="💼", fg='#10b981')
        self.status_label.config(text="Reset, ready", fg='#cbd5e1')
        self.timer_display.config(fg='#f59e0b')

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkingTimeApp(root)
    root.mainloop()