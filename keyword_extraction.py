# ----------------------------------------------------------
# 키워드 추출 함수
# ----------------------------------------------------------

import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle
import os

# 파일 이름 찾기
df = pd.read_csv('부산여행순위_최종.csv')
name_list = df['장소']

# 불용어 텍스트 파일 읽기
stop_words = []
with open('stop_words.txt', 'rt', encoding='utf-8') as fr:
    lines = fr.readlines()
    for line in lines:
        stop_words.append(line.replace('\n', ''))

# 키워드 추출 함수
def 키버트_키워드_추출(장소, 최소그램, 최대그램, 추출키워드개수, 상위키워드개수):
    평점 = []
    키워드_총_리스트 = []
    리뷰_수_리스트 = []
    s_w = set(stop_words)
    for k in tqdm(장소):
        # 파일 불러오기
        with open(f'merged_pickle\{k}.pickle', 'rb') as fr:
            data = pickle.load(fr)   
        t_d = data['총리뷰']
        t_d = pd.DataFrame(t_d)
        t_d.columns = ["리뷰", "평점"]

        # 전처리
        t_d['평점'] = t_d['평점'].apply(lambda x: float(x))
        doc = ""
        for m in t_d['리뷰']:
            doc += m
        doc = doc.replace(k,'')
        okt = Okt()
        tokenized_doc = okt.nouns(doc)
        end_d=[w for w in tokenized_doc if not w in s_w]
        tokenized_nouns = ' '.join(end_d)

        # 키워드 추출
        n_gram_range = (최소그램, 최대그램)
        count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
        candidates = count.get_feature_names_out()
        model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
        doc_embedding = model.encode([doc])
        candidate_embeddings = model.encode(candidates)
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        distances_candidates = cosine_similarity(candidate_embeddings, candidate_embeddings)
        candidates_idx = list(distances.argsort()[0][-상위키워드개수:])
        candidates_vals = [candidates[index] for index in candidates_idx]
        distances_candidates = distances_candidates[np.ix_(candidates_idx, candidates_idx)]
        min_sim = np.inf
        candidate = None
        for combination in itertools.combinations(range(len(candidates_idx)), 추출키워드개수):
            sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
            if sim < min_sim:
                candidate = combination
                min_sim = sim
        키워드_리스트 = []
        for idx in candidate:
            키워드_리스트.append(candidates_vals[idx])
        키워드_총_리스트.append(키워드_리스트)
        평점.append(t_d['평점'].mean())
        리뷰_수_리스트.append(data['총리뷰수'])

        print(f'''장소 : {k}
키워드 : {키워드_리스트}
평점 : {t_d['평점'].mean()}
리뷰수 : {data['총리뷰수']}        
        ''')
        
    장소_키워드_평점 = pd.DataFrame(list(zip(장소, 키워드_총_리스트, 평점, 리뷰_수_리스트)) ,columns=['장소','키워드','평점', '리뷰수'])
    장소_키워드_평점.to_pickle("pickle_review_data_frame.pickle")
    return 장소_키워드_평점

키버트_키워드_추출(장소=name_list, 최소그램=1, 최대그램=1, 추출키워드개수=10, 상위키워드개수=20)