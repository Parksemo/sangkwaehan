import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pandas as pd
import random

'''

lis = ['안녕', '나는', '김', '수민', '이야']
a, b, c, d, e = lis

token = '5569336973:AAHuk9BSs66Uq2fv7kuwNLCPVshMthsMXvA'
id = '5541102425'

bot = telegram.Bot(token=token)   # 봇 정의

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()
bot.sendMessage(chat_id=id, text="가고 싶은 여행지의 키워드를 입력해주세요.")
bot.sendMessage(chat_id=id, text=f"{a}, {b}, {c}, {d}, {e}")

df = pd.read_pickle("pickle_review_data_frame")
print(df)
a = '감천 문화마을'
#print(df.index[df['장소'] == a].tolist())

c = df.index[df['장소'] == a].tolist()
#print(df.loc[c]['키워드'].to_list())
d = sum(df.loc[c]['키워드'].to_list(), [])
print(d[0])
e = df.loc[c]['평점'].to_list()
print(round(e[0], 2))


df = pd.read_pickle("pickle_review_data_frame")


def add_info(tourist_attractions):
    index = df.index[df['장소'] == tourist_attractions].tolist()
    keyword_list = sum(df.loc[index]['키워드'].to_list(), [])
    key1, key2, key3 = random.sample(keyword_list, 3)
    score = df.loc[index]['평점'].to_list()
    return key1, key2, key3, round(score[0], 2)


a = '감천 문화마을'
print(add_info(a))

a = ['a', 'b', 'c']
b = 'd'
c = b in a
print(c)'''
def find_tourist_attractions(tourist_attractions):
    index = df.index[df['장소'] == tourist_attractions].tolist()
    if len(index) == 1:
        score = df.loc[index]['평점'].to_list()
        return round(score[0], 2)
    else:
        return -1
df = pd.read_pickle("pickle_review_data_frame")
tourist_attractions ='감천 문화마을'

#index = df.index[df['장소'] == tourist_attractions].tolist()
print(find_tourist_attractions(tourist_attractions))