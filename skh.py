import pandas as pd
import numpy as np
from CBF import CBF
from random_keyword import print_random_keyword

# 주 동작 함수
# 유저가 입력한 키워드에 따라 동작
# 1. 유저 입력 키워드가 키워드리스트에 존재한다. -> 추천 시스템 동작
# 2. 유저 입력 키워드가 키워드리스트에 존재하지 않는다. -> 랜덤 키워드 출력 함수 동작
def skh(user_input_keyword, keyword_list):
    k_list = sum(keyword_list['키워드'].to_list(), [])

    if user_input_keyword in k_list:
        print(CBF(user_input_keyword, keyword_list))
    else:
        print(print_random_keyword(k_list))
