import requests
from bs4 import BeautifulSoup



def Guard():
    url = 'https://www.guardiantales.com/coupon/redeem/'
    UsersID = ['885827936452']
    GRCodes = ['HAPPYNEWYEAR','FRESHSTART','WINTERBLUESWHO','WORLDCOLDCOFFEEWARM']

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
            if sel == "Congratulations!You've successfully claimed the Coupon!Please check your mail in-game in order to redeem your rewards.":
                print(bcolors.OK + '成功。 ' + bcolors.RESET + i + "：" + '兌換' + j)
            elif sel == 'We were unable to find your User Number.Please double-check your User Number and the Region selected and try again.' :
                print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：UserID Error' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered is invalid.Please check the Coupon Code and try again.":
                print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號錯誤' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered has already been claimed.If you have not yet redeemed this Coupon Code, please double-check your User Number and the Region selected and try again." :
                print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號已兌換' +' (' + i + '_兌換_' + j + ')')
            elif sel == "The Coupon Code you've entered has already expired." :    
                print(bcolors.FAIL + ' 失敗。 ' + bcolors.RESET + '原因：序號過期' +' (' + i + '_兌換_' + j + ')')
