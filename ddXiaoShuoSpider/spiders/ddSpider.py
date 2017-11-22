#coding=UTF-8
import scrapy
import urlparse
import re
from bs4 import BeautifulSoup
import sys
import re
from ddXiaoShuoSpider.items import ChaptersItem,BookItem,ChapterItem
#将其他组件加入路径中
sys.path.append("/usr/local/python2Demo/scrapyDemo/ddXiaoShuoSpider/ddXiaoShuoSpider") 
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html
import zlib

class ddSpider(CrawlSpider):
	name = "ddxiaoshuo"
	allowed_domains = ["23us.so"]
	start_urls = ["http://www.23us.so/xiaoshuo/414.html"]
	rules=(
		Rule(LinkExtractor(allow=("xiaoshuo/\d*\.html")),callback="parse_book_message",follow=True),
		Rule(LinkExtractor(allow=("files/article/html/\d*?/\d*?.index.html")),callback="parse_book_chapter",follow=True),
		#Rule(LinkExtractor(deny=("files/article/html/\d*?/\d*?/\d*?.html")),callback="parse_chapter_content_",follow=True),
		Rule(LinkExtractor(allow=(".*")),follow=True),
	)	
	#解析小说信息页面
	def parse_book_message(self,response):
		if not response.body:
			print(response.url+"已经被爬取过了，跳过")
			return;
		ht = response.body.decode("utf-8")	
		text = html.fromstring(ht)
		novel_Url = response.url
		novel_Name = text.xpath(".//dl[@id='content']/dd[1]/h1/text()")[0].split(" ")[0] if response.xpath(".//dl[@id='content']/dd[1]/h1/text()") else "None"
		novel_ImageUrl = text.xpath(".//a[@class='hst']/img/@src")[0] if response.xpath(".//a[@class='hst']/img/@src") else "None"
		novel_ID = int(response.url.split("/")[-1].split(".")[0]) if response.url.split("/")[-1].split(".") else "None"
		novel_Type = text.xpath(".//table[@id='at']/tr[1]/td[1]/a/text()") if response.xpath(".//table[@id='at']/tr[1]/td[1]/a/text()") else "None"
		novel_Writer = "".join(text.xpath(".//table[@id='at']/tr[1]/td[2]/text()")) if response.xpath(".//table[@id='at']/tr[1]/td[2]/text()") else "None"
		novel_Status = "".join(text.xpath(".//table[@id='at']/tr[1]/td[3]/text()")) if response.xpath(".//table[@id='at']/tr[1]/td[3]/text()") else "None"
		novel_Words = self.getNumber("".join(text.xpath(".//table[@id='at']/tr[2]/td[2]/text()"))) if response.xpath(".//table[@id='at']/tr[2]/td[2]/text()") else "None"
		novel_UpdateTime = "".join(text.xpath(".//table[@id='at']/tr[2]/td[3]/text()")) if response.xpath(".//table[@id='at']/tr[2]/td[3]/text()") else "None"
		novel_AllClick = int("".join(text.xpath(".//table[@id='at']/tr[3]/td[1]/text()"))) if response.xpath(".//table[@id='at']/tr[3]/td[1]/text()") else "None"
		novel_MonthClick = int("".join(text.xpath(".//table[@id='at']/tr[3]/td[2]/text()"))) if response.xpath(".//table[@id='at']/tr[3]/td[2]/text()") else "None"
		novel_WeekClick = int("".join(text.xpath(".//table[@id='at']/tr[3]/td[3]/text()"))) if response.xpath(".//table[@id='at']/tr[3]/td[3]/text()") else "None"
		novel_AllComm = int("".join(text.xpath(".//table[@id='at']/tr[4]/td[1]/text()"))) if response.xpath(".//table[@id='at']/tr[4]/td[1]/text()") else "None"
		novel_MonthComm = int("".join(text.xpath(".//table[@id='at']/tr[4]/td[3]/text()"))) if response.xpath(".//table[@id='at']/tr[4]/td[2]/text()") else "None"
		novel_WeekComm = int("".join(text.xpath(".//table[@id='at']/tr[4]/td[3]/text()"))) if response.xpath(".//table[@id='at']/tr[4]/td[3]/text()") else "None"
		pattern = re.compile('<p>(.*)<br')
		match = pattern.search(ht)
		novel_Introduction = "".join(match.group(1).replace("&nbsp;","")) if match else "None"
		#封装小说信息类
		bookitem = BookItem(
					novel_Type = novel_Type[0],
					novel_Name = novel_Name,
					novel_ImageUrl = novel_ImageUrl,
					_id = novel_ID,   #小说id作为唯一标识符
					novel_Writer = novel_Writer,
					novel_Status = 1 if novel_Status.find("连载") >= 0 else 0,
					novel_Words = novel_Words,
					novel_UpdateTime = novel_UpdateTime,
					novel_AllClick = novel_AllClick,
					novel_MonthClick = novel_MonthClick,
					novel_WeekClick = novel_WeekClick,
					novel_AllComm = novel_AllComm,
					novel_MonthComm = novel_MonthComm,
					novel_WeekComm = novel_WeekComm,
					novel_Url = novel_Url,
					novel_Introduction = novel_Introduction,
		)
		return bookitem
	def getNumber(self,numberStr):
		formart = '01234567890'
		result = numberStr
		for numstr in numberStr:
			if not numstr in formart:
				result = result.replace(numstr,'');
		return int("".join(result))
		
	#解析小说章节信息
	def parse_book_chapter(self,response):
		'''
		if not response.body:
			print(response.url+"已经被爬取过了，不发送请求")
			return;
		text = html.fromstring(response.body.decode("utf-8"))
		novel_ID = response.url.split("/")[-2]
		novel_Name = text.xpath(".//p[@class='fr']/following-sibling::a[3]/text()")[0]
		chapter_Elements = text.xpath(".//table[@id='at']//td/a")
		chapters=[]
		for chapter_Element in chapter_Elements:
			chapter_Name = chapter_Element.xpath("text()")
			chapter_Url = chapter_Element.xpath("@href")
			chapter = (chapter_Name,chapter_Url)
			chapters.append(chapter)
		chaptersItem = ChaptersItem(
							chapters_Url = response.url,
							_id=novel_ID,
							novel_Chapters=chapters,
							novel_Name=novel_Name)
		return chaptersItem
		'''
		pass
	def parse_chapter_content(self,response):
		if not response.body:
			print(response.url+"已经被爬取过了，跳过")
			return;
		ht = response.body.decode('utf-8')
		text = html.fromstring(ht)
		soup = BeautifulSoup(ht)
		novel_ID = response.url.split("/")[-2]
		novel_Name = text.xpath(".//p[@class='fr']/following-sibling::a[3]/text()")[0]
		chapter_Name = text.xpath(".//h1[1]/text()")[0]
		'''
		chapter_Content = "".join("".join(text.xpath(".//dd[@id='contents']/text()")).split())
		if len(chapter_Content) < 25:
			chapter_Content = "".join("".join(text.xpath(".//dd[@id='contents']//*/text()")))
		pattern = re.compile('dd id="contents".*?>(.*?)</dd>')
		match = pattern.search(ht)
		chapter_Content = "".join(match.group(1).replace("&nbsp;","").split()) if match else "爬取错误"
		'''
		result,number = re.subn("<.*?>","",str(soup.find("dd",id='contents')))
		chapter_Content = "".join(result.split())
		print(len(chapter_Content))
		novel_ID = response.url.split("/")[-2]
		return ChapterItem(
					chapter_Url = response.url,
					_id=int(response.url.split("/")[-1].split(".")[0]),
					novel_Name=novel_Name,
					chapter_Name=chapter_Name,
					chapter_Content= chapter_Content,
					novel_ID = novel_ID,
					is_Error = len(chapter_Content) < 3000
					)
		def parse_chapter_content_(self,response):
			print("跳过########################")
