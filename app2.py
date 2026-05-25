from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from tinydb import TinyDB, Query
app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key="very_secret_document"#War thunder reference
db=TinyDB("db2/omrezje.json")
upor_seznam=db.table('uporabniki')
post_seznam=db.table('objave')
user = Query()
@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    objave = post_seznam.all()
    objave.reverse()           
    msg = session.pop('msg', None)
    return render_template("index.html", objave=objave, msg=msg, cur_user=session["username"])
@app.route("/register", methods=["GET", "POST"])
#Login/Register/logout under here
def register():
    if request.method == "POST":
        username=request.form.get("username")
        pw=request.form.get("pw")

        if username and pw:
            if upor_seznam.search(user.username==username):
                session['msg']="Uporabniško ime že obstaja!"
                return redirect(url_for("register"))
        
        upor_seznam.insert({"username": username, "password": pw})
        session['msg'] = "Registracija uspešna!"
        return redirect(url_for("login"))
    msg = session.pop('msg', None)
    return render_template("register.html", msg=msg)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username=request.form.get("username")
        pw=request.form.get("pw")

        isci_upor=upor_seznam.search((user.username==username) & (user.password==pw))
        if isci_upor:
            session["username"]=username
            return redirect(url_for("index"))
        else:
            session["msg"]="Napačno uporabniško ime ali geslo!"
            return redirect(url_for("login"))
    msg = session.pop('msg', None)
    return render_template("login.html", msg=msg)
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))
@app.route("/dodajobjavo", methods=["POST"])
#Posts
def add():
    vsebina=request.form.get("besedilo")
    slika=request.files.get("slika")
    ime_slike=""
    if slika and slika.filename:
        ime_slike = slika.filename
        slika.save("static2/"+ime_slike)
    if vsebina:
        post_seznam.insert({
            "avtor": session["username"],
            "vsebina": vsebina,
            "slika":ime_slike

        })
        session["msg"]="Uspešno si objavil novo objavo!"
    return redirect(url_for("index"))
#delete je extra funkcija
@app.route("/brisiobjavo/<int:doc_id>", methods=["POST"])
def bris_ajax(doc_id):
    if "username" not in session:
        return jsonify({"success": False})
    objava=post_seznam.get(doc_id=doc_id)
    if objava and objava["avtor"]==session["username"]:    
        post_seznam.remove(doc_ids=[doc_id])
        return jsonify({"success": True})

    return jsonify({"success": False})
if __name__ == "__main__":
    app.run(debug=True, port=5000)