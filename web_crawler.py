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
        service = ChromeService(executable_path = "vendor\\chromedriver-win64\\chromedriver.exe")  # Set the path to your chromedriver executable
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

def save(data):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    with open("data\\index.json", "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main(seed, n):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
    following_links = [seed]
    data = []

    for i in range(n):
        try:
            link = following_links[i]
            title, description, links = crawl(link)

            if title == "":
                continue

            data.append(
                {
                    "Title": title,
                    "Description": description,
                    "PageRank": 0,
                    "URL": link
                }
            )

            following_links.extend(links)

        except KeyboardInterrupt:
            print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
            break

        except Exception as e:
            print(e)

    save(data)

links = [
    "https://github.com/Light-Lens?tab=repositories",
    "https://www.youtube.com/@OnestateCoding/videos",
    "https://stackoverflow.com/users/18121288/light-lens",
    "https://scratch.mit.edu/users/SuperStarIndustries",
    "https://superstar-games.itch.io",
    "https://www.instagram.com/srijansrivastava72",
    "https://uscontent.blogspot.com"
]

for link in links:
    main(link, 5000)
