from flask import Flask, render_template, request
from main import clean_sentence, list_of_titles
from utils import text_similarity
from pprint import pprint
import time

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    text = request.form["query"]
    print("SEARCH QUERY:", text)

    start_time = time.time()
    results = text_similarity(clean_sentence(text), list_of_titles)
    end_time = time.time()

    pprint(results)
    print("About", (end_time - start_time), "seconds")

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(port=8000)
