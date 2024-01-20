from colorama import Fore, Style, init
from src.crawler.crawler import crawler
from bs4 import BeautifulSoup

# Initialize colorama
init(autoreset = True)

def main(url, n):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
    crawl =  crawler("src\\vendor\\chromedriver-win64\\chromedriver.exe")
    links = [url]

    for i in range(n):
        try:
            crawl.fetch(links[i])
            links.extend(list(set(crawl.links)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
            break

        except Exception as e:
            print(e)

    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    crawl.save("data\\index.json")

# links = [
#     "https://github.com/Light-Lens?tab=repositories",
#     "https://www.youtube.com/@OnestateCoding/videos",
#     "https://stackoverflow.com/users/18121288/light-lens",
#     "https://scratch.mit.edu/users/SuperStarIndustries",
#     "https://superstar-games.itch.io",
#     "https://www.instagram.com/srijansrivastava72",
#     "https://uscontent.blogspot.com"
# ]

# for link in links:
#     main(link, 300)

# Download books
crawl =  crawler("src\\vendor\\chromedriver-win64\\chromedriver.exe")
crawl.fetch("https://www.pdfdrive.com/sapiens-a-brief-history-of-humankind-e175870479.html", wait_time=2)
links = [i for i in list(set(crawl.links)) if i.endswith(".html")]

for link in links:
    crawl.fetch_books(link, wait_time=2)
    if len(links) - 1 <= 1e6:
        links.extend([i for i in list(set(crawl.links)) if i.endswith(".html")])

crawl.close()
