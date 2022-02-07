import requests
from bs4 import BeautifulSoup

def test(A,B):
    url = 'https://www.guardiantales.com/coupon/redeem/'
    payload=('region=SEA&' + 'userId=' + A +'&code=' + B )
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, data=payload, headers=headers) # 送出資訊
    soup = BeautifulSoup(response.text,"html.parser")
    sel = soup.find('p').text #抓回顯示值

    class state: #結果清單
        state1 = ('成功。' + A + "：" + '兌換' + B)
        state2 = ('失敗。' + '原因：UserAD Error' +' (' + A + '_兌換_' + B + ')')
        state3 = ('失敗。' + '原因：序號錯誤' + '\n(' + A + '_兌換_' + B + ')')
        state4 = ('失敗。' + '原因：序號已兌換' + '\n(' + A + '_兌換_' + B + ')')
        state5 = ('失敗。' + '原因：序號過期' + '\n(' + A + '_兌換_' + B + ')')
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
