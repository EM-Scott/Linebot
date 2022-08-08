#輸入一個關鍵字，回傳youtube搜尋的前兩個影片
class youtubeBot:
    def youtubeBot(name):
        queryname = "+".join(name.split(" ")).lower()
        print("queryname:",queryname)
        r = requests.get("https://www.youtube.com/results?search_query="+queryname+"&gl=TW&hl=zh-TW")
        soup = BeautifulSoup(r.text, "html.parser")
        res = [""]
        for data in soup.select('a'):
            #print("data:", data)
            hit = re.search("v=(.*)",data['href'])
            if hit:
                h = hit.group(1)
                if re.search("list",h):
                    continue
                if h == res[-1][32:]:
                    continue
                res.append("https://www.youtube.com/watch?v="+h)
            if len(res) == 3:
                break
        return res[1:]
        #print("h:", h)
        #return "https://www.youtube.com/watch?v="+h
