import pandas as pd
import numpy as np
import keyword_extraction
import CBF

# 가볼만한 곳 리스트 불러오기.
data = pd.read_csv('부산여행순위.csv')
장소_list = np.array(data.장소)[:5]

keyword_list = keyword_extraction.키버트_키워드_추출(장소=장소_list, 최소그램=2, 최대그램=3, 추출키워드개수=5, 상위키워드개수=20)
print(CBF.CBF(keyword_list))