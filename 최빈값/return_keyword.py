import pandas as pd
import ast
from collections import Counter
import random

list1=[]
list2=[]
list3=[]
maximum=[]

data = pd.read_csv('keyword_list.csv')
for i in data.키워드:
    list1.append(i)#"['전망 새해 행복', '평화 바다 풍경', '여름 휴가 가치', '바다 행운 태종대', ''''''']"

#데이터 프레임 리스트화
for i in list1:
    list2.append(ast.literal_eval(i))#['전망 새해 행복', '평화 바다 풍경', '여름 휴가 가치', ''''']

#분할된 단어 리스트화
for i in list2:
    list3+=i#['전망', '새해', '행복', '평화', '바다', '풍경',''''''']

#최빈값 상위 15개 구하기
cnt= Counter(list3)
order=cnt.most_common(15)

#튜플 -> 리스트 및 최빈값 저장
for i in order:
    maximum.append(list(i)[0])
print(maximum)

#랜덤으로 최빈값 뽑기
rand_maximun=[]
for i in range(5):
    a = random.randrange(10)#30개의 최빈값중에서 상위 10개에서 랜덤으로 가져오기 위한 난수
    rand_maximun.append(maximum[a])#기존 최빈값에서 랜덤으로 가져오기
    b=maximum.remove(maximum[a])#중복값 제거
print(rand_maximun)#출력