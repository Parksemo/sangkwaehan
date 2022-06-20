import pandas as pd
import numpy as np
from keyword_extraction import 키버트_키워드_추출
from skh import skh

# 가볼만한 곳 리스트 불러오기.
data = pd.read_csv('부산여행순위.csv')
장소_list = np.array(data.장소)[:1]

keyword_list = 키버트_키워드_추출(장소=장소_list, 최소그램=1, 최대그램=1, 추출키워드개수=10, 상위키워드개수=20)

user_input = input("키워드를 입력하세요 : ")
skh(user_input, keyword_list)