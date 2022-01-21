from collections import UserDict
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac

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
#
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 建立憑證
cr = sac.from_json_keyfile_name('google_auth.json', scope)  # 請自行修改檔名
gs = gspread.authorize(cr)
my_user_id = 'U13827e14d459bb54ca2e0357703e920e'
line_bot_api.push_message(my_user_id, TextSendMessage(text='機器人運行開始'))

users = {}

def check_user(id, name):
    global users

    if id not in users and users[id] is None:
        users[id] = {    # 初始化此使用者物件
            'name':name,
            'words':'',
            'save':False 
        }
        print('新增一名用戶：', id)
    else:
        print('用戶已經存在，id：', id)
        print('目前用戶數：', len(users))

def reply_text(token, id, txt):
    global users
    me = users[id]

    if me['save']  == False:
        if '報修' in txt:
            queries = ConfirmTemplate(
                text=f"{me['name']}您好，請問要回報查修地點嗎？", 
                actions=[
                    URIAction(
                        label='回報地點',
                        uri='line://nv/location'
                    ),
                    MessageAction(label='不需要', text='不需要')
                ])
            # queries = ButtonsTemplate(
            #     text=f"{me['name']}您好，請問要回報查修地點嗎？",
            #     actions=[
            #         URIAction(
            #             label='回報地點',
            #             uri='line://nv/location'
            #         ),
            #         MessageAction(label='不需要', text='不需要'),
            #         URIAction(
            #             label='前往swf.com.tw網站',
            #             uri='https://swf.com.tw/'
            #         )
            #     ])

            temp_msg = TemplateSendMessage(alt_text='確認訊息',
                                        template=queries)
            line_bot_api.reply_message(token, temp_msg)
            me['save'] = True # 開始紀錄訊息
        else:
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="收到訊息了，謝謝！"))
    else:
        if txt=='不需要':
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="好的，請大致描述狀況。"))
        elif me['logs']['事由'] == '':
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="我記下來了，辛苦您了！"))
            me['logs']['事由'] = txt  # 儲存事由
            # 日期要設置成台北時間
            dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            me['logs']['日期時間'] = dt
            me['save'] = False   # 紀錄完畢

            print('資料紀錄:', me['logs'])
            logs = [id, me['name'], me['logs']['日期時間'], 
                        me['logs']['經緯度'], me['logs']['地址'], me['logs']['事由']]
            gs.append_row(logs)


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
@handler.default()
def default(event):
    print('捕捉到事件：', event)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id) 
    _name = profile.display_name
    txt = event.message.text
    print("大頭貼：", profile.picture_url)
    print("狀態消息：", profile.status_message)
    print("匿名：", profile.display_name)
    print("使用者ID：", profile.user_id)
    check_user(_id, _name)

    # if '牛牛' in txt:
    #     reply = '牛牛啊咪波'
    # elif '教學' in txt:
    #     reply = '給您參考:https://github.com/ChenTsungYu/stock_linebot_public/blob/master/app.py'
    # elif '最新合作廠商' in txt:
    #     message = imagemap_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '最新活動訊息' in txt:
    #     message = buttons_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '註冊會員' in txt:
    #     message = Confirm_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '旋轉木馬' in txt:
    #     message = Carousel_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '圖片畫廊' in txt:
    #     message = test()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '功能列表' in txt:
    #     message = function_list()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif 'Youtube:' in txt:
    #     reply = '此功能開發中'


   
    msg = TextSendMessage(reply)
    line_bot_api.reply_message(event.reply_token, msg)
    reply_text(event.reply_token, _id, txt)
    
# 處理地點訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    global users

    _id = event.source.user_id
    me = users[_id]
    addr=event.message.address    # 地址
    lat=str(event.message.latitude)    # 緯度
    lon=str(event.message.longitude)   # 經度

    if addr is None:
        msg=f'收到GPS座標：({lat}, {lon})\n謝謝您！'
    else:
        msg=f'收到GPS座標：({lat}, {lon})。\n地址：{addr}\n謝謝您！'

    if  me['save']:
        me['logs']['經緯度'] = f'({lat}, {lon})'
        me['logs']['地址'] = addr

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=msg),
                TextSendMessage(text='請問是什麼狀況呢？')
        ])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        
    
    
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
