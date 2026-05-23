from flask import Flask, render_template, request
from tinydb import TinyDB
app = Flask(
    __name__,
    template_folder="templates1",
    static_folder="static1"
)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/dodajzapiske", methods=["POST"])
def add():
    return
@app.route("/brisizapiske", methods=["POST"])
#namesto del bris ker del zgleda da je function
def bris():
    return
@app.route("/editzapiske", methods=["POST", "GET"])
def edit():
    return
if __name__ == "__main__":
    app.run(debug=True, port=5000)