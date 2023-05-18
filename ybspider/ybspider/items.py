# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YbspiderItem(scrapy.Item):
    序号 = scrapy.Field()
    医用耗材分类代码 = scrapy.Field()
    三级分类代码 = scrapy.Field()
    一级_学科_品类= scrapy.Field()
    二级_用途_品目	 = scrapy.Field()
    三级_部位_功能_品种	 = scrapy.Field()
    医保通用名代码	 = scrapy.Field()
    医保通用名	 = scrapy.Field()
    材质代码	 = scrapy.Field()
    耗材材质	 = scrapy.Field()
    规格代码	 = scrapy.Field()
    规格_特征_参数= scrapy.Field()

