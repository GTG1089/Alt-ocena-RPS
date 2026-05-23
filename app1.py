from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from tinydb import TinyDB
app = Flask(
    __name__,
    template_folder="templates1",
    static_folder="static1"
)
app.secret_key="very_secret_document"
db=TinyDB("db/notes.json")
@app.route("/")
def index():
    zapiski = db.all()
    return render_template("index.html", zapiski=zapiski)
@app.route("/dodajzapiske", methods=["POST"])
def add():
    naslov=request.form.get('naslov')
    vsebina=request.form.get("vsebina")
    if naslov and vsebina:
        db.insert({"naslov":naslov, "vsebina":vsebina})
    return redirect(url_for("index"))
@app.route("/brisizapiske", methods=["POST"])
#namesto del bris ker del zgleda da je function
def bris():
    return
@app.route("/editzapiske", methods=["POST", "GET"])
def edit(doc_id):
    if request.method == "POST":
        naslov=request.form.get("naslov")
        vsebina=request.form.get("vsebina")
    return
if __name__ == "__main__":
    app.run(debug=True, port=5000)