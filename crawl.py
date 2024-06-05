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
        links = list(set(links))

    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}\nStopping..")
        print(e)

with open("data\\top-1m.txt", "r", encoding="utf-8") as f:
    links = f.readlines()

for link in links:
    try:
        main(link.strip())

    except KeyboardInterrupt:
        break

print(f"{Fore.YELLOW}{Style.BRIGHT}Closing the crawler..")
crawl.close()

print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
crawl.save("data\\index.json")
