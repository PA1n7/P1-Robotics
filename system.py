from tkinter import *
from tkinter import ttk
from json import loads, dumps
from os import path

def start_check():
    if path.exists("db.json"):
        print("Database found!")
    else:
        print("Creating databse...")
        open("db.json", "w").write("{}")

start_check()

u_db = loads(open("db.json").read())

def save():
    open("db.json", "w").write(dumps(u_db))

def add(user):
    def check_add():
        un = username.get()
        num = number.get()
        if un not in u_db[user]["contacts"].keys():
            if num not in u_db[user]["contacts"].values():
                u_db[user]["contacts"][un] = num
                frm.destroy()
                uWin.destroy()
                open_user(user)
                save()
            else:
                alert("number overlap")
        else:
            alert("person already saved")
    frm = Toplevel(mainWin)
    frm.title(user)
    frm.grid()
    username = ttk.Entry(frm)
    username.grid(column=0, row=0)
    number = ttk.Entry(frm)
    number.grid(column=0, row=1)
    ttk.Button(frm, text="Cancel", command=frm.destroy).grid(column=1, row=2)
    ttk.Button(frm, text="Add", command=check_add).grid(column=0, row=2)

def delete_cont(user, cont):
    del u_db[user]["contacts"][cont]
    save()
    uWin.destroy()
    open_user(user)

def open_user(user):
    global uWin
    print(f"opening {user}'s profile")
    frm = Toplevel(mainWin)
    uWin = frm
    frm.title(user)
    frm.grid()
    row = 0
    for contact in u_db[user]["contacts"].keys():
        ttk.Button(frm, text=f"{contact} / {u_db[user]["contacts"][contact]}", command=lambda: delete_cont(user, contact)).grid(column=0, row=row)
        row+=1
    ttk.Button(frm, text="add", command=lambda: add(user)).grid(column=0, row=row)

def login(username, pw):
    un = username.get()
    pwt = pw.get()
    if un != "" and pwt != "":
        if un in u_db.keys():
            if u_db[un]["pw"] == pwt:
                open_user(un)
            else:
                alert("Wrong username or password")
        else:
            alert("User not found!")

def signin(username, pw):
    un = username.get()
    pwt = pw.get()
    if un != "" and pwt != "":
        if un not in u_db.keys():
            u_db[un] = {}
            u_db[un]["pw"] = pwt
            u_db[un]["contacts"] = {}
            alert(text="Added username to db")
            save()

def main():
    global mainWin
    root = Tk()
    main = ttk.Frame(root, padding=20)
    mainWin = main
    main.grid()
    alert = ttk.Label(main)
    username = ttk.Entry(main)
    username.grid(column=0, row=0)
    pw = ttk.Entry(main, show="*")
    pw.grid(column=0, row=1)
    ttk.Label(main).grid(column=0, row=2)
    ttk.Button(main, text="Login", command=lambda: login(username, pw)).grid(column=0, row=3)
    ttk.Button(main, text="Sign In", command=lambda: signin(username, pw)).grid(column=0, row=4)

    root.mainloop()

def alert(text):
    if text != "":
        frm = Toplevel(mainWin)
        frm.title("Alert")
        frm.grid()
        ttk.Label(frm, text=text).grid(column=0, row=0)
        ttk.Button(frm, text="Ok", command=frm.destroy).grid(column=1, row=0)

if(__name__ == "__main__"):
    main()