mport requests
from bs4 import BeautifulSoup

url = "https://www.guardiantales.com/coupon/reddem/"
UserID = ['124564563','212312323', '']
GRCode = ['defart', 'qwert']
for i in UserID:
    for j in GRCode:
        class bcolors:
            OK = '\033[92m' #GREEN
            WARNING = '\033[93m' #YELLOW
            FAIL = '\033[91m' #RED
            RESET = '\033[0m' #reset color

        payload=('region=SEA&' + 'userID=' + i + '&code=' + j )
        headers = {
            'contect-type': "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        soup = BeautifulSoup(response.text,"html.parser")
        sel = soup.find('p')
        print(payload)
        #print(soup)
        print(sel)

        if sel == "We were unable to find your User Number.Please double-check your User Number and the Region selected and try again.":
            print(成功)
        elif sel == "":
            print(失敗一)
        elif sel == "":
            print(失敗二）
        elif sel == "":
            print(失敗三）
        elif sel == "":
            print(失敗四）
