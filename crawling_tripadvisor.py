# ----------------------------------------------------------
# 트립어드바이저 크롤링 함수
# ----------------------------------------------------------

import numpy as np
import pandas as pd
import csv

from selenium import webdriver
import chromedriver_autoinstaller

from tqdm import tqdm, tqdm_notebook
from tqdm.notebook import tqdm
import re
from time import sleep
import time
import warnings
warnings.filterwarnings('ignore')
import random
import pickle
t=random.choice([3,4,5])

# 부산 가볼만한 곳 순위 불러오기
data = pd.read_csv('부산여행순위.csv')
tourist_attractions_list = np.array(data.장소)[:5]

# 트립어드바이저 웹 크롤링 함수
def 리뷰크롤링(key):
    # 크롬 접속
    chrome_path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(chrome_path)
    time.sleep(3)

    # 위치 찾기
    try:
        driver.get("https://www.tripadvisor.co.kr/")
        time.sleep(5)
        find = driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[3]/div/div/div/form/input[1]')
        driver.implicitly_wait(10)
        find.send_keys(key)
        time.sleep(7)
        find.submit()#엔터
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[1]').click()
        driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
    except:
        driver.get("https://www.tripadvisor.co.kr/")
        time.sleep(5)
        find = driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[3]/div/div/div/form/input[1]')
        driver.implicitly_wait(10)
        find.send_keys(key)
        time.sleep(7)
        find.submit()#엔터
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[1]').click()
        driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)

    # 파일 이름 저장
    file_name = driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text
    
    # 크롤링
    out_re = []
    c = True
    while c:   
        try:
            driver.execute_script("window.scrollTo(0, 5500)")
            driver.implicitly_wait(t)
            for j in tqdm(range(1,11)):
                try:
                    review = [driver.find_element_by_xpath(f'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[{j}]/span/div/div[5]/div[1]/div/span').text
                           ,driver.find_element_by_xpath(f'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[{j}]/span/div/div[2]/*[name()="svg"]').get_attribute('aria-label')
                           ]
                    review[1] = review[1].replace('풍선 5개 중 ','')
                    reviews = driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[3]/span/div/div[1]/div[2]/span').text
                    reviews = reviews.replace("리뷰 ","").replace("건","")
                    out_re.append(review)                    
                except:
                    break
            driver.implicitly_wait(t)
            element = driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[10]/span/div')
            driver.execute_script('arguments[0].scrollIntoView(true);', element)
            driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a/*[name()="svg"]').click()
            driver.implicitly_wait(t)
        except:
            c = False

    # pickle로 저장
    리뷰크롤링_리뷰수 = {}
    리뷰크롤링_리뷰수['리뷰'] = out_re
    리뷰크롤링_리뷰수['리뷰수']  = reviews
    with open(f"{file_name}_.pickle","wb") as fw:
        pickle.dump(리뷰크롤링_리뷰수, fw)        

# 가볼만한 곳 리스트의 장소들로 트립어드바이저 검색
for name in tourist_attractions_list:
    리뷰크롤링(name)