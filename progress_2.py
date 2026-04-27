import tkinter as tk
from tkinter import ttk, messagebox
import datetime


# ---------------- TASK ----------------

class Task:
    def __init__(self, name, deadline, profit):
        self.name = name
        self.deadline = deadline
        self.profit = profit


# ---------------- MERGE SORT ----------------

def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items, key):
    if len(items) <= 1:
        return items

    mid = len(items)//2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    return merge(left, right, key)


# ---------------- GUI ----------------

tasks = []


def add_task():
    name = name_entry.get().strip()
    date_text = deadline_entry.get().strip()
    profit_text = profit_entry.get().strip()

    if not name or not date_text or not profit_text:
        messagebox.showwarning(
            "Missing Input",
            "Fill in all fields."
        )
        return

    try:
        year = datetime.datetime.now().year
        deadline = datetime.datetime.strptime(
            f"{year}-{date_text}",
            "%Y-%m-%d %H:%M"
        )

        profit = int(profit_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Deadline format: MM-DD HH:MM\nProfit must be a number."
        )
        return

    tasks.append(
        Task(name, deadline, profit)
    )

    name_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    profit_entry.delete(0, tk.END)

    show_tasks(tasks)

    messagebox.showinfo(
        "Success",
        "Task added successfully."
    )


def show_tasks(task_list):
    listbox.delete(0, tk.END)

    if not task_list:
        listbox.insert(
            tk.END,
            "No tasks available."
        )
        return

    for i, task in enumerate(task_list,1):
        text = (
            f"{i}. {task.name} | "
            f"{task.deadline.strftime('%m-%d %H:%M')} | "
            f"Profit:{task.profit}"
        )
        listbox.insert(tk.END,text)


def sort_alpha():
    sorted_tasks = merge_sort(
        tasks,
        key=lambda t: t.name.lower()
    )
    show_tasks(sorted_tasks)


def sort_deadline():
    sorted_tasks = merge_sort(
        tasks,
        key=lambda t: t.deadline
    )
    show_tasks(sorted_tasks)


def sort_high_profit():
    sorted_tasks = merge_sort(
        tasks,
        key=lambda t: -t.profit
    )
    show_tasks(sorted_tasks)


def sort_low_profit():
    sorted_tasks = merge_sort(
        tasks,
        key=lambda t: t.profit
    )
    show_tasks(sorted_tasks)


def generate_schedule():
    if not tasks:
        messagebox.showwarning(
            "No Tasks",
            "Add tasks first."
        )
        return

    scheduled = merge_sort(
        tasks,
        key=lambda t: t.deadline
    )

    show_tasks(scheduled)

    total_profit = sum(
        t.profit for t in scheduled
    )

    messagebox.showinfo(
        "Schedule Generated",
        f"Tasks scheduled by earliest deadline.\n"
        f"Total Profit: {total_profit}"
    )


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Smart Task Scheduling System")
root.geometry("800x600")


title = tk.Label(
    root,
    text="SMART TASK SCHEDULING SYSTEM",
    font=("Arial",18,"bold")
)
title.pack(pady=10)


# ------- Input Frame -------

frame = tk.Frame(root)
frame.pack(pady=10)


tk.Label(
    frame,
    text="Task Name"
).grid(row=0,column=0,padx=8)

name_entry = tk.Entry(frame,width=18)
name_entry.grid(row=0,column=1)


tk.Label(
    frame,
    text="Deadline (MM-DD HH:MM)"
).grid(row=0,column=2,padx=8)

deadline_entry = tk.Entry(frame,width=18)
deadline_entry.grid(row=0,column=3)


tk.Label(
    frame,
    text="Profit"
).grid(row=0,column=4,padx=8)

profit_entry = tk.Entry(frame,width=10)
profit_entry.grid(row=0,column=5)


add_btn = tk.Button(
    root,
    text="Add Task",
    width=20,
    command=add_task
)
add_btn.pack(pady=8)


# ------- Sort Buttons -------

sort_frame = tk.Frame(root)
sort_frame.pack(pady=10)

buttons = [
("Alphabetical",sort_alpha),
("Deadline",sort_deadline),
("Highest Profit",sort_high_profit),
("Lowest Profit",sort_low_profit),
("Generate Schedule",generate_schedule)
]

for text,cmd in buttons:
    tk.Button(
        sort_frame,
        text=text,
        command=cmd,
        width=18
    ).pack(
        side=tk.LEFT,
        padx=5
    )


# ------- Task List -------

list_frame = tk.Frame(root)
list_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

listbox = tk.Listbox(
    list_frame,
    font=("Courier New",11),
    yscrollcommand=scrollbar.set
)

listbox.pack(
    fill="both",
    expand=True
)

scrollbar.config(
    command=listbox.yview
)


root.mainloop()