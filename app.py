from flask import Flask, render_template, request
from utils import text_similarity
from pprint import pprint
import json

titles = []
json_file = open("data\\index.json", "r", encoding="utf-8")

for idx, ele in enumerate(json.load(json_file)):
    titles.append(ele["Title"])

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    text = request.form["query"]

    # results = text_similarity(text, site_metadata)
    results = text_similarity(text, titles)

    print("SEARCH QUERY:", text)
    pprint(results)
    return render_template("index.html", results=results)

# app.run(port=8000)
