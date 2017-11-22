#encoding=utf-8
from scrapy import signals
from scrapy import http
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import pymongo
from scrapy.utils.project import get_project_settings
import re

class DdxiaoshuospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except

        # Must return only requests (not items).
        for r in start_requests:
            yield r

class UrlFilter(object):
	#初始化过滤器（使用mongodb过滤）
	def __init__(self):
		self.settings = get_project_settings()
		self.client = pymongo.MongoClient(
			host = self.settings['MONGO_HOST'],
			port = self.settings['MONGO_PORT'])
		self.db = self.client[self.settings['MONGO_DB']]
		self.bookColl = self.db[self.settings['MONGO_BOOK_COLL']]
		#self.chapterColl = self.db[self.settings['MONGO_CHAPTER_COLL']]
		self.contentColl = self.db[self.settings['MONGO_CONTENT_COLL']]
	def regexfilter(self,url,regex):
		if re.match(regex,url):
			return True
	def process_request(self,request,spider):
		if (self.regexfilter(request.url,".*?files/article/html/\d*?/\d*?/\d*?.html")):
			print("跳过##################")
			return  http.Response(url=request.url,body=None)
		if (self.bookColl.count({"novel_Url":request.url}) > 0) or (self.contentColl.count({"chapter_Url":request.url}) > 0):
			return http.Response(url=request.url,body=None)
				

class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
				
