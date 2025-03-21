from flask import Flask, render_template, request, jsonify
from colorama import Fore, Style, init
from src.color.color import Color
from src.llm import GROQ
from pprint import pprint
import time, os

# Initialize
init(autoreset = True)
C = Color("data\\index.json", "data\\index_hash_map.json")
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
    # Get the search query
    data = request.json
    text = data["query"]

    print(text)

    if text == "<|del-history|>":
        print(f"{Fore.YELLOW}{Style.BRIGHT}Clearing History")

        history.clear()
        with open(user_history_path, "w", encoding="utf-8") as f:
            f.write("")

        return jsonify({
            "history": []
        })

    # Save the search query in the user history
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving History")
    if text not in history:
        history.insert(0, text)
        with open(user_history_path, "w", encoding="utf-8") as f:
            f.write("\n".join(history) + "\n")

    # Use my Color search algo to search.
    start_time = time.time()
    overview = llm.generate(text)
    results = C.search(text)
    end_time = time.time()

    time_taken = f"About {len(results)} results ({(end_time - start_time):.2f} seconds)"

    print(f"{Fore.YELLOW}{Style.BRIGHT}SEARCH QUERY:", text)
    print(f"{Fore.YELLOW}{Style.BRIGHT}RESULTS:")
    pprint(results)
    print(f"{Fore.YELLOW}{Style.BRIGHT}AI OVERVIEW:")
    print(overview)
    print(f"{Fore.WHITE}{Style.BRIGHT}{time_taken}")

    # Render the results.
    return jsonify({
        "results": results,
        "time_taken": time_taken,
        "history": history,
        "overview": overview
    })

if __name__ == "__main__":
    app.run(port=8000)
