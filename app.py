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
    
    print(body)
    GGGG = handler.handle(body, signature)
    print(GGGG)
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
            print(sn)
            print(sn_name)
            print(uid)
            print(user_name)
        else:
            line_bot_api.push_message(uid, TextSendMessage(user_name + '無使用權限'))
            print(uid)
            print(user_name)
        return 0
    elif re.match("守望兌換:[A-Z]", msg):
        GRCodes = msg[5:]
        print(GRCodes)
        #GRCode_name = guard(GRCodes)
        #print(GRCode_name)
        #line_bot_api.push_message(uid, TextSendMessage(text=GRCode_name))
        url = 'https://www.guardiantales.com/coupon/redeem/'
        UsersID = ['89765498736423','321231321']
        for i in UsersID:
            for j in {GRCodes}:
                #兌換開始    
                payload=('region=SEA&' + 'userId=' + i +'&code=' + j )
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                }
                response = requests.request("POST", url, data=payload, headers=headers) # 送出資訊
                soup = BeautifulSoup(response.text,"html.parser")
                sel = soup.find('p').text #抓回顯示值
                #print(sel)

                class state: #結果清單
                    state1 = ('成功。' + i + "：" + '兌換' + j)
                    state2 = ('UserID Error')
                    state3 = ('失敗。 ' + '原因：序號錯誤' + '\n(' + i + '_兌換_' + j + ')')
                    state4 = ('失敗。 ' + '原因：序號已兌換' + '\n(' + i + '_兌換_' + j + ')')
                    state5 = ('失敗。 ' + '原因：序號過期' + '\n(' + i + '_兌換_' + j + ')')
                #判斷兌換結果
                if sel == "Congratulations!You've successfully claimed the Coupon!Please check your mail in-game in order to redeem your rewards.":
                    name = state.state1
                elif sel == 'We were unable to find your User Number.Please double-check your User Number and the Region selected and try again.' :
                    name = state.state2
                elif sel == "The Coupon Code you've entered is invalid.Please check the Coupon Code and try again.":
                    name = state.state3
                elif sel == "The Coupon Code you've entered has already been claimed.If you have not yet redeemed this Coupon Code, please double-check your User Number and the Region selected and try again." :
                    name = state.state4
                elif sel == "The Coupon Code you've entered has already expired." : 
                    name = state.state5
                line_bot_api.push_message(uid, TextSendMessage(text=name))    
                #eenndd.append(name)
                #return name

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
