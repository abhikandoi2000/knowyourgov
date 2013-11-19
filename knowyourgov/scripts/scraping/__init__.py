import scraperconfig
import urllib2, json
from bs4 import BeautifulSoup

class Scraper:
	articles = []
	def getArticleLinks(self, search):
		url = self.gcsUrl+'&q='+search
		response = urllib2.urlopen(url)
		jsonResponse = json.loads(response.read())

		for item in jsonResponse["items"]:
			self.articles.append({'url':item["link"]})
	def getArticleContent(self):
		pass

class HinduScraper(Scraper):
	gcsUrl = scraperconfig.customSearchUrl + scraperconfig.searchId['hindu']

	def addArticleContent(self):
		for article in self.articles:
			htmlResponse = urllib2.urlopen(article["url"])
			soup = BeautifulSoup(htmlResponse)

			article["title"] = soup.find("h1", class_="detail-title").text

			article["content"] = "";
			for para in soup.find_all("p", class_="body"):
				article["content"] += para.text

			article["comments"] = [];
			for comment in soup.select("div#comment-section h4"):
				article["comments"].append(comment.text)

	def getArticles(self):
		return self.articles

scrapers = {}
scrapers['hindu'] = HinduScraper()
