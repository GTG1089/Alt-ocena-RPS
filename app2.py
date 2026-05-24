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
    objave = post_seznam.all()
    objave.reverse()
    msg = session.pop('msg', None)
    return render_template("index.html", objave=objave, msg=msg)
@app.route("/register", methods=["GET", "POST"])
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
    msg = session.pop('msg', None)
    return render_template("register.html", msg=msg)
@app.route("/dodajobjavo", methods=["POST"])
def add():
    naslov=request.form.get("naslov")
    vsebina=request.form.get("vsebina")
    if naslov and vsebina:
        db.insert({"naslov":naslov, "vsebina":vsebina})
        session['msg'] = "Zapisek uspešno dodan!"
    return redirect(url_for("index"))
@app.route("/brisiobjavo/<int:doc_id>", methods=["POST"])
def bris_ajax(doc_id):
    db.remove(doc_ids=[doc_id])
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)