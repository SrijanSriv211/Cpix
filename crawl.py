from colorama import Fore, Style, init
from src.crawler.crawler import crawler
import json, os

# Initialize colorama
init(autoreset = True)

def main(url, n, savepath="data\\index.json"):
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

    print(f"{Fore.YELLOW}{Style.BRIGHT}Closing the crawler..")
    crawl.close()

    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
    crawl.save()

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
crawl.fetch_books("https://www.pdfdrive.com/ncert-class-10-history-e27066083.html", wait_time=2)
links = [i for i in list(set(crawl.links)) if i.endswith(".html")]

for link in links:
    crawl.fetch_books(link, wait_time=2)
    if len(links) - 1 <= 1e6:
        links.extend([i for i in list(set(crawl.links)) if i.endswith(".html")])

crawl.close()
