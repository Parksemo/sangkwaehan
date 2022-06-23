# ----------------------------------------------------------
# 피클 병합 함수
# ----------------------------------------------------------

import numpy as np
import pandas as pd
import os
import pickle

def 피클병합():
    reviews_TAV_l = []
    reviews_GMR_l = []
    reviews_TDC_l = []
    reviews_all_l = []
    
    # 파일 검색을 위해 이름 가져오기
    data = pd.read_csv('부산여행순위_최종.csv')
    data_l = list(data.장소)
    
    # 파일 경로 찾기
    TAV = os.listdir(os.getcwd()+'\\TAV')
    GMR = os.listdir(os.getcwd()+'\\GMR')
    TDC = os.listdir(os.getcwd()+'\\TDC')
    
    # 장소 이름 따오기
    TAV_l = []
    for i in TAV:
        TAV_l.append(i.replace('.pickle',''))        
    GMR_l = []
    for i in GMR:
        GMR_l.append(i.replace('.pickle',''))
    TDC_l = []
    for i in TDC:
        TDC_l.append(i.replace('.pickle',''))    
    
    # 피클 파일 병합
    for i in data_l:
        if i not in TAV_l:
            reviews_TAV = 0
            out_re_TAV = []
        else:
            with open(f"./TAV/{i}.pickle","rb") as fr:
                크롤링_리뷰수 = pickle.load(fr)
            reviews_TAV = 크롤링_리뷰수['트립리뷰수']
            out_re_TAV = 크롤링_리뷰수['트립리뷰']
        reviews_TAV_l.append(reviews_TAV)

        if i not in GMR_l:
            reviews_GMR = 0
            out_re_GMR = []
        else:
            with open(f"./GMR/{i}.pickle","rb") as fr:
                구글_리뷰크롤링 = pickle.load(fr)
            reviews_GMR = 구글_리뷰크롤링['구글리뷰수']
            out_re_GMR = 구글_리뷰크롤링['구글리뷰']
        reviews_GMR_l.append(reviews_GMR)

        if i not in TDC_l:
            reviews_TDC = 0
            out_re_TDC = []
        else:
            with open(f"./TDC/{i}_.pickle","rb") as fr:
                크롤링_리뷰수 = pickle.load(fr)
            reviews_TDC = len(크롤링_리뷰수['리뷰'])
            out_re_TDC = 크롤링_리뷰수['리뷰']
        reviews_TDC_l.append(reviews_TDC)

        reviews_all = reviews_TAV+reviews_GMR+reviews_TDC
        reviews_all_l.append(reviews_all)
        out_re_all = out_re_TAV+out_re_GMR+out_re_TDC    

        총_크롤링_리뷰={}
        총_크롤링_리뷰['총리뷰'] = out_re_all
        총_크롤링_리뷰['총리뷰수']  = reviews_all
        with open(f"merged_pickle/{i}.pickle","wb") as fw:
            pickle.dump(총_크롤링_리뷰, fw)
    피클_병합=pd.DataFrame(list(zip(data_l, reviews_TAV_l, reviews_GMR_l,reviews_TDC_l,
                                reviews_all_l)) ,columns=['장소','트립어드바이저','구글맵리뷰',
                                                          '트립닷컴','총개수'])
    피클_병합.to_csv("피클_병합.csv", encoding='utf-8-sig')
    return 피클_병합