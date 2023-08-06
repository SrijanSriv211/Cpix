from flask import Flask, render_template, request

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    text = request.form["query"]
    print(text)
    return render_template("index.html", results="This is a test search result")

# app.run(port=8000)
