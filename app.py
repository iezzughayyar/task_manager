from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect("data.db", check_same_thread=False)
cursor = connection.cursor()

#check if table exits and create one if not

cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tasks'")
#if the count is 1, then table exists
if cursor.fetchone()[0]!=1 :
	cursor.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY,task TEXT, UNIQUE(task));")



tasks = []

@app.route("/")
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks = tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        added = request.form.get("task")
        cursor.execute("INSERT OR IGNORE INTO tasks (task) VALUES (?);", (added,))
        connection.commit()
        return redirect("/")

@app.route("/delete", methods=["POST","GET"])
def delete():
    if request.method == "GET":
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return render_template("delete.html", tasks = tasks)
    else:
        somehin = request.form
        for item in somehin.items():
            if item[1] == "on":
                removed = item[0]
                cursor.execute("DELETE FROM tasks WHERE task = ? ;", (removed,))
                connection.commit()
        return redirect("/")

@app.route("/edit", methods=["POST","GET"])
def edit():
    if request.method == "GET":
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return render_template("edit.html", tasks = tasks)
    else:
        #tasks.clear()
        cursor.execute("DELETE FROM tasks;")
        connection.commit()
        somehin = request.form
        for item in somehin.items():
            #tasks.append(item[1])

            added = item[1]
            cursor.execute("INSERT OR IGNORE INTO tasks (task) VALUES (?);", (added,))
            connection.commit()


        return redirect("/")