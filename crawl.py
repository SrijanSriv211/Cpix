from colorama import Fore, Style, init
from src.crawler.crawler import crawl, save

# Initialize colorama
init(autoreset = True)

def main(seed, n):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Crawling the web..")
    following_links = [seed]
    data = []

    for i in range(n):
        try:
            link = following_links[i]
            title, description, links = crawl(link, "src\\vendor\\chromedriver-win64\\chromedriver.exe")

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

    print(f"{Fore.YELLOW}{Style.BRIGHT}Saving the crawled data..")
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
    main(link, 300)
