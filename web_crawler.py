from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from colorama import Fore, Style, init
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import unicodedata, json

# Initialize colorama
init(autoreset = True)

def crawl(url):
    try:
        # Use Selenium to open the webpage and interact with dynamic content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        service = ChromeService(executable_path = "vendor\chromedriver-win64\chromedriver.exe")  # Set the path to your chromedriver executable
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        # Wait for some time to let the page load dynamically
        driver.implicitly_wait(10)

        # Get the page source after it has loaded dynamically
        page_source = driver.page_source

        # Close the Selenium WebDriver
        driver.quit()

        # Parse the HTML content of the page
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the title of the page
        title = unicodedata.normalize('NFKD', soup.title.text.strip()) if soup.title else ""

        # Extract the meta description of the page
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description_tag['content'].strip() if meta_description_tag else ""

        # Extract all the links (URLs) on the page
        links = []
        for a in soup.find_all("a", href=True):
            if a["href"].startswith("http"):
                links.append(a["href"])

            elif a["href"].startswith("/"):
                links.append(urljoin(url, a["href"]))

        return ("", "", []) if title == "" else (title, meta_description, links)

    except Exception as e:
        print(f"An error occurred: {e}")
        return ("", "", [])

def calculate_pagerank(links, num_iterations=10, damping_factor=0.85):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Page Ranking crawled data..")

    # Initialize PageRank scores
    page_ranks = {link: 1.0 for link in links}

    for _ in range(num_iterations):
        new_page_ranks = {}
        for page in links:
            # Calculate the new PageRank score for each page
            new_page_rank = (1 - damping_factor) + damping_factor * sum(
                page_ranks[link] / len(links) for link in links if page in page_ranks[link]
            )
            new_page_ranks[page] = new_page_rank

        # Update the PageRank scores for the next iteration
        page_ranks = new_page_ranks

    return page_ranks

def save(data):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    with open("data\\index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = []
following_links = [
    "https://github.com/Light-Lens?tab=repositories",
    "https://www.youtube.com/@OnestateCoding/videos",
    "https://stackoverflow.com/users/18121288/light-lens",
    "https://scratch.mit.edu/users/SuperStarIndustries",
    "https://superstar-games.itch.io",
    "https://www.instagram.com/srijansrivastava72",
    "https://uscontent.blogspot.com"
]

print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
for i in range(1000):
    try:
        link = following_links[i]
        title, description, links = crawl(link)

        if title != "":
            data.append(
                {
                    "Title": title,
                    "Description": description,
                    "URL": link
                }
            )

            following_links.extend(links)
            print(f"{Fore.WHITE}{Style.BRIGHT}Scraped [{len(data)}/{len(following_links)}]", end="\r")

    except KeyboardInterrupt:
        print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
        break

    except Exception as e:
        print(e)

# page_ranks = calculate_pagerank(following_links)
# for entry in data:
#     entry["PageRank"] = page_ranks.get(entry["URL"], 0.0)

save(data)
