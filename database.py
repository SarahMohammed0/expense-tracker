import sqlite3
#conn is connection to database file
#cursor execute SQL command
DbName="expenses.db"
def init_db():
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute("""
    create table if not exists expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT
    )
    """)
    conn.commit()
    conn.close()
def add_expense(amount, category, date, note=""):
    conn = sqlite3.connect(DbName)
    cursor =conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES(?,?,?,?)",
        (amount,category, date, note)
    )
    conn.commit()
    conn.close()
    print(f"added expense: {amount} - {category} on {date}")


def view_expenses():
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No expenses recorded")
        return
    print(f"{'ID':<4}{'amount':<10}{'category':<15}{'date':<12}{'Note'}")
    print("-"*67)
    for row in rows:
        id,amount,category,date,note =row
        print(f"{id:<4}{amount:<10}{category:<15}{date:<12}{note}")

def delete_expense(expense_ID):
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_ID,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected ==0:
        print(f"No expense found with ID {expense_ID}")
    else:
        print(f" deleted expense with ID {expense_ID}")

def total_spent():
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total= cursor.fetchone()[0]
    conn.close()
    total= total if total else 0
    print(f"total spent:{total:.2f}")
    return total

def spent_by_category():
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute(""" SELECT category , SUM(amount) 
    FROM expenses
    Group BY category
        ORDER BY SUM ( amount) DESC""")
    rows=cursor.fetchall()
    conn.close()
    if not rows:
        print("no expenses recorded")
        return
    print(f"{'category':<15}{'total'}")
    print("-"* 25)
    for category,total in rows:
        print(f"{category:<15}{total:.2f}")

def reset_db():
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    print("All expenses cleared.")

def filter_by_date(start_date, end_date):
    conn = sqlite3.connect(DbName)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date",
        (start_date, end_date)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print(f"No expenses found between {start_date} and {end_date}")
        return
    print(f"{'ID':<4}{'amount':<10}{'category':<15}{'date':<12}{'note'}")
    print("-"*67)
    for row in rows:
        id, amount, category,date,note=row
        print(f"{id:<4}{amount:<10}{category:<15}{date:<12}{note}")


if __name__=="__main__":
    init_db()
    #reset_db()
    while True:
        print("\n *** expenses tracker ***")
        print("1- add expense")
        print("2- view all expenses")
        print("3- delete expenses")
        print("4- total spent")
        print("5- spend by category")
        print("6- filter by date ")
        print("7- exit")

        choice = input("choose option (1-7): ")

        if choice== "1":
            amount=float(input("Amount: "))
            category=input("category: ")
            date= input("date YYYY/MM/DD: ")
            note=input("note(optional): ")
            add_expense(amount,category, date, note)
        elif choice =="2":
            view_expenses()
        elif choice =="3":
            expenses_id=int(input(" Enter ID to delete"))
            delete_expense(expenses_id)
        elif choice =="4":
            total_spent()
        elif choice =="5":
            spent_by_category()
        elif choice == "6":
            start =input("start date (YYY/MM/DD) ")
            end=input(" end date (yyyymm/dd): ")
            filter_by_date(start,end)
        elif choice =="7":
            print("byeeeee")
            break
        else:
            print("invalid input")


