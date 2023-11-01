import tkinter as tk
from tkinter import messagebox, ttk
import schedule
import time
import threading

class ReminderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("RemindMe")
        self.geometry("400x450")  # Increased height to accommodate large Text widget
        self.configure(bg='light blue')
        self.resizable(False, False)

        # Main Frame
        self.main_frame = tk.Frame(self, bg='light blue')
        self.main_frame.pack(fill="both", expand=1)

        # Create a Notebook (Tabbed Layout)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=1)

        # First Tab (Add Reminder)
        self.tab1 = tk.Frame(self.notebook, width=400, height=400, bg='light blue')
        self.notebook.add(self.tab1, text="Add Reminder")
        
        # Task Entry with Placeholder using Text widget
        self.task_entry = tk.Text(self.tab1, height=20, width=40, fg='grey')
        self.task_entry.pack(pady=10)
        self.task_entry.insert(tk.END, "Task...")
        self.task_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.task_entry.bind("<FocusOut>", self.on_entry_focus_out)

        # Date and Time Entry
        tk.Label(self.tab1, text="Date (YYYY-MM-DD):", bg='light blue').place(x=32,y=340)
        self.date_entry = tk.Entry(self.tab1, width=35)
        self.date_entry.place(x=32, y=370)

        tk.Label(self.tab1, text="Time (HH:MM):", bg='light blue').place(x=260,y=340)
        self.time_entry = tk.Entry(self.tab1, width=15)
        self.time_entry.place(x=260, y=370)

        # Add Button with light red background and white text
        self.add_btn = tk.Button(self.tab1, text="Add Reminder", command=self.add_reminder,
                                 bg='light coral', fg='white', width=45)  # Modified here
        self.add_btn.place(x=30, y=398)

        # Second Tab (View Reminders)
        self.tab2 = tk.Frame(self.notebook, width=400, height=400, bg='light blue')
        self.notebook.add(self.tab2, text="View Reminders")
        
        # Treeview for Reminders
        self.tree = ttk.Treeview(self.tab2, columns=("Task", "Date & Time"), show="headings")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Date & Time", text="Date & Time")
        self.tree.pack(pady=10, fill="both", expand=True)

    def on_entry_focus_in(self, event):
        if self.task_entry.get("1.0", "end-1c") == "Task...":
            self.task_entry.delete("1.0", tk.END)
            self.task_entry.configure(fg='black')

    def on_entry_focus_out(self, event):
        if not self.task_entry.get("1.0", "end-1c"):
            self.task_entry.insert("1.0", "Task...")
            self.task_entry.configure(fg='grey')

    def add_reminder(self):
        task = self.task_entry.get("1.0", "end-1c")
        date = self.date_entry.get()
        time_ = self.time_entry.get()

        if task == "Task" or not date or not time_:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            reminder_time = f"{date} {time_}"
            schedule.every().day.at(time_).do(self.show_reminder, task).tag(reminder_time)
            self.tree.insert("", "end", values=(task, reminder_time))
            messagebox.showinfo("Success", f"Reminder set for {reminder_time}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_reminder(self, task):
        messagebox.showinfo("Reminder", f"Time to: {task}")

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        # Start schedule in a separate thread to keep GUI responsive
        scheduler_thread = threading.Thread(target=self.run_schedule, daemon=True)
        scheduler_thread.start()

        # Run the main loop
        self.mainloop()

if __name__ == "__main__":
    app = ReminderApp()
    app.run()
