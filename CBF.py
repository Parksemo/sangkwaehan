# ----------------------------------------------------------
# 관광지 추천 함수
# ----------------------------------------------------------

import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CBF 수행 
def CBF(user_input_keyword, DataFrame):
    # 전처리
    data = DataFrame
    data['키워드_literal'] = data['키워드'].apply(lambda x: (' ').join(x))
    
    input_sereris = {'장소': '사용자', '키워드': np.nan, '평점': np.nan, '리뷰수': np.nan, '키워드_literal': f'{user_input_keyword}'}
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

    # -----------------------------------------------------------------------------
    # 꿀장소 추천
    similar_df = new_data.iloc[similar_idxs][1:8]
    review_max = max(similar_df['리뷰수'])

    review_score = []
    score_score = []
    for i in similar_df['리뷰수']:
        review_score.append(100 - (i / review_max * 100))
    
    for i in similar_df['평점']:
        score_score.append(i * 20)

    similar_df['review_score'] = review_score
    similar_df['score_score'] = score_score

    result = []
    for i in range(len(similar_df)):
        result.append(review_score[i] / 2 + score_score[i] / 2)
    
    similar_df['result'] = result
    similar_df = similar_df.sort_values(by = ['result'], ascending = False)
    result_max1 = list(similar_df['result'])[0]
    result_max2 = list(similar_df['result'])[1]

    best_tourist_attractions = new_data.iloc[similar_idxs][1:2]['장소']
    honey_tourist_attractions1 = similar_df[similar_df['result'] == result_max1]['장소']
    honey_tourist_attractions2 = similar_df[similar_df['result'] == result_max2]['장소']
    return best_tourist_attractions, honey_tourist_attractions1, honey_tourist_attractions2