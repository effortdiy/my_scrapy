from scrapy import cmdline
import os,sys
dirpath=os.path.dirname(os.path.abspath(__file__))
# 获取当前路径
os.chdir(dirpath)
cmdline.execute(['scrapy','crawl','main'])