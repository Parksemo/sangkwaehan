import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer

# 가볼만한 곳 리스트 불러오기.
data = pd.read_csv('부산여행순위.csv')
장소_list = np.array(data.장소)

# 키워드 추출 함수
def 키워드추출(장소):
    키워드_리스트 = []
    평점 = []
    for j in 장소:
        t_d = pd.read_csv(f'{j}.csv')
        s_w = set(['곳', '수', '것', '추천', '정도', '사람', '때', '정말', '볼', '꼭', '좀', '날', '그', '번', '조금', '가면', '시간', '타고', '다누', '방문', '떄문', '다시', '예전', '보고', '중간', '주변'])
        okt = Okt()
        p_data = []
        for i in tqdm(t_d['리뷰']):
            tk_d=okt.nouns(i)
            end_d=[w for w in tk_d if not w in s_w]
            p_data.append(' '.join(end_d))
        tk = Tokenizer(num_words=1000)
        tk.fit_on_texts(p_data)
        키워드개수 = sorted(list(tk.word_counts.items()), key=lambda x:x[1], reverse=True)[:10]
        키워드top10 = []
        for i in 키워드개수:
            키워드top10.append(i[0])
        키워드_리스트.append(키워드top10)
        평점.append(t_d['평점'].mean())
    장소_키워드_평점 = pd.DataFrame(list(zip(장소, 키워드_리스트, 평점)), columns=['장소', '키워드', '평점'])
    return 장소_키워드_평점

for 장소 in 장소_list:
    키워드추출(장소).to_csv(f'{장소}_키워드.csv', encoding='utf-8-sig')
