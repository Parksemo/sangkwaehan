import numpy as np
import pandas as pd
from CBF import CBF
import telegram

token = '5569336973:AAHuk9BSs66Uq2fv7kuwNLCPVshMthsMXvA'
id = '5541102425'

bot = telegram.Bot(token=token)   # 봇 정의

bot.sendMessage(chat_id=id, text="test")  # 메세지 보내기

df = pd.read_pickle("pickle_review_data_frame")

#print(df)
#print(df.키워드)

np_df = df.to_numpy()

#print(np_df)
#print(np_df[0][1])
#print(np_df[0][1][0])

key = '관광지'
k_list = sum(df['키워드'].to_list(), [])
if key in k_list:
    a, b = CBF(key, df) # 추천 여행지, 꿀 여행지
    print(CBF(key, df))
    #print(type(a))
    c = a.values
    print(a.values) # 이렇게 하면 룰루가 리스트 나옴
    print(b.values[0]) # 이렇게 하면 값이 나옴
    #print(CBF(key, df)[0]['Name'])

    print("찾음")
for i in c:
    bot.sendMessage(chat_id=id, text=f"{i}")  # 메세지 보내기


