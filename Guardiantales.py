import requests
from bs4 import BeautifulSoup

def guard(A,B):
    url = 'https://www.guardiantales.com/coupon/redeem/'
    payload=('region=SEA&' + 'userId=' + A +'&code=' + B )
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, data=payload, headers=headers) # 送出資訊
    soup = BeautifulSoup(response.text,"html.parser")
    sel = soup.find('p').text #抓回顯示值

    class state: #結果清單
        state1 = ('成功。' + '序號:' + B)
        state2 = ('失敗。' + '(UserAD Error) ' + '序號:' + B)
        state3 = ('失敗。' + '(序號錯誤) ' + '序號:' + B)
        state4 = ('失敗。' + '(序號已兌換) ' + '序號:' + B)
        state5 = ('失敗。' + '(序號過期) ' + '序號:' + B)
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
    return name


def check_name(Z):
    class nick_name:#識別使用者ID
        ID1 = '考特：'
        ID2 = '球球：'
        ID3 = '軒軒：'
        ID4 = 'kawakil：'
        ID5 = 'Yun：'
        ID6 = '測試帳號：'
        ID7 = '我測試一下：'
        ID8 = '巴拉巴拉霸：'

    if Z == '885827936452':
        n_name = nick_name.ID1
    elif Z == '733122961641':
        n_name = nick_name.ID2
    elif Z == '477722973249':
        n_name = nick_name.ID3
    elif Z == '615722923499':
        n_name = nick_name.ID4
    elif Z == '989122951121':
        n_name = nick_name.ID5
    elif Z == '885827936452':
        n_name = nick_name.ID6
    elif Z == '32':
        n_name = nick_name.ID7
    elif Z == '98':
        n_name = nick_name.ID8
    else :
        n_name = Z
    return n_name
