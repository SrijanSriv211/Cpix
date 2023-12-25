from flask import Flask, render_template, request
from main import color_rank
from pprint import pprint
import time

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    # Get the search query
    text = request.form["query"]

    # Save the search query in the user history
    with open("web\\history\\user.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

    # Use my Color search algo to search.
    start_time = time.time()
    results = color_rank(text)
    end_time = time.time()

    pprint(results)
    print("SEARCH QUERY:", text)
    print("About", (end_time - start_time), "seconds")

    # Render the results.
    return render_template("index.html", results=results)

@app.route("/history")
def history_page():
    return render_template("history.html")

@app.route("/history", methods=["POST"])
def load_history():
    # Load user history
    with open("web\\history\\user.txt", "r", encoding="utf-8") as f:
        history = [i.strip() for i in f.readlines()]

    return render_template("history.html", results=history)

if __name__ == "__main__":
    app.run(port=8000)
