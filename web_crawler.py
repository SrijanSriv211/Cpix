from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import unicodedata, requests, numpy, json

# Initialize colorama
init(autoreset = True)

def crawl(url):
    try:
        # Check if the URL has a scheme; if not, prepend "https://"
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

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

            # Extract all the links (URLs) on the page
            links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

            return ("", "", []) if title == "" else (title, meta_description, links)

        else:
            with open("crashreport.txt", "a", encoding="utf-8") as f:
                f.write(f"Failed to retrieve {url}. Status code: {response.status_code}\n")

            return ("", "", [])

    except Exception as e:
        with open("crashreport.txt", "a", encoding="utf-8") as f:
            f.write(f"An error occurred: {e}\n")

        return ("", "", [])

def calculate_pagerank(links, num_iterations=10, damping_factor=0.85):
    print(f"{Fore.YELLOW}{Style.BRIGHT}\nCalculating PageRanks..")

    # Initialize PageRank scores
    page_ranks = {link: 1.0 for link in links}

    for _ in range(num_iterations):
        new_page_ranks = {}
        for page in links:
            # Calculate the new PageRank score for each page
            new_page_rank = (1 - damping_factor) + damping_factor * sum(
                page_ranks[link] / len([link for link in links if link in page_ranks]) for link in links if page in page_ranks.get(link, [])
            )
            new_page_ranks[page] = new_page_rank

        # Update the PageRank scores for the next iteration
        page_ranks = new_page_ranks

    return page_ranks

def save(data):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

with open("data\\top-1m.txt", "r", encoding="utf-8") as f:
    following_links = [i.strip() for i in f.readlines()]

# following_links = ["https://www.youtube.com"]
patience, i = 100, 0
data = []

print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
for link in following_links:
    try:
        title, description, links = crawl(link)

        if title != "" or links != []:
            data.append(
                {
                    "Title": title,
                    "Description": description,
                    "URL": link
                }
            )

            # if link in following_links:
            #     following_links.remove(link)

            # patience -= 1
            # if patience >= 0:
            #     following_links.extend(links)

            # elif patience == -1:
            #     patience = 100
            #     following_links = [numpy.random.choice(following_links)]
            #     print()

        print(f"Scraped [{len(data)}/{len(following_links)}]", f"Name: {link}", " " * (len(link) * 2), end="\r")

    except KeyboardInterrupt:
        break

    except Exception as e:
        print(e)

# Calculate PageRank scores
# page_ranks = calculate_pagerank(following_links, 10)
# for entry in data:
#     entry["PageRank"] = page_ranks.get(entry["URL"], 0.0)

save(data)
