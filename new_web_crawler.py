from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import requests, json

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
            title = soup.title.text.strip() if soup.title else "No Title Found"

            # Extract all the links (URLs) on the page
            links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

            return title, links

        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

data = []

url_to_crawl = "https://en.wikipedia.org/wiki/Google"
title, links = crawl(url_to_crawl)
following_links = links

data.append(
	{
		"Title": title,
		"URL": url_to_crawl
	},
)

print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
for link in following_links:
    try:
        title, links = crawl(link)
        data.append(
            {
                "Title": title,
                "URL": link
            },
        )

        # print(f"{Fore.WHITE}{Style.BRIGHT}Title:", title)
        # print(f"{Fore.WHITE}{Style.BRIGHT}URL:", link)
        # print()

        following_links.extend(links)

    except KeyboardInterrupt:
        break

with open("index.json", "w") as f:
    json.dump(data, f)
