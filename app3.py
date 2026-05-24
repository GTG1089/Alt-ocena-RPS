import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from datetime import datetime, timezone, timedelta

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)
app.secret_key="sekritdokument"
API_KEY="61ea5bdda483dd02d99dfd5308d8264f"
os.makedirs("db3", exist_ok=True)
def init_db():
    with sqlite3.connect("db3/weather.db") as conn:
        c=conn.cursor()
        c.execute(''' create table if not exists users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS locations 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, city TEXT)
        ''')
        conn.commit
init_db()
def get_db():
    conn = sqlite3.connect('db3/weather.db')
    conn.row_factory = sqlite3.Row #<----- Ta koda nardi da loh stvari gledaš kot slovar (prek imen stolpcev)
    return conn
@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", msg=session.pop('msg', None), cur_user=session["username"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        pw=request.form.get("pw")
        if username and pw:
            conn = get_db()
            c=conn.cursor()
            #Dupe check for username
            uporabnik=c.execute("SELECT * FROM users WHERE username=?", (username)).fetchone()           
            if uporabnik:
                session["msg"]="Uporabniško ime že obstaja!"
                return redirect(url_for("/register"))
            c.execute("INSERT INTO Users(username, password) Values(?,?)",(username,pw))
            conn.commit()
            conn.close()
        session["msg"] = "Registracija uspešna!"
        return redirect(url_for("login"))
    return render_template("register.html", msg=session.pop("msg",None))
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username=request.form.get("username")
        pw=request.form.get("pw")
        conn=get_db()
        c=conn.cursor()

        isci_upor=c.execute("Select * from users WHERE username = ? and password= ?", (username,pw)).fetchone()
        if isci_upor:
            session["username"]=username
            return redirect(url_for("index"))
        else:
            session["msg"]="Napačno uporabniško ime ali geslo!"
            return redirect(url_for("login"))
    return render_template("login.html", msg=session.pop('msg', None))
if __name__ == "__main__":
    app.run(debug=True, port=5000)
