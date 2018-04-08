import requests, time
import itchat
import json
import pytz
from bson.codec_options import CodecOptions
from pymongo import MongoClient as Client
from bson.json_util import dumps
from itchat.content import TEXT, PICTURE, VIDEO, RECORDING, ATTACHMENT, VIDEO
from wordcloud import WordCloud
import codecs
import jieba
import jieba.analyse
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

connection = Client('mongodb://localhost:27017/')
mongodb = connection.get_database(
    "wechat",
    codec_options=CodecOptions(
        tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))

msg_info = mongodb.msg_info

KEY = '684233fbc60b47d69f11a225b1d1c2ee'


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wecahtbot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


# @itchat.msg_register(TEXT, isFriendChat=True)
# def tuling_reply(msg):
#     """
#     图灵机器人
#     """
#     print(msg)
#     return get_response(msg.text)

# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     """
#     文本消息
#     """
#     msg.user.send('%s: %s' % (msg.type, msg.text))


def group_id(name):
    df = itchat.search_chatrooms(name=name)
    return df[0]['UserName']


# msgType = {1: "文本", 3: "图片", 47: "emoji", 62: "小视频"}


# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid',
#     }.get(msg.type, 'fil')
#     print('@%s@%s' % (typeSymbol, msg.fileName))


def draw_wordcloud():
    items = msg_info.find({
        "create_at": {
            "$gt": time.strftime("%Y-%m-%d", time.localtime())
        }
    }).sort("create_at", -1)
    comment_text = ""

    for item in items:
        comment_text += item["content"]

    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__)  # 当前文件文件夹所在目录
    frequencies = jieba.analyse.extract_tags(
        cut_text, topK=100, withWeight=True)
    freq_dict = dict(frequencies)
    # color_mask = imread("./images.jpg") # 读取背景图片
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        font_path="HYQiHei-25J.ttf",
        #设置背景色
        background_color="white",
        #词云形状
        # mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        width=1000,
        height=600,
        min_font_size=20,
        max_font_size=80,
        margin=2)
    word_cloud = cloud.generate_from_frequencies(freq_dict)  # 产生词云
    word_cloud.to_file("pjl_cloud.jpg")  #保存图片


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    chat_dict = {}
    item = group_id(u'萌炸天🐱')
    if msg['FromUserName'] == item:
        msg_info.insert_one({
            "type":
            msg["MsgType"],
            "name":
            msg["ActualNickName"],
            "content":
            msg["Content"],
            "create_at":
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })

        items = msg_info.aggregate([{
            "$match": {
                "create_at": {
                    "$gt": time.strftime("%Y-%m-%d", time.localtime())
                }
            }
        }, {
            "$group": {
                "_id": "$name",
                "count": {
                    "$sum": 1
                }
            }
        }, {
            "$sort": {
                "count": -1
            }
        }])
        items = dumps(items)
        with open('we-chat/static/data.json', 'w') as f:
            json.dump(items, f, 'UTF-8')


if __name__ == '__main__':

    draw_wordcloud()
    itchat.auto_login(hotReload=True)
    itchat.run()
