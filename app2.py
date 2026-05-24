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
@app.route("/dodajzapiske", methods=["POST"])
def add():
    naslov=request.form.get("naslov")
    vsebina=request.form.get("vsebina")
    if naslov and vsebina:
        db.insert({"naslov":naslov, "vsebina":vsebina})
        session['msg'] = "Zapisek uspešno dodan!"
    return redirect(url_for("index"))
@app.route("/brisizapiske/<int:doc_id>", methods=["POST"])
#namesto "del" bris ker "del" zgleda da je function
def bris_ajax(doc_id):
    db.remove(doc_ids=[doc_id])
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)