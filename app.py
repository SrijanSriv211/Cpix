from flask import Flask, render_template, request, jsonify
from colorama import Fore, Style, init
from src.color.history import History
from src.color.color import Color
from src.llm.llm import GROQ
from pprint import pprint
import webbrowser, time

# initialize
init(autoreset = True)
COLOR = Color("data\\index.bin", "data\\index_hash_map.bin")
HISTORY = History("cache\\history.json")
LLM = GROQ("cache\\GroqAPI.txt")

app = Flask(__name__, template_folder="src\\web\\templates", static_folder="src\\web\\static")
history = HISTORY.load()

bangs = {
    "g?": "https://www.google.com/search?q=",
    "yt?": "https://www.youtube.com/results?search_query=",
    "eb?": "https://www.britannica.com/search?query=",
    "git?": "https://github.com/search?q=",
    "bing?": "https://www.bing.com/search?q=",
    "ddg?": "https://duckduckgo.com/?q=",
    "gs?": "https://scholar.google.com/scholar?q=",
    "wiki?": "https://en.wikipedia.org/w/index.php?search="
}

@app.get("/")
def index_get():
    print([i["query"] for i in history])
    return render_template("index.html", history=[i["query"] for i in history], overview="Hello! How can I help you today?")

@app.route("/", methods=["POST"])
def search():
    # get the search query
    data = request.json
    text: str = data["query"].strip()

    # special tokens
    if text == "<|del-history|>":
        return jsonify({
            "history": HISTORY.delete()
        })

    elif text.startswith("<|overview|>"):
        print(f"{Fore.YELLOW}{Style.BRIGHT}Getting AI overview")

        return jsonify({
            "overview": LLM.generate(text[12:])
        })

    elif any(text.lower().startswith(i) for i in bangs.keys()):
        bang = text[:text.find("?") + 1].lower()
        text = text[text.find("?") + 1:].strip()
        print(f"{Fore.YELLOW}{Style.BRIGHT}Bang:", bang)
        webbrowser.open(bangs[bang] + text.replace(" ", "+"))

    # use my Color search algo to search.
    start_time = time.time()

    result, score = HISTORY.search(text)
    results = COLOR.search(text) if score < 0.9 else result["results"]
    total_results = len(results) if score < 0.9 else result["total_results"]

    end_time = time.time()

    time_taken = f"About {total_results} results ({(end_time - start_time):.2f} seconds)"
    results = results[:50]

    # save the search query in the user history
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving History")
    history = HISTORY.update(text, results, total_results)

    print(f"{Fore.YELLOW}{Style.BRIGHT}SEARCH QUERY:", text)
    print(f"{Fore.YELLOW}{Style.BRIGHT}RESULTS:")
    pprint(results[0])
    print(f"{Fore.WHITE}{Style.BRIGHT}{time_taken}")


    # render the results.
    return jsonify({
        "results": results,
        "time_taken": time_taken,
        "history": [i["query"] for i in history]
    })

if __name__ == "__main__":
    app.run(port=8000)
