# _*_coding:utf-8_*_

from bottle import route, run, post, request
import json
import requests
import os
import random

TO_CHANNEL = 1383378250
EVENT_TYPE = "138311608800106203"

GOI = [
        u"超ウケる〜！",
        u"マジ？",
        u"超かわい〜",
        u"えー！まじやばい！",
        u"やばくない？",
        u"マジやばいんだけど〜",
    ]


@route("/test")
def test():
    return "I'm alive"


@post("/linebot/callback")
def send_message():
    messages = json.loads(request.body)["result"]

    result = []
    random.seed()

    for message in messages:
        body = json.dumps({
            "to": message["from"],
            "toChannel": TO_CHANNEL,
            "eventType": EVENT_TYPE,
            "content": {
                "contentType": 1,
                "toType": 1,
                "text": GOI[random.randint(0, len(GOI) - 1)],
            }
        })

        url = 'https://trialbot-api.line.me/v1/events'

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Line-ChannelID': os.environ.get("LINE_CHANNEL_ID"),
            'X-Line-ChannelSecret': os.environ.get("LINE_CHANNEL_SECRET"),
            'X-Line-Trusted-User-With-ACL': os.environ.get("LINE_CHANNEL_MID")
        }

        r = requests.post(url, data=json.dumps(body), headers=headers)
        result.append(r.headers["status"])
    return json.dumps(result)


run(host="localhost", port=9000, debug=True, reloader=True)
