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
import os

gs = sheet.GoogleSheet('LineBotDATA','工作表1')

line_bot_api = LineBotApi('lPkuq0new8upb+bh5muA9vU9w/BNy5+QQhk7r3cFxqdL9wcv6n2ue1/jxzWPiCBXSvo0agpYhE4X55liDKoAz6yxoOFxwL/FCUtjEX3TQz+IFDzwuWNmYFxpSgaVenl3Qn4lwPVM7n7FL79qK5DagAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e8a1992d6f0fa55a5509d6f7145835b0')

users = {}

def check_user(id, name):
    global users

    if id not in users:
        users[id] = {
            'name':name,
            'logs':{'日期時間':'', '經緯度':'', '地址':'', '事由':''},
            'save':False 
        }

app = Flask(__name__)

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
    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id)
    # 紀錄用戶資料
    _name = profile.display_name
    print('大頭貼網址：', profile.picture_url)
    print('狀態消息：', profile.status_message)
    check_user(_id, _name)

    txt=event.message.text

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
