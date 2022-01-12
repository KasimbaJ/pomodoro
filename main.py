from tkinter import *
import sqlite3 as sq3
import math
import datetime
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 5
timer = ""
localDB = "pomodoro_to-do_list.db"

# TODO - 5:---------------------------- to-do list & DB --------
# Create a Table
# Create a database or connect to one
conn = sq3.connect(localDB)
# Create a cursor
c = conn.cursor()
# c.execute("""CREATE TABLE pomodoro (
#     pomodoro_1 text,
#     pomodoro_2 text,
#     pomodoro_3 text,
#     pomodoro_4 text
#     )""")


# Create Submit Function For Databases
def submit():
    # Create a database or connect to one
    conn = sq3.connect(localDB)
    # Create a cursor
    c = conn.cursor()

    # Insert Into Table
    c.execute("INSERT INTO pomodoro VALUES (:pomodoro_1, :pomodoro_2, :pomodoro_3, :pomodoro_4)",
              {
                  'pomodoro_1': pomodoro_1.get(),
                  'pomodoro_2': pomodoro_2.get(),
                  'pomodoro_3': pomodoro_3.get(),
                  'pomodoro_4': pomodoro_4.get(),
              })

    # Commit changes
    c = conn.commit()
    # Close connection
    c = conn.close()

    # Clear The Text Boxes
    pomodoro_1.delete(0, END)
    pomodoro_2.delete(0, END)
    pomodoro_3.delete(0, END)
    pomodoro_4.delete(0, END)



def query():
    # Create a database or connect to one
    conn = sq3.connect(localDB)
    # Create a cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT * FROM pomodoro")
    pomodoros = c.fetchall()
    print(pomodoros)

    # Loop Through Results
    print_records = ''
    for pomodoro in pomodoros:
        print_records += str(pomodoro) + "\n"

    query_label = Label(window, text=print_records)
    query_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10, ipadx=137)

    # Commit changes
    c = conn.commit()
    # Close connection
    c = conn.close()



# TODO - 4:---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0

# TODO - 3:---------------------------- TIMER MECHANISM -------------------------------

def start_timer():
    # count_down(100)
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# TODO - 2:---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
        count_sec = "00"
    elif count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for i in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# TODO - 1:---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro Timer & To-Do List")
window.config(padx=100, pady=50, bg=YELLOW)
# localDB = "pomodoro_to-do_list.db"

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 112, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
# canvas.pack()
canvas.grid(column=1, row=1)

#count_down(100)

start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
# marks += "✔"
check_marks.grid(column=1, row=3)

# Create Text Boxes
pomodoro_1 = Entry(window, width=30)
pomodoro_1.grid(row=4, column=1, padx=20, pady=10)
pomodoro_2 = Entry(window, width=30)
pomodoro_2.grid(row=5, column=1, padx=20, pady=10)
pomodoro_3 = Entry(window, width=30)
pomodoro_3.grid(row=6, column=1, padx=20, pady=10)
pomodoro_4 = Entry(window, width=30)
pomodoro_4.grid(row=7, column=1, padx=20, pady=10)
#
#
# Create Text Box Labels
pomodoro_1_label = Label(window, text="Pomodoro #1")
pomodoro_1_label.grid(row=4, column=0)
pomodoro_2_label = Label(window, text="Pomodoro #2")
pomodoro_2_label.grid(row=5, column=0)
pomodoro_3_label = Label(window, text="Pomodoro #3")
pomodoro_3_label.grid(row=6, column=0)
pomodoro_4_label = Label(window, text="Pomodoro #4")
pomodoro_4_label.grid(row=7, column=0)
#
#
# Create a Submit Button
submit_btn = Button(window, text="Add Record To Database", command=submit)
submit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#
# # Create a Query Button
query_btn = Button(window, text="Show Records", command=query)
query_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10, ipadx=137)

# Commit changes
c = conn.commit()
# Close connection
c = conn.close()


window.mainloop()
