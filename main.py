# ----------------------------------------------------------
# 메인 함수
# 키워드 추출도 바깥으로 빼낼까 고민 중
# ----------------------------------------------------------

from unicodedata import name
import pandas as pd
import numpy as np
import os
from keyword_extraction import 키버트_키워드_추출
from skh import skh

# 파일 이름 찾기
dir_path = os.getcwd() + '\\tourist_attractions'
name_list = []
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        name_list.append(file_path.split('\\')[-1].replace('_.pickle', ''))

keyword_list = 키버트_키워드_추출(장소=name_list, 최소그램=1, 최대그램=1, 추출키워드개수=10, 상위키워드개수=20)

user_input = input("키워드를 입력하세요 : ")
skh(user_input, keyword_list)