from search_engines.engines import search_engines_dict
from search_engines.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
from search_engines import config

class crawler:
    def __init__(self, query, search_engines=["google"], output="print", outfilename=config.OUTPUT_DIR+"output", number_of_pages=1, filer_results=[], ignore_duplicates=True, proxy=config.PROXY):
        self.query = query
        self.search_engines = search_engines
        self.output = output
        self.outfilename = outfilename
        self.number_of_pages = number_of_pages
        self.filer_results = filer_results
        self.ignore_duplicates = ignore_duplicates
        self.proxy = proxy

    def crawl(self):
        timeout = config.TIMEOUT + (10 * bool(self.proxy))
        engines = [e for e in self.search_engines if e in search_engines_dict or e == 'all']
        if not engines:
            print('Please choose a search engine: ' + ', '.join(search_engines_dict))

        else:
            if 'all' in engines:
                engine = AllSearchEngines(self.proxy, timeout)

            elif len(engines) > 1:
                engine = MultipleSearchEngines(engines, self.proxy, timeout)

            else:
                engine = search_engines_dict[engines[0]](self.proxy, timeout)

            engine.ignore_duplicate_urls = self.ignore_duplicates
            if self.filer_results:
                engine.set_search_operator(self.filer_results)

            engine.search(self.query, self.number_of_pages)
            engine.output(self.output, self.outfilename)

crawler_engine = crawler("google", number_of_pages=config.SEARCH_ENGINE_RESULTS_PAGES)
crawler_engine.crawl()
