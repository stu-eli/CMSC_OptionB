"""
SMART TASK SCHEDULING SYSTEM
Improved version with:
- Blank input validation
- Option to return to menu or exit after actions
"""

import time
from itertools import permutations

# ======================================================
# TASK DATA STRUCTURE
# ======================================================

class Task:
    def __init__(self, name, deadline, profit):
        self.name = name
        self.deadline = deadline
        self.profit = profit

    def __repr__(self):
        return f"{self.name} | Deadline: {self.deadline} | Profit: {self.profit}"


# ======================================================
# INPUT VALIDATION FUNCTIONS
# ======================================================

def get_non_empty_input(prompt):
    """Ensures user cannot enter blank values."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Enter a value.")
        else:
            return value


def get_integer_input(prompt):
    """Ensures user enters a valid integer."""
    while True:
        value = get_non_empty_input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")


# ======================================================
# GREEDY ALGORITHM
# ======================================================

def greedy_schedule(tasks):
    tasks_sorted = sorted(tasks, key=lambda t: t.profit, reverse=True)

    max_deadline = max(task.deadline for task in tasks)
    schedule = [None] * max_deadline

    for task in tasks_sorted:
        for slot in range(task.deadline - 1, -1, -1):
            if schedule[slot] is None:
                schedule[slot] = task
                break

    scheduled = [t for t in schedule if t]
    profit = sum(t.profit for t in scheduled)
    return scheduled, profit


# ======================================================
# BRUTE FORCE ALGORITHM
# ======================================================

def brute_force_schedule(tasks):
    best_profit = 0
    best_schedule = []

    for perm in permutations(tasks):
        time_slot = 0
        profit = 0
        current = []

        for task in perm:
            if time_slot < task.deadline:
                current.append(task)
                profit += task.profit
                time_slot += 1

        if profit > best_profit:
            best_profit = profit
            best_schedule = current

    return best_schedule, best_profit


# ======================================================
# DISPLAY FUNCTIONS
# ======================================================

def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nCurrent Tasks:")
    print("-----------------------------------")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print("-----------------------------------")


def display_schedule(schedule, profit):
    print("\nScheduled Tasks:")
    print("-----------------------------------")
    for task in schedule:
        print(task)
    print("-----------------------------------")
    print(f"Total Profit: {profit}")


# ======================================================
# TASK MANAGEMENT
# ======================================================

def add_task(tasks):
    print("\nEnter task details:")

    name = get_non_empty_input("Task name: ")
    deadline = get_integer_input("Deadline: ")
    profit = get_integer_input("Profit: ")

    tasks.append(Task(name, deadline, profit))
    print("Task added successfully!")


# ======================================================
# NAVIGATION FUNCTION
# ======================================================

def continue_or_exit():
    """Gives user choice to return to menu or exit."""
    while True:
        print("\n1. Return to menu")
        print("2. Exit program")
        choice = input("Choose an option: ").strip()

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
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Run Greedy Scheduling")
        print("4. Compare Greedy vs Brute Force")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
            continue_or_exit()

        elif choice == "2":
            display_tasks(tasks)
            continue_or_exit()

        elif choice == "3":
            if not tasks:
                print("No tasks to schedule.")
            else:
                schedule, profit = greedy_schedule(tasks)
                display_schedule(schedule, profit)
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
            display_schedule(greedy_result, greedy_profit)
            print(f"Execution Time: {greedy_time:.6f} seconds")

            print("\nBRUTE FORCE RESULT:")
            display_schedule(brute_result, brute_profit)
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