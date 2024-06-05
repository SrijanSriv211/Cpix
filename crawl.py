from colorama import Fore, Style, init
from src.crawler.crawler import crawler

# Initialize colorama
init(autoreset = True)

crawl =  crawler("src\\vendor\\chromedriver-win64\\chromedriver.exe")
def main(url):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
    links = [url]

    try:
        crawl.fetch(url, wait_time=5)
        crawled_links = list(set(crawl.links))
        links.extend(crawled_links)

    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
        print(e)

with open("data\\top-1m.txt", "r", encoding="utf-8") as f:
    links = f.readlines()

# links = [
#     "https://github.com/Light-Lens?tab=repositories",
#     "https://www.youtube.com/@OnestateCoding/videos",
#     "https://stackoverflow.com/users/18121288/light-lens",
#     "https://scratch.mit.edu/users/SuperStarIndustries",
#     "https://superstar-games.itch.io",
#     "https://www.instagram.com/srijansrivastava72",
#     "https://uscontent.blogspot.com"
# ]

for link in links:
    try:
        main(f"https://{link.strip()}")

    except KeyboardInterrupt:
        break

print(f"{Fore.YELLOW}{Style.BRIGHT}Closing the crawler..")
crawl.close()

print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
crawl.save("data\\index.json")
