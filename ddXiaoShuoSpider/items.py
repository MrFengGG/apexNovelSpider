#coding: utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
		_id = scrapy.Field()
		novel_Name = scrapy.Field()
		novel_Writer = scrapy.Field()
		novel_Type = scrapy.Field()
		novel_Status = scrapy.Field()
		novel_UpdateTime = scrapy.Field()
		novel_Words = scrapy.Field()
		novel_ImageUrl = scrapy.Field()
		novel_AllClick = scrapy.Field()
		novel_MonthClick = scrapy.Field()
		novel_WeekClick = scrapy.Field()
		novel_AllComm = scrapy.Field()
		novel_MonthComm = scrapy.Field()
		novel_WeekComm = scrapy.Field()
		novel_Url = scrapy.Field()
		novel_Introduction = scrapy.Field()

class ChaptersItem(scrapy.Item):
		chapters_Url = scrapy.Field()
		_id = scrapy.Field()
		novel_Chapters = scrapy.Field()
		novel_Name = scrapy.Field()
	
class ChapterItem(scrapy.Item):
		chapter_Url = scrapy.Field()
		_id = scrapy.Field()
		novel_Name = scrapy.Field()
		chapter_Name = scrapy.Field()
		chapter_Content = scrapy.Field()
		novel_ID = scrapy.Field()
		is_Error = scrapy.Field()
