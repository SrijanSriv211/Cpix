from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import unicodedata, requests, json

# Initialize colorama
init(autoreset = True)

def crawl(url):
    try:
        # Make an HTTP request to the specified URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title of the page
            title = unicodedata.normalize('NFKD', soup.title.text.strip()) if soup.title else "No Title Found"

            # Extract all the links (URLs) on the page
            links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

            return title, links

        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return ("", [])

    except Exception as e:
        print(f"An error occurred: {e}")
        return ("", [])

with open("data\\index.json", "r", encoding="utf-8") as f:
    old_index_data = json.load(f)

following_links = [i["URL"] for i in old_index_data]
following_links.append("https://en.wikipedia.org")
data = []

print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
for link in following_links:
    try:
        title, links = crawl(link)
        if title != "" or links != []:
            data.append(
                {
                    "Title": title,
                    "URL": link
                },
            )

            following_links.extend(links)

    except KeyboardInterrupt:
        break

print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
