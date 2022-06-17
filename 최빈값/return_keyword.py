import pandas as pd
import ast
from collections import Counter

list1=[]
list2=[]
list3=[]
list4=[]
maximum=[]

data = pd.read_csv('keyword_list.csv')
for i in data.키워드:
    list1.append(i)#"['전망 새해 행복', '평화 바다 풍경', '여름 휴가 가치', '바다 행운 태종대', ''''''']"

#데이터 프레임 리스트화
for i in list1:
    list2.append(ast.literal_eval(i))#['전망 새해 행복', '평화 바다 풍경', '여름 휴가 가치', ''''']

#띄어쓰기 단위로 단어 분할
for j in list2:
    for k in j:
        list3.append(k.split())#['전망', '새해', '행복'], ['평화', '바다', '풍경'], ['여름', '휴가', '가치']''''''

#분할된 단어 리스트화
for i in list3:
    list4+=i#['전망', '새해', '행복', '평화', '바다', '풍경',''''''']

#상위 10개의 최빈값 구하기
cnt= Counter(list4)
order=cnt.most_common(10)

#튜플 -> 리스트 및 최빈값 저장
for i in order:
    maximum.append(list(i)[0])
print(maximum)
