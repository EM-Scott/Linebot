import requests
from bs4 import BeautifulSoup



def Guard():
    url = 'https://www.guardiantales.com/coupon/redeem/'
    UsersID = ['885827936452','2452763765']
    GRCodes = ['HAPPYNEWYEAR']

    for i in UsersID:
        for j in GRCodes:
            class bcolors:
                OK= '\033[92m' #GREEN
                WARNING= '\033[93m' #YELLOW
                FAIL= '\033[91m' #RED
                RESET= '\033[0m' #RESET COLOR
                
            payload=('region=SEA&' + 'userId=' + i +'&code=' + j )
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            response = requests.request("POST", url, data=payload, headers=headers) # 送出資訊
            soup = BeautifulSoup(response.text,"html.parser")
            sel = soup.find('p').text #抓回顯示值
            #print(sel)
            class state:
                state1 = (bcolors.OK + '成功。 ' + bcolors.RESET + i + "：" + '兌換' + j)
                state2 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：UserID Error' +' (' + i + '_兌換_' + j + ')')            
                state3 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號錯誤' +' (' + i + '_兌換_' + j + ')')            
                state4 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號已兌換' +' (' + i + '_兌換_' + j + ')')            
                state5 = (bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號過期' +' (' + i + '_兌換_' + j + ')')

            if sel == "Congratulations!You've successfully claimed the Coupon!Please check your mail in-game in order to redeem your rewards.":
                # print(state.state1)
                name = state.state1
                # print(bcolors.OK + '成功。 ' + bcolors.RESET + i + "：" + '兌換' + j)
            elif sel == 'We were unable to find your User Number.Please double-check your User Number and the Region selected and try again.' :
                # print(state.state2)
                name = state.state2
                # print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：UserID Error' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered is invalid.Please check the Coupon Code and try again.":
                # print(state.state3)
                name = state.state3
                # print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號錯誤' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered has already been claimed.If you have not yet redeemed this Coupon Code, please double-check your User Number and the Region selected and try again." :
                # print(state.state4)
                name = state.state4
                # print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號已兌換' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered has already expired." : 
                # print(state.state5)
                name = state.state5
                # print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號過期' +' (' + i + '_兌換_' + j + ')')
            print(name)
            try: resule = name
            except: return "兌換失敗"
            return resule
