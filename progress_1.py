"""
SMART TASK SCHEDULING SYSTEM
Greedy vs Brute Force with Advanced Viewing Options

Features:
- Date + military time deadlines
- Input validation
- Sorting view options
- Greedy vs brute-force comparison
"""

import time
import datetime
from itertools import permutations

# ======================================================
# TASK CLASS
# ======================================================

class Task:
    def __init__(self, name, deadline, profit):
        self.name = name
        self.deadline = deadline
        self.profit = profit

    def __repr__(self):
        return (
            f"{self.name} | Deadline: "
            f"{self.deadline.strftime('%m-%d %H:%M')} | Profit: {self.profit}"
        )

# ======================================================
# INPUT FUNCTIONS
# ======================================================

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Enter a value.")
        else:
            return value

def get_integer_input(prompt):
    while True:
        value = get_non_empty_input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")

def get_deadline_input():
    while True:
        print("\nEnter deadline in this format:")
        print("MM-DD HH:MM")
        print("Example: 03-31 14:30")

        value = input("Deadline: ").strip()

        if value == "":
            print("Enter a value.")
            continue

        try:
            current_year = datetime.datetime.now().year
            full_date = f"{current_year}-{value}"
            deadline = datetime.datetime.strptime(
                full_date, "%Y-%m-%d %H:%M"
            )
            return deadline
        except ValueError:
            print("Invalid format. Use MM-DD HH:MM with military time.")

# ======================================================
# ALGORITHMS
# ======================================================

def greedy_schedule(tasks):
    tasks_sorted = sorted(tasks, key=lambda t: t.deadline)
    schedule = []
    total_profit = 0

    for task in tasks_sorted:
        schedule.append(task)
        total_profit += task.profit

    return schedule, total_profit

def brute_force_schedule(tasks):
    best_profit = 0
    best_schedule = []

    for perm in permutations(tasks):
        profit = sum(task.profit for task in perm)
        if profit > best_profit:
            best_profit = profit
            best_schedule = list(perm)

    return best_schedule, best_profit

# ======================================================
# VIEWING & DISPLAY
# ======================================================

def print_tasks(task_list):
    print("\nCurrent Tasks:")
    print("-----------------------------------")
    for i, task in enumerate(task_list, 1):
        print(f"{i}. {task}")
    print("-----------------------------------")

def display_tasks_menu(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    # Start with default view (unsorted)
    current_tasks = tasks[:]
    print_tasks(current_tasks)

    while True:
        print("\nWhat would you like to do next?")
        print("1. Change order of viewing")
        print("2. Return to Main Menu")
        print("3. Exit Program")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            print("\nVIEW TASK OPTIONS")
            print("---------------------------")
            print("a. Alphabetical (Task Name)")
            print("b. Earliest Deadline First")
            print("c. Profit: Highest to Lowest")
            print("d. Profit: Lowest to Highest")

            order_choice = input("Choose how to view tasks (a/b/c/d): ").strip().lower()

            if order_choice == "a":
                current_tasks = sorted(tasks, key=lambda t: t.name.lower())
            elif order_choice == "b":
                current_tasks = sorted(tasks, key=lambda t: t.deadline)
            elif order_choice == "c":
                current_tasks = sorted(tasks, key=lambda t: t.profit, reverse=True)
            elif order_choice == "d":
                current_tasks = sorted(tasks, key=lambda t: t.profit)
            else:
                print("Invalid choice. Showing previous order.")
                continue

            print_tasks(current_tasks)

        elif choice == "2":
            print("Returning to Main Menu...")
            return  # exit function to go back to main menu

        elif choice == "3":
            print("Exiting program...")
            exit()  # ends the program

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

# ======================================================
# TASK MANAGEMENT
# ======================================================

def add_task(tasks):
    print("\nEnter task details:")
    name = get_non_empty_input("Task name: ")
    deadline = get_deadline_input()
    profit = get_integer_input("Profit: ")

    tasks.append(Task(name, deadline, profit))
    print("\nTask added successfully!")

# ======================================================
# NAVIGATION
# ======================================================

def continue_or_exit():
    while True:
        print("\n1. Return to menu")
        print("2. Exit program")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            return
        elif choice == "2":
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Please select 1 or 2.")

# ======================================================
# MAIN MENU
# ======================================================

def main():
    tasks = []

    while True:
        print("\n==============================")
        print("SMART TASK SCHEDULING SYSTEM")
        print("==============================")
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Run Greedy Scheduling")
        print("4. Compare Greedy vs Brute Force")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_task(tasks)
            continue_or_exit()

        elif choice == "2":
            display_tasks_menu(tasks)
            continue_or_exit()

        elif choice == "3":
            if not tasks:
                print("No tasks to schedule.")
            else:
                schedule, profit = greedy_schedule(tasks)
                print_tasks(schedule)
                print(f"Total Profit: {profit}")
            continue_or_exit()

        elif choice == "4":
            if not tasks:
                print("No tasks to schedule.")
                continue_or_exit()

            print("\nRunning Greedy Algorithm...")
            start = time.time()
            greedy_result, greedy_profit = greedy_schedule(tasks)
            greedy_time = time.time() - start

            print("Running Brute Force Algorithm...")
            start = time.time()
            brute_result, brute_profit = brute_force_schedule(tasks)
            brute_time = time.time() - start

            print("\nGREEDY RESULT:")
            print_tasks(greedy_result)
            print(f"Total Profit: {greedy_profit}")
            print(f"Execution Time: {greedy_time:.6f} seconds")

            print("\nBRUTE FORCE RESULT:")
            print_tasks(brute_result)
            print(f"Total Profit: {brute_profit}")
            print(f"Execution Time: {brute_time:.6f} seconds")

            if greedy_profit == brute_profit:
                print("\nGreedy found the optimal solution.")
            else:
                print("\nGreedy did NOT find the optimal solution.")

            continue_or_exit()

        elif choice == "5":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1–5.")

# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    main()
