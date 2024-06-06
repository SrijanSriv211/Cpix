from flask import Flask, render_template, request
from colorama import Fore, Style, init
from src.color.color import Color
from pprint import pprint
import time, os

# Initialize colorama & Color
init(autoreset = True)
C = Color("data\\index.json", "data\\index_hash_map.json")

app = Flask(__name__, template_folder="src\\web\\templates", static_folder="src\\web\\static")
user_history_path = "src\\web\\history\\user_history.txt"
if os.path.isfile(user_history_path) == False:
    with open(user_history_path, "w", encoding="utf-8") as f:
        f.write("")

@app.get("/")
def index_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
    # Get the search query
    text = request.form["query"]

    # Save the search query in the user history
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving History")
    with open(user_history_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    # Use my Color search algo to search.
    start_time = time.time()
    results = C.search(text)
    end_time = time.time()

    time_taken = f"About {len(results)} results ({(end_time - start_time):.2f} seconds)"

    print(f"{Fore.YELLOW}{Style.BRIGHT}SEARCH QUERY:", text)
    print(f"{Fore.YELLOW}{Style.BRIGHT}RESULTS:")
    pprint(results)
    print(f"{Fore.WHITE}{Style.BRIGHT}{time_taken}")

    # Render the results.
    return render_template("index.html", results=results, time_taken=time_taken)

@app.route("/history")
def load_history():
    # Load user history
    with open(user_history_path, "r", encoding="utf-8") as f:
        history = [i.strip() for i in f.readlines()]

    print(history)

    return render_template("history.html", results=history)

@app.route("/history", methods=["POST"])
def delete_history():
    # Delete user history
    with open(user_history_path, "w", encoding="utf-8") as f:
        f.write("")

    print("History deleted")

    return render_template("history.html")

if __name__ == "__main__":
    app.run(port=8000)
