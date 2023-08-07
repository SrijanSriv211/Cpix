from flask import Flask, render_template, request

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    text = request.form["query"]
    print(text)

    # results = [
    # "This is a test search result", "Test2"
    # ]
    results = [
        {
            "title": "This is a test search result",
            "url": "https://google.com"
        },
        {
            "title": "Test2",
            "url": "https://youtube.com"
        }
    ]
    return render_template("index.html", results=results)

# app.run(port=8000)
