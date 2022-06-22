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
t=random.choice([1,2,3])
tt=random.choice([7,9,11])

def 구글크롤링(key):
    
    #크롬 구글맵url불러오기
    chrome_path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(chrome_path)
    time.sleep(3)
    driver.get("https://www.google.co.kr/maps/?hl=ko")
    driver.implicitly_wait(10)
    
    #검색어지정
    find = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    find.send_keys(f"{key}")
    driver.implicitly_wait(tt)
    
    #검색하기
    driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click()
    time.sleep(t)
    try:
        try:
            driver.find_element_by_css_selector('.Nv2PK.Q2HXcd.THOPZb .hfpxzc').click()
        except:
            driver.find_element_by_css_selector('.Nv2PK.THOPZb.CpccDe .hfpxzc').click()
        검색지명 = driver.find_element_by_css_selector('.tAiQdd .lMbq3e .DUwDvf.fontHeadlineLarge').text    
        driver.implicitly_wait(tt)
        try:
            driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]')
        except:
            driver.close()

        #리뷰더보기
        try:
            element = driver.find_element_by_css_selector('#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf')
            time.sleep(t)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element)
            time.sleep(t)
            element = driver.find_elements_by_css_selector(".m6QErb.Hk4XGb.QoaCgb.KoSBEe.tLjsW .M77dve")
            if len(element) < 2:
                driver.execute_script("arguments[0].click();", element[0])
                time.sleep(t)
            else:
                driver.execute_script("arguments[0].click();", element[1])
                time.sleep(t)
        except:
            try:
                driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button').click()
            except:
                driver.close()
                
        #스크롤100번 내리기
        try:
            리뷰총수 = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text
        except:
            try:
                리뷰총수 = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]').text
            except:
                driver.close()
        페이지카운트 = 100
        try:
            리뷰총수 = 리뷰총수.replace("리뷰 ","").replace("개","").replace(',',"")
        except:
            리뷰총수 = 리뷰총수.replace("리뷰 ","").replace("개","")
        if int(리뷰총수) < 1001:
            페이지카운트 = (int(리뷰총수) // 10)+1

        for _ in range(페이지카운트):
            scroll = driver.find_element_by_css_selector(
                        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
            time.sleep(1)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)
            time.sleep(1)

        #평점 리스트
        구글평점 = driver.find_elements_by_css_selector('.GHT2ce .DU9Pgb .kvMYJc')

        #리뷰 리스트
        구글리뷰 = driver.find_elements_by_css_selector('.GHT2ce .MyEned .wiI7pd')

        #리뷰수
        구글리뷰수 = len(구글리뷰)

        # 평점 리뷰 묶기
        구글리뷰_평점=[]
        
        for i in tqdm(range(len(구글리뷰))):
            try:
                reivew = [구글리뷰[i].text,구글평점[i].get_attribute('aria-label').replace(" 별표 ","").replace("개 ","")]
                구글리뷰_평점.append(reivew)
            except:
                continue
    
        #피클로 저장하기
        구글_리뷰크롤링 = {}
        구글_리뷰크롤링['구글리뷰'] = 구글리뷰_평점
        구글_리뷰크롤링['구글리뷰수']  = 구글리뷰수
        with open(f"google_pickle\{key}.pickle","wb") as fw:
            pickle.dump(구글_리뷰크롤링, fw)
        
    except:
        검색지명 = driver.find_element_by_css_selector('.tAiQdd .lMbq3e .DUwDvf.fontHeadlineLarge').text    
        driver.implicitly_wait(tt)
        try:
            driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]')
        except:
            driver.close()

        #리뷰더보기
        try:
            element = driver.find_element_by_css_selector('#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf')
            time.sleep(t)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element)
            time.sleep(t)
            element = driver.find_elements_by_css_selector(".m6QErb.Hk4XGb.QoaCgb.KoSBEe.tLjsW .M77dve")
            if len(element) < 2:
                driver.execute_script("arguments[0].click();", element[0])
                time.sleep(t)
            else:
                driver.execute_script("arguments[0].click();", element[1])
                time.sleep(t)
        except:
            try:
                driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button').click()
            except:
                driver.close()

        #스크롤100번 내리기
        try:
            리뷰총수 = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text
        except:
            try:
                리뷰총수=driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]').text
            except:
                driver.close()            
        페이지카운트 = 100
        try:
            리뷰총수 = 리뷰총수.replace("리뷰 ","").replace("개","").replace(',',"")
        except:
            리뷰총수 = 리뷰총수.replace("리뷰 ","").replace("개","")
        if int(리뷰총수) < 1001:
            페이지카운트 = int(리뷰총수) // 10
        for _ in range(페이지카운트):
            scroll = driver.find_element_by_css_selector(
                        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
            time.sleep(1)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)
            time.sleep(1)

        #평점 리스트
        구글평점 = driver.find_elements_by_css_selector('.GHT2ce .DU9Pgb .kvMYJc')

        #리뷰 리스트
        구글리뷰 = driver.find_elements_by_css_selector('.GHT2ce .MyEned .wiI7pd')

        #리뷰수
        구글리뷰수 = len(구글리뷰)

        # 평점 리뷰 묶기
        구글리뷰_평점=[]
        
        for i in tqdm(range(len(구글리뷰))):
            try:
                reivew = [구글리뷰[i].text,구글평점[i].get_attribute('aria-label').replace(" 별표 ","").replace("개 ","")]
                구글리뷰_평점.append(reivew)
            except:
                continue

        구글_리뷰크롤링 = {}
        구글_리뷰크롤링['리뷰'] = 구글리뷰_평점
        구글_리뷰크롤링['리뷰수']  = 구글리뷰수
        with open(f"google_pickle\{key}.pickle","wb") as fw:
            pickle.dump(구글_리뷰크롤링, fw)  
        