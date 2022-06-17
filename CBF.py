import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CBF 수행 
def CBF(DataFrame):
    # 전처리
    data = DataFrame.drop(labels='Unnamed: 0', axis=1)
    data['키워드'] = data['키워드'].apply(literal_eval)
    data['키워드_literal'] = data['키워드'].apply(lambda x: (' ').join(x))
    
    # 키워드 입력 부분(최종 코드에서는 수정 예정)
    input_sereris = {'장소': '사용자', '키워드': np.nan, '평점': np.nan, '키워드_literal': '바다'}
    user_series = pd.Series(input_sereris)

    new_data = data.append(user_series, ignore_index=True)

    # CBF
    count_vec = CountVectorizer(min_df=0)
    keyword_mat = count_vec.fit_transform(new_data['키워드_literal'])
    keyword_sim = cosine_similarity(keyword_mat, keyword_mat)

    keyword_sim_sorted_ind = keyword_sim.argsort()[:, ::-1]
    input_user = new_data[new_data['장소'] == '사용자']
    input_idx = input_user.index.values
    similar_idx = keyword_sim_sorted_ind[input_idx]
    similar_idxs = similar_idx.reshape(-1)

    return new_data.iloc[similar_idxs][1:2] # 유사도 가장 높은 장소 한 곳 반환