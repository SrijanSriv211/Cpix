from colorama import Fore, Style, init
from src.crawler.crawler import crawler
import json, os

# Initialize colorama
init(autoreset = True)

crawl =  crawler("src\\vendor\\chromedriver-win64\\chromedriver.exe")
def main(url, n):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
    links = [url]

    for i in range(n):
        try:
            crawl.fetch(links[i], wait_time=5)
            links.extend(list(set(crawl.links)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
            break

        except Exception as e:
            print(e)


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
    main(link, 300)

print(f"{Fore.YELLOW}{Style.BRIGHT}Closing the crawler..")
crawl.close()

print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
crawl.save("data\\index.json")
