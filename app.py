from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
    ConfirmTemplate, TemplateSendMessage,
    MessageAction, URIAction, LocationMessage,
    ButtonsTemplate,
    FollowEvent
)

line_bot_api = LineBotApi('lPkuq0new8upb+bh5muA9vU9w/BNy5+QQhk7r3cFxqdL9wcv6n2ue1/jxzWPiCBXSvo0agpYhE4X55liDKoAz6yxoOFxwL/FCUtjEX3TQz+IFDzwuWNmYFxpSgaVenl3Qn4lwPVM7n7FL79qK5DagAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e8a1992d6f0fa55a5509d6f7145835b0')

line_bot_api.push_message('U13827e14d459bb54ca2e0357703e920e', TextSendMessage(text='你可以開始了'))

app = Flask(__name__)

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

# 處理回應文字
def reply_text(token, id, txt):
    global users
    me = users[id]

    if (txt=='Hi') or (txt=="你好"):
        reply = f"{me['name']}你好！"
    elif '悄悄話' in txt:
        words = me['words']
        if words != '':
            reply = f'你的悄悄話是：\n\n{words}'
        else:
            reply = '放膽說出心裡的話吧～'
            me['save'] = True  # 準備儲存祕密
    elif me['save']:
        me['words'] = txt      # 儲存祕密
        me['save'] = False     # 停止儲存祕密
        reply = '我會好好保護這個祕密～'
    else:
        reply = txt  #學你說話

    msg = TextSendMessage(reply)
    line_bot_api.reply_message(token, msg)
    # stk = StickerSendMessage(
    #     package_id=3,
    #     sticker_id=233)
    # line_bot_api.reply_message(token, [msg, stk])

@handler.default()
def default(event):
    print('捕捉到事件：', event)

# 接收文字訊息的事件處理程式
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    # 紀錄用戶資料
    _id = event.source.user_id
    _name = profile.display_name
    _txt = event.message.text

    check_user(_id, _name)
    reply_text(event.reply_token, _id, _txt)
    

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

@handler.add(FollowEvent)
def followed(event):
    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id)
    _name = profile.display_name
    print('歡迎新好友，ID：', _id)
    print('名字：', _name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
