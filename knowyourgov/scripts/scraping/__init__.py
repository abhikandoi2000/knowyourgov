import scraperconfig
import urllib2, json, urllib, re
from bs4 import BeautifulSoup

class Scraper:
	articles = []
	def getArticleLinks(self, search):
		url = self.gcsUrl+'&q='+urllib.quote(search)
		response = urllib2.urlopen(url)
		jsonResponse = json.loads(response.read())

		for item in jsonResponse["items"]:
			self.articles.append({'url':item["link"], 'imageUrl':item["pagemap"]["cse_image"][0], 'snippet':item["snippet"]})

	def getArticles(self):
		return self.articles

	def getArticleContent(self):
		pass


class HinduScraper(Scraper):
	gcsUrl = scraperconfig.customSearchUrl + scraperconfig.searchId['hindu']

	def addArticleContent(self):
		for article in self.articles:
			htmlResponse = urllib2.urlopen(article["url"])
			soup = BeautifulSoup(htmlResponse)

			title = soup.find("h1", class_="detail-title").text
			if title:
				article["title"] = title.text

			article["content"] = "";
			for para in soup.find_all("p", class_="body"):
				article["content"] += para.text

			article["comments"] = [];
			for comment in soup.select("div#comment-section h4"):
				article["comments"].append(comment.text)

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

class india60Scraper(Scraper):
	baseUrl = "http://india60.com/mps/list.php?page="
	links = []

	def getArticleLinks(self, search):
		pass
	def getArticles(self):
		pass
	def getArticleContent(self):
		pass
	def getPoliticianLinks(self):
		page = 1
		linksFile = open('india60links.txt', 'w')
		while page < 12:
			url = self.baseUrl + str(page)
			page += 1
			htmlResponse = urllib2.urlopen(url)
			soup = BeautifulSoup(htmlResponse)
			for politician in soup.find_all("ul", class_="mpinfo"):
				link = politician.find('a')['href']
				linksFile.write(link+"\n")

	def getPoliticianData(self, url):
		htmlResponse = urllib2.urlopen(url)
		pol = {}
		soup = BeautifulSoup(htmlResponse)
		ele = soup.select('div.listtitle2 h1')
		pol['constituency'] = ele[2].text[14:]

		for li in soup.find('div', class_="wealth").find_all('li'):
			divs = li.find_all('div')
			attr = removeNonAlphanumeric(divs[0].text)
			value = removeNonAlphanumeric(divs[1].text)
			pol[attr] = value

		return pol

def removeNonAlphanumeric(string):
	return re.sub(r'[^a-zA-Z0-9]','', string)

scrapers = {}
scrapers['hindu'] = HinduScraper()
scrapers['toi'] = toiScraper()
scrapers['india60'] = india60Scraper()
