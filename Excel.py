import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 建立憑證
cr = sac.from_json_keyfile_name('D:\Python\Learn\Python 教材\F9796\ch07\model\google_auth.json', scope)  # 請自行修改檔名
gs = gspread.authorize(cr)

sh = gs.open('LineBotDATA')  # 請自行修改試算表名稱
wks = sh.sheet1
# wks = sh.worksheet('網拍價格')

# wks.update_acell('D2', 'swf.com.tw')
# wks.update_cell(2, 5, 'swf.com.tw')

values = ['日期時間', '商品標題', '價格', '網址']
wks.insert_row(values, 1)
# wks.resize(1)
