import scrapy
from scrapy import Request
from urllib.parse import quote
from ..items import YbspiderItem
from selenium import webdriver
from selenium.webdriver.support.select import Select


def _getWebDriver():
    chrome_options = webdriver.EdgeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41')  
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    chrome_options.add_experimental_option('useAutomationExtension', False)  
    #打开浏览器
    
    driver = webdriver.ChromiumEdge(options=chrome_options)  
    driver.maximize_window()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })

    return driver


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['code.nhsa.gov.cn']
    url = "https://code.nhsa.gov.cn/toSearch.html?sysflag=1004"
    

    def start_requests(self):
        self.bro = _getWebDriver()
        yield Request(url = self.url, callback = self.parse_first, dont_filter = True)

    def close(self):
        self.bro.quit()

    """
    获取到网页后，需要点击各种按钮执行操作。
    """
    def parse_first(self,response):

        # 第一次进来，要切换页面和点击最大
        # 1. 点击切换按钮        
        self.bro.switch_to.frame(0)
        xpath = '/html/body/section/div/div[1]/label[1]'
        self.bro.find_element('xpath',xpath).click()


        # 2. 点击最大页数
        self.bro.switch_to.frame(0)
        xpath = '//*[@id="gridpage_center"]/table/tbody/tr/td[8]/select'
        sl = Select(self.bro.find_element('xpath',xpath))
        sl.select_by_value('200')

        while True:
            # 处理一下，获取ifrema 后再传递给下一级
            _response = scrapy.http.HtmlResponse(url=self.url, body=self.bro.page_source.encode('utf-8'), status=200)
            # self.parse_content(_response)
            
             # 开始采集数据
            item = YbspiderItem()
            trlist = _response.xpath('//*[@id="gridlist"]/tbody/tr')
            for tr in trlist[1:]:
                item['序号'] = tr.xpath('./td[1]/text()').extract_first()
                item['医用耗材分类代码'] = tr.xpath('./td[3]/text()').extract_first()
                item['三级分类代码'] = tr.xpath('./td[4]/text()').extract_first()
                item['一级_学科_品类'] = tr.xpath('./td[5]/text()').extract_first()
                item['二级_用途_品目'] = tr.xpath('./td[6]/text()').extract_first()
                item['三级_部位_功能_品种'] = tr.xpath('./td[7]/text()').extract_first()
                item['医保通用名代码'] = tr.xpath('./td[8]/text()').extract_first()
                item['医保通用名'] = tr.xpath('./td[9]/text()').extract_first()
                item['材质代码'] = tr.xpath('./td[10]/text()').extract_first()
                item['耗材材质'] = tr.xpath('./td[11]/text()').extract_first()
                item['规格代码'] = tr.xpath('./td[12]/text()').extract_first()
                item['规格_特征_参数'] = tr.xpath('./td[13]/text()').extract_first()

                yield item


            # 下一次进来，就可以点击下一页了
            # 3. 找到下一页
            xpath = '//*[@id="next_gridpage"]'
            ele = self.bro.find_element('xpath',xpath)
            if not ele or 'disabled' in ele.get_attribute('class'):
                break
            else:
                ele.click()


