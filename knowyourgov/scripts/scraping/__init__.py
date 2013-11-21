import scraperconfig
import urllib2, json, urllib
from bs4 import BeautifulSoup

class Scraper:
	articles = []
	def getArticleLinks(self, search):
		url = self.gcsUrl+'&q='+urllib.quote(search)
		response = urllib2.urlopen(url)
		jsonResponse = json.loads(response.read())

		for item in jsonResponse["items"]:
			self.articles.append({'url':item["link"], 'imageUrl':item["pagemap"]["cse_image"][0], 'snippet':item["snippet"]})
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

class toiScraper(Scraper):
	gcsUrl = scraperconfig.customSearchUrl + scraperconfig.searchId['toi']

	def addArticleContent(self):
		self.articles.pop(0)
		for article in self.articles:
			htmlResponse = urllib2.urlopen(article["url"])
			soup = BeautifulSoup(htmlResponse)
			title = soup.find("h1", class_="multi-line-title-1")
			if title:
				article["title"] = title.text
			article["content"] = "";
			content = soup.select("div.mod-articletext p")
			if content:
				for para in content:
					article["content"] += para.text

			article["comments"] = []
			containerDiv = soup.find("div", id="mod-readers-comment")
			if containerDiv:
				commentsUrl = containerDiv.iframe['src']
				if commentsUrl:
					commentsUrl = commentsUrl.replace('pmcomment', 'opinions')
					htmlResponse = urllib2.urlopen(commentsUrl)
					soup = BeautifulSoup(htmlResponse)
					comments = soup.find_all("span", class_="replybtn")
					if comments:
						for comment in comments:
							article["comments"].append(comment.previousSibling.text)
				break	




	def getArticles(self):
		return self.articles

scrapers = {}
scrapers['hindu'] = HinduScraper()
scrapers['toi'] = toiScraper()
