#encoding=utf-8
import pymongo
from ddXiaoShuoSpider.items import ChaptersItem
from ddXiaoShuoSpider.items import BookItem,ChapterItem
from scrapy.utils.project import get_project_settings		

class DdxiaoshuospiderPipeline(object):
	
	def __init__(self):
		self.settings = get_project_settings()
		self.client = pymongo.MongoClient(
			host=self.settings['MONGO_HOST'],
			port=self.settings['MONGO_PORT'])
		self.db = self.client[self.settings['MONGO_DB']]
		self.bookColl = self.db[self.settings['MONGO_BOOK_COLL']]
		#self.chapterColl = self.db[self.settings['MONGO_CHAPTER_COLL']]
		self.contentColl = self.db[self.settings['MONGO_CONTENT_COLL']]
	def open_spider(self,spider):
		self.bookColl.remove({"novel_Url":"http://www.23us.so/xiaoshuo/414.html"})	
	#处理书信息
	def process_BookItem(self,item):
		bookItemDick = dict(item)
		try:
			self.bookColl.insert(bookItemDick)
			print("插入小说《%s》的所有信息"%item["novel_Name"])
		except Exception:
			print("小说《%s》已经存在"%item["novel_Name"])
	#处理章节内容
	'''
	def process_ChaptersItem(self,item):
		chapterDick = dict(item)
		try:
			self.chapterColl.insert(chapterDick)
			print("插入一个小说《%s》的所有章节"%item["novel_Name"])
		except Exception:
			print("小说《%s》的章节url已经存在"%item["novel_Name"])
	'''
	#处理每个章节
	def process_ChapterItem(self,item):
		try:
			self.contentColl.insert(dict(item))
			print('插入小说《%s》的章节"%s"'%(item['novel_Name'],item['chapter_Name']))
		except Exception:
			print("%s存在了,跳过"%item["chapter_Name"])
	def process_item(self, item, spider):
		'''
		if isinstance(item,ChaptersItem):
			self.process_ChaptersItem(item)
		'''
		if isinstance(item,BookItem):
			self.process_BookItem(item)
		if isinstance(item,ChapterItem):
			self.process_ChapterItem(item)
		return item
		

