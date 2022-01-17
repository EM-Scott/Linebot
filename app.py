from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('lPkuq0new8upb+bh5muA9vU9w/BNy5+QQhk7r3cFxqdL9wcv6n2ue1/jxzWPiCBXSvo0agpYhE4X55liDKoAz6yxoOFxwL/FCUtjEX3TQz+IFDzwuWNmYFxpSgaVenl3Qn4lwPVM7n7FL79qK5DagAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e8a1992d6f0fa55a5509d6f7145835b0')
my_user_id = 'U13827e14d459bb54ca2e0357703e920e'
line_bot_api.push_message(my_user_id, TextSendMessage(text='機器人運行開始'))

words = ''
save = False


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#======回應內容======

# 處理訊息
@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global words
    global save

    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id) 
    
    _name = profile.display_name
    print("大頭貼：", profile.picture_url)
    print("狀態消息：", profile.status_message)
    print("匿名：", profile.display_name)
    print("使用者ID：", profile.user_id)

    txt=event.message.text

    if (txt=='Hi') or (txt=="你好"):
        reply = f'{_name}你好！'
    elif '悄悄話' in txt:
        if words != '':
            reply = f'你的悄悄話是：\n\n{words}'
        else:
            reply = '放膽說出心裡的話吧～'
            save = True
    elif save:
        words = txt
        save = False
        reply = '我會好好保護這個祕密喔～'
    elif '牛牛' in txt:
        reply = '牛牛啊咪波'
    elif '教學' in txt:
        reply = '給您參考:https://github.com/ChenTsungYu/stock_linebot_public/blob/master/app.py'
    elif '最新合作廠商' in txt:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in txt:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in txt:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in txt:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in txt:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in txt:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'Youtube:' in txt:
        reply = '此功能開發中'
   
    msg = TextSendMessage(reply)
    line_bot_api.reply_message(event.reply_token, msg)
    

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
