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
        conn.commit()
init_db()
def get_db():
    conn = sqlite3.connect('db3/weather.db')
    conn.row_factory = sqlite3.Row #<----- Ta koda nardi da loh stvari gledaš kot slovar (prek imen stolpcev)
    return conn
@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    c = conn.cursor()
    loc_base = c.execute("SELECT * FROM locations WHERE username = ?", (session["username"],)).fetchall()
    conn.close()
    weather_dat=[]
    for location in loc_base:
        url=f"http://api.openweathermap.org/data/2.5/weather?q={location['city']}&appid={API_KEY}&units=metric&lang=en"
        response=requests.get(url).json()

        if response.get("cod")==200:
            timedlt=response["timezone"]
            lokalni_cas=datetime.now(timezone.utc) + timedelta(seconds=timedlt)
            cas_string = lokalni_cas.strftime('%H:%M:%S')

            weather_dat.append({
                "id": location["id"], # sqlite id
                "city": response["name"],
                "temp": response["main"]["temp"],
                "description": response["weather"][0]["description"],
                "local_time": cas_string
            })
    return render_template("index.html",podatki=weather_dat, msg=session.pop('msg', None), cur_user=session["username"])
#login/register/logout
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        pw=request.form.get("pw")
        if username and pw:
            conn = get_db()
            c=conn.cursor()
            #Dupe check for username
            uporabnik=c.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()           #vejica po username zato da je tuple
            if uporabnik:
                session["msg"]="Uporabniško ime že obstaja!"
                return redirect(url_for("register"))
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
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))
#saving locations
@app.route("/add_location", methods=["POST"])
def add_location():
    cty=request.form.get("mesto")

    if cty:
        url= f"http://api.openweathermap.org/data/2.5/weather?q={cty}&appid={API_KEY}&units=metric&lang=en"
        response=requests.get(url).json()
        if response.get("cod")==200:
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO locations (username, city) VALUES (?, ?)", (session["username"], response["name"]))
            conn.commit()
            conn.close()
            session["msg"] = f"Mesto {response['name']} uspešno dodano!"
        else:
            session["msg"]="Neznano mesto"
    return redirect(url_for("index"))
@app.route("/delete_location/<int:loc_id>", methods=["POST"])
def delete_location(loc_id):
    if "username" not in session:
        return jsonify({"success":False})
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM locations WHERE id = ? AND username = ?", (loc_id, session["username"]))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    if changes>0:
        return jsonify({"success":True})
    return jsonify({"success":False})
if __name__ == "__main__":
    app.run(debug=True, port=5000)
#maybe nared weather forecast za daterange
