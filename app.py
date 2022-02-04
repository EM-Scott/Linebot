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
from Guardiantales import Guard
import os
import re

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
        sn = msg[2:5]
        sn_name = taiwanlottery.getGG88(sn)
        line_bot_api.push_message(uid, TextSendMessage(sn_name))
        print(sn)
        print(sn_name)
        return 0
    elif re.match("UID:[0-9]", msg):
        UIDD = msg
        line_bot_api.push_message(uid, TextSendMessage('UID紀錄完成'))
        return 0
    elif re.match("SN:[A-Z]", msg):
        SNN = msg
        line_bot_api.push_message(uid, TextSendMessage('SN紀錄完成'))
        return 0
    elif re.match("守望兌換", msg):
        resule = Guardiantales.Guard()
        print(resule) 
        line_bot_api.push_message(uid, TextSendMessage(resule))
        
                                  
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
