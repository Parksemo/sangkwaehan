import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller
import time
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')

# 크롬 연결
chrome_path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(chrome_path)
driver.get('https://www.naver.com')
time.sleep(2)

# 네이버 검색창에 부산 여행 검색
element = driver.find_element_by_name("query")
element.send_keys('부산 여행')
element.submit()
time.sleep(2)

# 스크롤 다운
driver.execute_script("window.scrollTo(0, 2000)")
time.sleep(2)

# 부산 가볼만한 곳 더보기 클릭
driver.find_element_by_xpath('//*[@id="nxTsDo"]/div/div[2]/div/div[5]/div[4]/a').click( )
time.sleep(2)

# 새창 전환
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)

# 가볼만한 곳 크롤링 시작
item_li = driver.find_elements_by_css_selector('._30fe_ ._1bzDV')
장소 = []
for i in range(0, len(item_li)):
    장소.append(item_li[i].text)

# 데이터 프레임으로 만들고 csv파일로 저장
data = pd.DataFrame(장소, columns=['장소'])
data.to_csv("부산여행순위.csv", encoding='utf-8-sig')