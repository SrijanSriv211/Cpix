from bs4 import BeautifulSoup
import requests

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

print(f"Title: {title}")
print(f"URL: {title}")

print("Following Links:")
for link in links:
    print(link)
