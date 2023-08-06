from search_engines.engines import search_engines_dict
from search_engines.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
from search_engines import config
import numpy, json, os

class crawler:
    def __init__(self, search_engines=["google"], filename=config.OUTPUT_DIR+"output", number_of_pages=1):
        self.search_engines = search_engines
        self.filename = filename
        self.number_of_pages = number_of_pages
        self.ignore_duplicates = True
        self.proxy = config.PROXY

    def crawl(self, query):
        timeout = config.TIMEOUT + (10 * bool(self.proxy))
        engines = [e for e in self.search_engines if e in search_engines_dict or e == 'all']
        if 'all' in engines:
            engine = AllSearchEngines(self.proxy, timeout)

        elif len(engines) > 1:
            engine = MultipleSearchEngines(engines, self.proxy, timeout)

        else:
            engine = search_engines_dict[engines[0]](self.proxy, timeout)

        engine.ignore_duplicate_urls = self.ignore_duplicates
        engine.search(query, self.number_of_pages)
        engine.output("json,print", "temp")
        self.__format_result__()

    def __format_result__(self):
        json_file = open(f"temp.json", "r", encoding="utf-8")
        content = json.load(json_file)
        for engine in content["results"]:
            for result in content["results"][engine]:
                site_title = result["title"].split("http")[0]
                site_link = result["link"]
                site_link = site_link[:-1] if site_link.endswith("/") else site_link

                # Write all the links and titles to a file in json manner.
                Pages = open(f"{self.filename}.json", "a", encoding="utf-8")
                Pages.write('{\n')
                Pages.write(f'\t"Title": "{site_title}",\n')
                Pages.write(f'\t"URL": "{site_link}"\n')
                Pages.write('},\n')
                Pages.close()

        # Close the Json file and Delete the temp.json file.
        json_file.close()
        os.remove("temp.json")

# Arrange words in such a way to form a logical sentence.
def arrange_words(tokens):
    """
    A number will represent the number of empty strings in a list.
    For example: 4 -> ["", "", "", ""].
    """

    processed_tokens = []
    for sublist in tokens:
        if isinstance(sublist[-1], int):
            empty_list = [""] * sublist[-1]
            processed_tokens.append(sublist[:-1] + empty_list)

        else:
            processed_tokens.append(sublist)

    # Construct a logical sentence.
    sentence = [numpy.random.choice(i).strip() for i in processed_tokens]
    return " ".join(sentence)

T1 = [
["class"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
["maths", "english", "hindi", "social science", "science", "physics", "chemistry", "biology", "economics", "civics", "history", "geography"],
["chapter"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24" "all"],
["learncbse", "byjus", "vedantu", "tiwari academy", "topper", "brainly", "youtube", "physics wallah", "magnet brains", "unacademy", "pw", "google scholar", "meritnation", "extramarks", "class saathi", "study rankers", "innovative gyan", "jagran josh", "myCBSEguide", "smart study point", "study iq education", "wifistudy", "khan gs research centre", "right to shiksha", 12],
["question answer", "notes", "explanation", "summary", "chapter name", "introduction", "one video", "one shot", "lecture", "in 1 hour", "in 30 minutes", 6]
]

S1 = ""
list_of_queries = []
crawler_engine = crawler(filename="data\\index")
for i in range(2000):
    S1 = " ".join(arrange_words(T1).split())

    if S1 in list_of_queries: continue
    list_of_queries.append(S1)

    print(f"\n{S1}")
    crawler_engine.crawl(S1)
