import sqlite3

def to_connect():
    connection = sqlite3.connect("to_do_database_4.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        status INTEGER NOT NULL,
        prior INTEGER NOT NULL,
        time FLOAT NOT NULL
    )
    ''')
    connection.commit()
    return connection, cursor

def add_task():
    connection, cursor = to_connect()
    task_name = input("\nEnter the task name: ")
    while True:
        status = int(input("Enter the status: pending(0) ou done(1) "))
        if status == 0 or status == 1:
            break
        else:
            print("Only 0 and 1 are accepted")
    
    while True:
        prior = int(input("Enter the task priority: High(1), Medium(2), Low(3): "))
        if prior == 1 or prior == 2 or prior == 3:
            break
        else:
            print("Only 1, 2 or 3 accepted")
    
    time = float(input("Enter one time (ex.: 8.2 to 8:20): "))
    cursor.execute('''
    INSERT INTO tasks (task_name, status, prior, time)
    VALUES (?, ?, ?, ?)
    ''', (task_name, status, prior, time))
    connection.commit()
    connection.close()
    print("\nTask successfully entered")

def task_uptade():
    connection, cursor = to_connect()
    task_id = int(input("Please, enter the task ID to be updated: "))
    task_name = input("Enter the task name: ")
    status = int(input("Enter the status: Pending(0) ou Done(1) "))
    prior = int(input("Enter the task priority: High(1), Medium(2), Low(3): "))
    time = float(input("Enter one time (ex.: 8.2 to 8:20): "))
    cursor.execute('''
    UPDATE tasks
    SET task_name = ?, status = ?, prior = ?, time = ?
    WHERE id = ?
    ''', (task_name, status, prior, time, task_id))
    connection.commit()
    connection.close()
    print("\nTask successfully updated")

def task_delete():
    connection, cursor = to_connect()
    task_id = int(input("\nPlease, enter the task ID do be deleted: "))
    
    #Take the task name
    cursor.execute('SELECT task_name FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task:
        task_name = task[0]

        # ANSI CODE FOR COLOR
        YELLOW = '\033[93m'
        RESET = '\033[0m'

        confirmation = input(f"{YELLOW}Are you sure you want to delete the task '{task_name}'?  (y/n) {RESET}").lower()
        if confirmation == 'y':
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            connection.commit()
            print("\ntask successfully deleted")
        else:
            print("\nExclusion cancelled")
    else:
        print("\ntask not found")
    
    connection.close()

def show_tasks():
    
    # OPENING CONNECTION
    connection, cursor = to_connect()
    
    # SELECTING ALL TASKS AND ORDERING THEM BY TIME
    cursor.execute('SELECT * FROM tasks ORDER BY time')
    
    # OPINING CURSOR
    tasks = cursor.fetchall()
    print("")
    
    #TASK HEADER
    print(f"{"ID":<4} | {"TASK NAME":<30} | {"STATUS":<8} | {"PRIORITY":<12} | {"TIME":<6}")
    print("-" * 70)
    
    # ANSI COLOR CODES
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    for task in tasks:
        task_id, task_name, status, priority, time = task
        
        # CONVERTING STATUS CODE IN STATUS STRING TO SHOW TO USER
        status_string = "Pending" if status == 0 else "Done"
        
        # CONVERTING PRIORITIES TO TEXT
        if priority == 1:
            priority_string = "High"
        elif priority == 2:
            priority_string = "Medium"
        elif priority == 3:
            priority_string = "Low"
        else:
            priority_string = "Not defined"

        # Highlighting task status
        color = RED if status == 0 else GREEN
        
        print(f"{task_id:<4} | {task_name:<30} | {color}{status_string:<8}{RESET} | {priority_string:<12} | {time:<6}" )
    connection.close()
    
def update_task_time():
    connection, cursor = to_connect()
    task_id = int(input("Please, enter the task ID to be updated: "))
    time = float(input("Plese, enter a new task time: "))
    cursor.execute('''
    UPDATE tasks
    SET time = ?
    WHERE id = ?
    ''', (time, task_id))
    connection.commit()
    connection.close()
    print("\nTask successfully updated")

def main():
    to_connect()
    while True:
        print("\nMenu:")
        print("1 - Insert task")
        print("2 - Update task")
        print("3 - Delete task")
        print("4 - Show tasks")
        print("5 - Change task time")
        print("6 - Leave")

        choose = input("Please, enter the desired option: ")
        if choose == "1":
            add_task()
        elif choose == "2":
            task_uptade()
        elif choose == "3":
            task_delete()
        elif choose == "4":
            show_tasks()
        elif choose == "5":
            update_task_time()
        elif choose == "6":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()


