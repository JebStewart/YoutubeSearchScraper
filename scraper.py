from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import webbrowser
import pandas as pd
import re 
DRIVER_PATH = r'C:\Users\jebli\AppData\Roaming\Python\Scraping\chromedriver.exe'

class YoutubeScraper:
    def __init__(self):
        """This tool is used to get titles and thumbnails from a search on youtube"""
        #options = Options()
        #options.headless=headless
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.search_start = 'https://www.youtube.com/results?search_query='
        self.query = []
        self.titles = []
        self.clean_titles = []
        self.df = pd.DataFrame()

    def search(self, search_term):
        full_path = self.search_start+search_term
        self.driver.get(full_path)

    def _get_titles(self):
        results = self.driver.find_elements_by_id('video-title')
        self.titles = self.titles + [result.text for result in results]
        return len(results)

    def get_titles(self):
      self._get_titles()
      return self.titles

    def _sanitize_titles(self):
      if len(self.titles) ==0:
        self._get_titles()
      self.clean_titles = self.clean_titles + [self._clean_(title) for title in self.titles]

    def _clean_(self, title):
      """Takes string and returns only words with alpha characters"""
      title = re.sub(r'[^A-Za-z ]+', '', title)
      return title.lower()

    def get_clean_titles(self):
      self._sanitize_titles()
      return self.clean_titles

    def end_session(self):
      self.driver.quit()

    def RUN(self, queries):
      """Build data frame from list of queries and sanitize results"""
      for query in queries:
        self.search(query)
        num_of_results = self._get_titles()
        self.query = self.query + ([query]*num_of_results)
      self._sanitize_titles
      self.df['Query'] = self.query
      self.df['Titles'] = self.titles
      self.df['Clean_Titles'] = self.df['Titles'].apply(lambda x: self._clean_(x))
      self.end_session()
      return self.df

if __name__=='__main__':
    yts = YoutubeScraper()
    result = yts.RUN(['crypto', 'crossfit'])
    print(result.head())
"""
Notes
Title element
<a id="video-title" class="yt-simple-endpoint style-scope ytd-video-renderer" title="Top 9 “SLEEPING GIANT” Cryptocurrency Altcoin Projects! Best DeFi Investments 2021 | Crypto News" href="/watch?v=GC8uO_2tcfE" aria-label="Top 9 “SLEEPING GIANT” Cryptocurrency Altcoin Projects! Best DeFi Investments 2021 | Crypto News by Altcoin Daily 20 hours ago 12 minutes, 5 seconds 68,886 views">
            <yt-icon id="inline-title-icon" class="style-scope ytd-video-renderer" hidden=""><!--css-build:shady--></yt-icon>
            <yt-formatted-string class="style-scope ytd-video-renderer" aria-label="Top 9 “SLEEPING GIANT” Cryptocurrency Altcoin Projects! Best DeFi Investments 2021 | Crypto News by Altcoin Daily 20 hours ago 12 minutes, 5 seconds 68,886 views">Top 9 “SLEEPING GIANT” Cryptocurrency Altcoin Projects! Best DeFi Investments 2021 | Crypto News</yt-formatted-string>
          </a>

Thumbnail
<a id="thumbnail" class="yt-simple-endpoint inline-block style-scope ytd-thumbnail" aria-hidden="true" tabindex="-1" rel="null" href="/watch?v=GC8uO_2tcfE">
  <yt-img-shadow ftl-eligible="" class="style-scope ytd-thumbnail no-transition" style="background-color: transparent;" loaded=""><!--css-build:shady--><img id="img" class="style-scope yt-img-shadow" alt="" width="360" src="https://i.ytimg.com/vi/GC8uO_2tcfE/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&amp;rs=AOn4CLAv0s5mIrCQPvoONjqW-aJ6-YKZ2Q"></yt-img-shadow>
  
  <div id="overlays" class="style-scope ytd-thumbnail"><ytd-thumbnail-overlay-time-status-renderer class="style-scope ytd-thumbnail" overlay-style="DEFAULT"><!--css-build:shady--><yt-icon class="style-scope ytd-thumbnail-overlay-time-status-renderer" disable-upgrade="" hidden=""></yt-icon><span id="text" class="style-scope ytd-thumbnail-overlay-time-status-renderer" aria-label="12 minutes, 5 seconds">
  12:05
</span></ytd-thumbnail-overlay-time-status-renderer><ytd-thumbnail-overlay-now-playing-renderer class="style-scope ytd-thumbnail"><!--css-build:shady--><span class="style-scope ytd-thumbnail-overlay-now-playing-renderer">Now playing</span>
<ytd-thumbnail-overlay-equalizer class="style-scope ytd-thumbnail-overlay-now-playing-renderer"><!--css-build:shady--><svg xmlns="http://www.w3.org/2000/svg" id="equalizer" viewBox="0 0 55 95" class="style-scope ytd-thumbnail-overlay-equalizer">
  <g class="style-scope ytd-thumbnail-overlay-equalizer">
    <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="0"></rect>
    <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="20"></rect>
    <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="40"></rect>
  </g>
</svg>
</ytd-thumbnail-overlay-equalizer>
</ytd-thumbnail-overlay-now-playing-renderer></div>
  <div id="mouseover-overlay" class="style-scope ytd-thumbnail"></div>
  <div id="hover-overlays" class="style-scope ytd-thumbnail"></div>
</a>
"""