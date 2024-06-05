from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import unicodedata, json

class crawler:
    def __init__(self, path_to_chrome_driver):
        # use Selenium to open the webpage and interact with dynamic content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # run Chrome in headless mode (no GUI)
        options.add_argument('--log-level=3')  # suppress logging output of the WebDriver

        service = ChromeService(executable_path = path_to_chrome_driver) # set the path to your chromedriver executable
        self._driver = webdriver.Chrome(service=service, options=options)
        self.links, self.data = [], []
        self.url_to_data = {}  # hash table to map URLs to their data

    # close the Selenium WebDriver
    def close(self):
        self._driver.quit()

    # save the data
    def save(self, savepath):
        with open(savepath, "a", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def fetch(self, url, wait_time=10):
        try:
            self._driver.get(url)

            # wait for some time to let the page load dynamically
            self._driver.implicitly_wait(wait_time)

            # get the page source after it has loaded dynamically
            page_source = self._driver.page_source

            # parse the HTML content of the page
            soup = BeautifulSoup(page_source, "html.parser")

            # extract the title of the page
            title = unicodedata.normalize('NFKD', soup.title.text.strip()) if soup.title else ""
            if title == "":
                return

            # extract all the links (URLs) on the page
            links = []
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("http"):
                    links.append(a["href"])

                elif a["href"].startswith("/"):
                    links.append(urljoin(url, a["href"]))
            links = list(set(links))

            # extract and normalize all text from the body of the page
            body = soup.body
            body_text = unicodedata.normalize('NFKD', ' '.join(body.stripped_strings)) if body else ""

            # remove duplicate links
            for link in links:
                # check if URL already exists in the hash table
                if link in self.url_to_data:
                    self.url_to_data[link]['PageRank'] += 1

                else:
                    self.links.append(link)

            # check if URL already exists in the hash table
            # Resolve the canonical URL
            if url in self.url_to_data:
                self.url_to_data[url]['PageRank'] += 1

            else:
                # create the new data entry
                new_data = {
                    "Title": title,
                    "BodyText": body_text,
                    "PageRank": 0,
                    "URL": url
                }

                # append the new data to the list and hash table
                self.data.append(new_data)
                self.url_to_data[url] = new_data
        
        except WebDriverException:
            print("There is some problem with the page.\n")

        except Exception as e:
            print(e)
