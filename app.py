from flask import Flask, render_template, request, jsonify
from src.color.color import Color
from src.llm.llm import GROQ
import time, os

# initialize
C = Color("data\\index.bin", "data\\index_hash_map.bin")
llm = GROQ("cache\\GroqAPI.txt")

app = Flask(__name__, template_folder="src\\web\\templates", static_folder="src\\web\\static")
user_history_path = "src\\web\\history\\user_history.txt"

history = []
if os.path.isfile(user_history_path) == False:
    with open(user_history_path, "w", encoding="utf-8") as f:
        f.write("")

else:
    with open(user_history_path, "r", encoding="utf-8") as f:
        history = [i.strip() for i in f.readlines()]

@app.get("/")
def index_get():
    return render_template("index.html", history=history, overview="Hello! How can I help you today?")

@app.route("/", methods=["POST"])
def search():
    # get the search query
    data = request.json
    text = data["query"]

    if text == "<|del-history|>":
        history.clear()
        with open(user_history_path, "w", encoding="utf-8") as f:
            f.write("")

        return jsonify({
            "history": []
        })
    
    elif text.startswith("<|overview|>"):
        return jsonify({
            "overview": llm.generate(text[12:])
        })

    # save the search query in the user history
    if text not in history:
        history.insert(0, text)
        with open(user_history_path, "w", encoding="utf-8") as f:
            f.write("\n".join(history) + "\n")

    # use my Color search algo to search.
    start_time = time.time()
    results = C.search(text)
    end_time = time.time()

    time_taken = f"About {len(results)} results ({(end_time - start_time):.2f} seconds)"

    # render the results.
    return jsonify({
        "results": results,
        "time_taken": time_taken,
        "history": history
    })

if __name__ == "__main__":
    app.run(port=8000)
