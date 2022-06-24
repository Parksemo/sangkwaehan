# ----------------------------------------------------------
# 챗봇 함수
# ----------------------------------------------------------

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pandas as pd
import telegram
from CBF import CBF
from random_keyword import print_random_keyword
import os
from google_images_download import google_images_download
import random

token = '5462763221:AAEIpwfa5dkOtDrt75kQbSyWLeCd26XSiGc'
id = '5577209588'

bot = telegram.Bot(token=token)   # 봇 정의

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

df = pd.read_pickle("pickle_review_data_frame.pickle")

'''
1. 사용자에게 키워드 입력을 요구
2. 사용자가 입력한 키워드를 받아서 처리
3-1. 키워드가 있을 경우, 키워드에 해당되는 장소 반환
3-2. 키워드가 없을 경우, 키워드를 랜덤으로 5개 제공, 키워드 다시 입력 요구
'''

# 1 -> 나중에 문구 수정
bot.send_photo(chat_id=id, photo=open('main.PNG', 'rb'))
#bot.sendMessage(chat_id=id, text="가고 싶은 여행지의 키워드를 입력해주세요.")

def handler(update, context):
    # 2
    user_text = update.message.text # 사용자가 보낸 메세지

    k_list = sum(df['키워드'].to_list(), [])
    # 3-1.
    if user_text in k_list:
        best_tourist_attractions, honey_tourist_attractions1, honey_tourist_attractions2 = CBF(user_text, df)
        
        if best_tourist_attractions.item() == honey_tourist_attractions1.item():
            honey_tourist_attractions = honey_tourist_attractions2
        else:
            honey_tourist_attractions = honey_tourist_attractions1

        for i in best_tourist_attractions:
            key1, key2, key3, score = add_info(i)
            bot.sendMessage(chat_id=id, text=f"추천하는 인기 여행지는 {i} 입니다.\n\n해당 여행지의 키워드는 {key1}, {key2}, {key3} 입니다. \n\n해당 여행지를 다녀간 여행객들의 평균 평점은 {score} 입니다.")  # 추천 여행지
            path = show_image(i)
            bot.send_photo(chat_id=id, photo=open(f'{path}', 'rb'))

        for j in honey_tourist_attractions:
            key1, key2, key3, score = add_info(j)
            bot.sendMessage(chat_id=id, text=f"추천하는 꿀 여행지는 {j} 입니다.\n\n해당 여행지의 키워드는 {key1}, {key2}, {key3} 입니다.\n\n해당 여행지를 다녀간 여행객들의 평균 평점은 {score} 입니다.")  # 꿀 여행지
            path = show_image(j)
            bot.send_photo(chat_id=id, photo=open(f'{path}', 'rb'))

    #3-2
    else:
        score = find_tourist_attractions(user_text)
        if score > 0:
            bot.sendMessage(chat_id=id,text=f"입력하신 여행지는 {user_text} 입니다.\n\n해당 여행지를 다녀간 여행객들의 평균 평점은 {score} 입니다.")
            bot.sendMessage(chat_id=id, text="하지만 저희 챗봇은 여행 키워드 입력 후 여행지를 추천해줍니다. \n\n다시 가고 싶은 여행지의 키워드를 입력해주세요.")

        else:
            key_list = print_random_keyword(k_list)
            bot.sendMessage(chat_id=id, text="검색한 키워드를 찾을 수 없습니다. 시스템의 추천 키워드는 다음과 같습니다.")
            a, b, c, d, e = key_list
            bot.sendMessage(chat_id=id, text=f"{a}, {b}, {c}, {d}, {e}")
            bot.sendMessage(chat_id=id, text="다시 가고 싶은 여행지의 키워드를 입력해주세요.")


def show_image(key):
    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": key, "limit": 1, "print_urls": True, "format":"jpg"}
    paths = response.download(arguments)  # passing the arguments to the function
    #print(paths)

    dir_path = os.getcwd() + '\\downloads' + f'\\{key}'

    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            #name = file_path.split('\\')[-1].replace('.jpg', '')
    return file_path


def add_info(tourist_attractions):
    index = df.index[df['장소'] == tourist_attractions].tolist()
    keyword_list = sum(df.loc[index]['키워드'].to_list(), [])
    key1, key2, key3 = random.sample(keyword_list, 3)
    score = df.loc[index]['평점'].to_list()
    return key1, key2, key3, round(score[0], 2)


def find_tourist_attractions(tourist_attractions):
    index = df.index[df['장소'] == tourist_attractions].tolist()
    if len(index) == 1:
        score = df.loc[index]['평점'].to_list()
        return round(score[0], 2)
    else:
        return -1


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
