from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import csv


class ybSelenum:
  URL = "https://code.nhsa.gov.cn/toSearch.html?sysflag=1004"

  def __init__(self) -> None:
      self.bro = self._get_webDriver()

  def __del__(self) -> None:
      if self.bro :
          self.bro.quit()

  def _get_webDriver(self):
      chrome_options = webdriver.EdgeOptions()
      chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41')  
      chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  
      chrome_options.add_experimental_option('useAutomationExtension', False)  
      #打开浏览器
      
      bro = webdriver.ChromiumEdge(options=chrome_options)  

      # with open('./lib/stealth.min.js') as f:
      #     source_js = f.read()
      #     bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      #         "source": source_js
      #     })
      bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
              Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
              })
            """
          })
      return bro

  def parse_main(self):
      
      # 开始请求网站
      self.bro.get(self.URL)
      time.time(5)

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
          xpath = '//*[@id="gridlist"]'
          table = self.bro.find_element('xpath',xpath)
          contents = table.text
          for row in contents.split('\n'):
            cols = row.split(' ')
            yield cols

          # 下一次进来，就可以点击下一页了
          # 3. 找到下一页
          xpath = '//*[@id="next_gridpage"]'
          ele = self.bro.find_element('xpath',xpath)
          if not ele or 'disabled' in ele.get_attribute('class'):
              break
          else:
              ele.click()

      print('数据已拿完，浏览器正在退出！')
      self.bro.quit()
      bro =None

    
if __name__ == '__main__':
    file = './main.csv'
    ybsel = ybSelenum()
    with open(file,'+w',encoding='utf8',newline='') as f:        
      csv_writer = csv.writer(f)
      csv_writer.writerow(['医用耗材分类代码','三级分类代码','一级（学科、品类）','二级（用途、品目）','三级（部位、功能、品种）','医保通用名代码','医保通用名','材质代码','耗材材质','规格代码','规格（特征、参数）'])
      for item in ybsel.parse_main():
        csv_writer.writerow(item)