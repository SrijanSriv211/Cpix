from flask import Flask, render_template, request
from web_crawler import crawler

app = Flask(__name__, template_folder="web\\templates", static_folder="web\\static")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    text = request.form["query"]

    print(text)
    crawler_engine = crawler(text)
    crawler_engine.crawl()

    return render_template("index.html")

# app.run(port=8000)
