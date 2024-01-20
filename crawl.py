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
crawl.fetch("https://www.pdfdrive.com/the-purpose-driven-life-what-on-earth-am-i-here-for-e185720921.html")
links = list(set(crawl.links))

for i in links:
    if i.endswith(".html"):
        print(i)

crawl.close()
