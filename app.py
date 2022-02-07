### it can run by 2022/02/04 for call issue. ###
from model import sheet
from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
    ConfirmTemplate, TemplateSendMessage,
    MessageAction, URIAction, LocationMessage,
    ButtonsTemplate
)
import taiwanlottery
from Guardiantales import guard
from Guardiantales import check_name
import os
import re
import requests
from bs4 import BeautifulSoup

gs = sheet.GoogleSheet('LineBotDATA','工作表1')

line_bot_api = LineBotApi('lPkuq0new8upb+bh5muA9vU9w/BNy5+QQhk7r3cFxqdL9wcv6n2ue1/jxzWPiCBXSvo0agpYhE4X55liDKoAz6yxoOFxwL/FCUtjEX3TQz+IFDzwuWNmYFxpSgaVenl3Qn4lwPVM7n7FL79qK5DagAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e8a1992d6f0fa55a5509d6f7145835b0')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Line Bot!'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.default()
def default(event):
    print('捕捉到事件：', event)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).upper().strip() # 使用者輸入的內容
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name #使用者名稱
    uid = profile.user_id # 發訊者ID
#================================ 
    # AnswerFile
    if re.match("呱:[A-Z]{3}", msg):
        if uid == 'U13827e14d459bb54ca2e0357703e920e' or 'U06e24ea18e919e92af56dcdd8eec0565':
            sn = msg[2:5]
            sn_name = taiwanlottery.getGG88(sn)
            line_bot_api.push_message(uid, TextSendMessage(sn_name))
            print(sn,sn_name,uid,user_name)
        else:
            line_bot_api.push_message(uid, TextSendMessage(user_name + '無使用權限'))
            print(uid,user_name)
        return 0
    
    elif re.match("守望兌換:[A-Z]", msg):
        if uid == 'U13827e14d459bb54ca2e0357703e920e' or 'U06e24ea18e919e92af56dcdd8eec0565':
            GRCodes = msg[5:].split(",")
            UsersID = ['32','98']
            guard_name = ['《兌換結果》']
            
            for i in UsersID:
                guard_name.append(check_name(i))
                for j in GRCodes:
                    guard_name.append(guard(i,j))
            line_bot_api.push_message(uid, TextSendMessage("\n".join(guard_name) + "\n")
                                      
        #else :
            #line_bot_api.push_message(uid, TextSendMessage(user_name + '無使用權限'))
            #print(uid,user_name)
        return 0
            
#處理貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
