from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

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
    txt=event.message.text
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=txt)
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
