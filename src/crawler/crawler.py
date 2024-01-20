from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import unicodedata, requests, json

class crawler:
    def __init__(self, path_to_chrome_driver):
        # use Selenium to open the webpage and interact with dynamic content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # run Chrome in headless mode (no GUI)
        options.add_argument('--disable-logging')  # disable logging
        service = ChromeService(executable_path = path_to_chrome_driver) # set the path to your chromedriver executable
        self._driver = webdriver.Chrome(service=service, options=options)
        self.links, self.data = [], []

    # save the data
    def save(self, savepath):
        with open(savepath, "a", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # close the Selenium WebDriver
    def close(self):
        self._driver.quit()

    #NOTE: To be removed later
    def fetch_books(self, url, wait_time=10):
        try:
            self._driver.get(url)

            # wait for some time to let the page load dynamically
            self._driver.implicitly_wait(wait_time)

            # get the page source after it has loaded dynamically
            page_source = self._driver.page_source

            # parse the HTML content of the page
            soup = BeautifulSoup(page_source, "html.parser")

            # extract book
            ignore_chars = """\/:*?"<>|"""
            book_name = soup.find("h1", attrs={"class": "ebook-title"}).text
            formatted_book_name = "".join([i for i in book_name if i not in ignore_chars]) + ".pdf"

            book_id = soup.find("button", attrs={"id": "previewButtonMain"})["data-preview"]
            book_id = book_id.replace("/ebook/preview", "/download.pdf")
            book_id = book_id.replace("&session=", "&h=")
            book_id += "&u=cache&ext=pdf"

            # Send a GET request to the URL
            response = requests.get(f"https://www.pdfdrive.com{book_id}")

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Open the file in binary mode and write the content of the response
                with open(f"data\\books\\{formatted_book_name}", 'wb') as file:
                    file.write(response.content)

                print(f"File downloaded successfully to 'data\\books\\{formatted_book_name}'")

            else:
                print(f"Failed to download file 'data\\books\\{formatted_book_name}'. Status code: {response.status_code}")

            # extract all the links (URLs) on the page
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("http"):
                    self.links.append(a["href"])

                elif a["href"].startswith("/"):
                    self.links.append(urljoin(url, a["href"]))

            # remove duplicate links
            self.links = list(set(self.links))

        except Exception as e:
            print(f"An error occurred: {e}")

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

            # extract the meta description of the page
            meta_description_tag = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description_tag['content'].strip() if meta_description_tag else ""

            # extract all the links (URLs) on the page
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("http"):
                    self.links.append(a["href"])

                elif a["href"].startswith("/"):
                    self.links.append(urljoin(url, a["href"]))

            # remove duplicate links
            self.links = list(set(self.links))

            # append the data
            self.data.append(
                {
                    "Title": title,
                    "Description": meta_description,
                    "URL": url
                }
            )

        except Exception as e:
            print(f"An error occurred: {e}")
