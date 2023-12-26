from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import unicodedata, requests, numpy, json

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
            title = unicodedata.normalize('NFKD', soup.title.text.strip()) if soup.title else ""

            # Extract the meta description of the page
            meta_description_tag = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description_tag['content'].strip() if meta_description_tag else ""

            # Extract the meta keywords of the page
            meta_keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            meta_keywords = meta_keywords_tag['content'].strip() if meta_keywords_tag else ""

            # Extract all the links (URLs) on the page
            links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

            return ("", "", [], []) if title == "" else (title, meta_description, meta_keywords, links)

        else:
            with open("crashreport.txt", "a", encoding="utf-8") as f:
                f.write(f"Failed to retrieve {url}. Status code: {response.status_code}\n")

            return ("", "", [], [])

    except Exception as e:
        with open("crashreport.txt", "a", encoding="utf-8") as f:
            f.write(f"An error occurred: {e}\n")

        return ("", "", [], [])

def save(data):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

following_links = ["https://www.learncbse.in/"]
patience = 1000
data = []

print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
for link in following_links:
    try:
        title, description, keywords, links = crawl(link)

        if title != "" or links != []:
            data.append(
                {
                    "Title": title,
                    "Description": description,
                    "Keywords": keywords,
                    "URL": link
                }
            )

            following_links.remove(link)

            patience -= 1
            if patience >= 0:
                following_links.extend(links)

            elif patience == -1:
                patience = 100
                following_links = [numpy.random.choice(following_links)]
                print()

            print(f"Scraped [{len(data)}/{len(following_links)}]", end="\r")

    except KeyboardInterrupt:
        break

    except Exception as e:
        print(e)

save(data)
