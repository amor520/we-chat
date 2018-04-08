# -*- coding: utf-8 -*-
from flask import Flask
import flask_restful
import json
import pytz
import time
from bson.codec_options import CodecOptions
from pymongo import MongoClient as Client
from bson.json_util import dumps

connection = Client('mongodb://localhost:27017/')
mongodb = connection.get_database(
    "wechat",
    codec_options=CodecOptions(
        tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))

msg_info = mongodb.msg_info

app = Flask(__name__)
api = flask_restful.Api(app)
class HelloWorld(flask_restful.Resource):
    def get(self):
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
        items = dumps(items,ensure_ascii=False)
        return items
api.add_resource(HelloWorld, '/')
app.run(host='0.0.0.0',port=5000)