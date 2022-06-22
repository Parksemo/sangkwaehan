from selenium import webdriver
import chromedriver_autoinstaller
import time
from tqdm import tqdm_notebook
from selenium.webdriver.common.keys import Keys
import pickle
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('부산여행순위_최종.csv')
places = data['장소']

def crawling_tripdotcom(place):
    # 크롬 접속
    chrome_path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(chrome_path)

    driver.get('https://kr.trip.com/?allianceid=14887&sid=1621818&ppcid=ckid-58405427_adid-520580363185_akid-kwd-415216391968_adgid-122493363536&utm_source=google&utm_medium=cpc&utm_campaign=Trip_KR-ko+Exact+2&ds_cid=71700000083539479&ds_kid=43700063610995885&gclid=CjwKCAjwtcCVBhA0EiwAT1fY7xJ2rWB6av3kZ68J0IUw0aMFQ4fdFwMFf90DoVp9p0kQHyFxJvE4oBoCcl8QAvD_BwE&gclsrc=aw.ds')
    time.sleep(2)
    
    # 검색창에 관광지 입력
    element = driver.find_element_by_xpath('//*[@id="header-search-container"]/div/div[1]/input')
    element.send_keys(place)
    
    # 검색 버튼 클릭
    element = driver.find_element_by_xpath('//*[@id="header-search-container"]/div/div[2]')
    element.click()
    time.sleep(1)
    
    # 새창 전환
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    
    # 좌측 메뉴에서 명소 탭 클릭
    menu = driver.find_elements_by_class_name('tab-name')
    for i in menu:
        if '명소' in i.text:
            i.click()
            time.sleep(2)
    
    try:
        # 장소 클릭
        element = driver.find_element_by_class_name('gl-search-result_list-content')
        element.click()
        time.sleep(2)
        
        # 지역 체크(부산인지)
        region_check = False
        regions = driver.find_elements_by_class_name('gl-component-bread-crumb_item')
        for region in regions:
            if '부산' in region.text:
                region_check = True
                break

        # 부산이 맞다면 정상적으로 진행
        if region_check:
            # 리뷰가 있는 곳으로 이동
            element = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[1]/div[1]/span[2]/div')
            element.click()
            time.sleep(2)

            reviews = []
            stars = []
            check = True
            while check:
                try:
                    driver.find_element_by_class_name('btn-next.disabled')

                    review_data = driver.find_elements_by_class_name('mt10.hover-pointer ')
                    star_data = driver.find_elements_by_class_name('review_score')
                    if len(star_data) == 0:
                        check = False

                    for i in review_data:
                        reviews.append(i.text)
                    for i in star_data:
                        if len(i.text) < 2:
                            stars.append(i.text)

                    check = False
                except:
                    review_data = driver.find_elements_by_class_name('mt10.hover-pointer ')
                    star_data = driver.find_elements_by_class_name('review_score')
                    if len(star_data) == 0:
                        check = False

                    for i in review_data:
                        reviews.append(i.text)
                    for i in star_data:
                        if len(i.text) < 2:
                            stars.append(i.text)
                    driver.find_element_by_class_name('ReviewListContainer-p31g93-0 button.btn-next').send_keys(Keys.RETURN)
                    time.sleep(2)

            out_review = list(zip(reviews, stars))
            pickle_data = {}
            pickle_data['리뷰'] = out_review
            pickle_data['리뷰수']  = len(reviews)

            try:
                with open(f'tripdotcom_pickle\{place}_.pickle', 'rb') as fr:
                    loaded_data = pickle.load(fr)     

                new_out = loaded_data['리뷰'] + out_review
                new_num_of_review = loaded_data['리뷰수'] + len(reviews)
                pickle_data = {'리뷰': new_out, '리뷰수': new_num_of_review}

                with open(f'tripdotcom_pickle\{place}_.pickle', 'wb') as fw:
                    pickle.dump(pickle_data, fw)
            except:
                with open(f'tripdotcom_pickle\{place}_.pickle', 'wb') as fw:
                    pickle.dump(pickle_data, fw)

        #부산이 아니라면 크롤링하지 않음
        else:
            print('부산 관광지가 아닙니다.')
    except Exception as e:
        print(f'{place}에 해당하는 검색결과가 없습니다.\n', e)

for place in tqdm_notebook(places):
    crawling_tripdotcom(place)