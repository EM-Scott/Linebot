import requests
from bs4 import BeautifulSoup

def guard(GRCodes):
    url = 'https://www.guardiantales.com/coupon/redeem/'
    UsersID = ['89765498736423']
    
    for i in UsersID:
        for j in {GRCodes}:
            class bcolors: #顏色註記
                OK= '\033[92m' #GREEN
                WARNING= '\033[93m' #YELLOW
                FAIL= '\033[91m' #RED
                RESET= '\033[0m' #RESET COLOR
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
                state1 = (bcolors.OK + '成功。 ' + bcolors.RESET + i + "：" + '兌換' + j)
                state2 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：UserID Error' +' (' + i + '_兌換_' + j + ')')            
                state3 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號錯誤' +' (' + i + '_兌換_' + j + ')')            
                state4 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號已兌換' +' (' + i + '_兌換_' + j + ')')            
                state5 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號過期' +' (' + i + '_兌換_' + j + ')')
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
