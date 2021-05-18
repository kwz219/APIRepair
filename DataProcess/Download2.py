# coding=utf-8
from urllib import request
import ssl
import json
from requests import Session
import time
import wget
from DataProcess.Filter import filter
def IsLeap(year):
    if (year%4==0 and year%100!=0) or (year%400==0):
        return True
    return False
def download_events(year,min_month,min_day,min_hour):
    session=Session()
    session.proxies={'https':'127.0.0.1:7890','http':'127.0.0.1"7890'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    hours = [str(i) for i in range(24)]
    tenstr = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    months_normal = {"1": tenstr + [str(i) for i in range(10, 32)], "2": tenstr + [str(i) for i in range(10, 29)],
                     "3": tenstr + [str(i) for i in range(10, 32)],
                     "4": tenstr + [str(i) for i in range(10, 31)], "5": tenstr + [str(i) for i in range(10, 32)],
                     "6": tenstr + [str(i) for i in range(10, 31)],
                     "7": tenstr + [str(i) for i in range(10, 32)], "8": tenstr + [str(i) for i in range(10, 32)],
                     "9": tenstr + [str(i) for i in range(10, 31)],
                     "10": tenstr + [str(i) for i in range(10, 32)], "11": tenstr + [str(i) for i in range(10, 31)],
                     "12": tenstr + [str(i) for i in range(10, 32)]}
    months_leap = {"1": tenstr + [str(i) for i in range(10, 32)], "2": tenstr + [str(i) for i in range(10, 30)],
                   "3": tenstr + [str(i) for i in range(10, 32)],
                   "4": tenstr + [str(i) for i in range(10, 31)], "5": tenstr + [str(i) for i in range(10, 32)],
                   "6": tenstr + [str(i) for i in range(10, 31)],
                   "7": tenstr + [str(i) for i in range(10, 32)], "8": tenstr + [str(i) for i in range(10, 32)],
                   "9": tenstr + [str(i) for i in range(10, 31)],
                   "10": tenstr + [str(i) for i in range(10, 32)], "11": tenstr + [str(i) for i in range(10, 31)],
                   "12": tenstr + [str(i) for i in range(10, 32)]}
    if IsLeap(year):
        months = months_leap
    else:
        months = months_normal
    for i in range(1, 13):
        days = months[str(i)]
        if i < 10:
            month = tenstr[i - 1]
        else:
            month = str(i)
        for day in days:
            for hour in hours:
                if (i > min_month) or (i == min_month and int(day)>min_day) or (i == min_month and int(day)==min_day and int(hour)>min_hour):
                    url = "https://data.gharchive.org/" + str(year) + "-" + month + "-" + day + "-" + hour + ".json.gz"
                    #print(url)
                    r = session.get(url=url, headers=headers)
                    with open("E:\API\Data\Raw\githubEvents"+str(year)+"\\"+str(year) + "-" + month + "-" + day + "-" + hour + ".json.gz", "wb") as f:
                        f.write(r.content)
                        f.flush()
                    print(str(year) + "-" + month + "-" + day + "-" + hour + "  Finished")
def download_eventurl_content(jsonfile,least_id):
    print("Filtering")
    events = filter(jsonfile)
    print("Filter finished")
    print("total",len(events))
    token="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"
    i=1
    for ev in events:
        id=ev["id"]
        json_url=ev["payload"]["commits"][0]["url"]
        if int(id)<least_id:
            i=i+1
            continue
        try:
            html = request.urlopen(json_url+"?access_token="+token)
            hjson = json.loads(html.read())
            with open("E:\API\Data\Filted\\2016\\"+jsonfile[24:-5]+"-"+str(id)+".json",'w',encoding="utf8")as f:
                json.dump(hjson,f)
                f.close()
            print(i,id,"finished")
        except Exception:
            pass
        i=i+1



download_eventurl_content("E:\API\Data\Raw\\raw2016\\2016-01-01-0.json",3486707015)