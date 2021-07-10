# coding=utf-8
from urllib import request
import ssl
import json
from requests import Session
import time
import wget
import random

def hit(keywords,str):
    for word in keywords:
        if word in str:
            return True
    return False
"""
从github event事件列表中筛选出合适的事件
"""
def filter_events(json_path,filter_types,filter_keywords):
    events=[]
    with open(json_path,'r',encoding="utf8")as f:
        for line in f:
            event=json.loads(line.strip())
            events.append(event)
        f.close()

    filted_events=[]
    for event in events:
        if event['type'] in filter_types and len(event["payload"]["commits"])>0:
            if hit(filter_keywords,event["payload"]["commits"][0]["message"]):
                filted_events.append(event)
    return filted_events

def filter(json_path):
    filter_types=["PushEvent"]
    filter_keywords=["fix","Fix","FIX","Bug","bug","BUG","solution","Solution","problem","Problem","Correct","correct","debug","Debug"]
    return filter_events(json_path,filter_types,filter_keywords)

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
def download_eventurl_contents(filedir,downloaddir,githubtoken,year,min_month,min_day,min_hour,min_id):
    """
    :param filedir:  原始的json文件，每个json文件中包含某个时间段所有的github event事件
    :param downloaddir:  从原始json文件中下载特定事件到该文件夹
    :param githubtoken: 每个github账号均可生成的token，用于爬取github数据
    :param year: 从该年份起开始下载
    :param min_month: 从该月份开始下载
    :param min_day: 从该日开始下载
    :param min_hour: 从该时段开始下载
    :param min_id: 只下载大于等于该id编号的事件
    :return:
    """
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
                #只下载大于等于该日期或id的github event数据
                if (i > min_month) or (i == min_month and int(day)>min_day) or (i == min_month and int(day)==min_day and int(hour)>min_hour):
                    url = filedir+"\\" + str(year) + "-" + month + "-" + day + "-" + hour + ".json"
                    download_eventurl_content(url,min_id,githubtoken,downloaddir)
                    print("--------------------------------------------------------------")
                    print(str(year) + "-" + month + "-" + day + "-" + hour + "  Finished")
                    print("--------------------------------------------------------------")


def download_eventurl_content(jsonfile,least_id,githubtoken,downloaddir):
    session = Session()
    authorization='token '+githubtoken
    print(authorization)
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': str(authorization),
               'Content-Type': 'application/json',
               'Accept': 'application/json'
               }
    print("Filtering")
    events = filter(jsonfile)
    print("Filter finished")
    print("total",len(events))

    i=1
    for ev in events:
        id=ev["id"]
        json_url=ev["payload"]["commits"][0]["url"]
        if int(id)<least_id:
            i=i+1
            continue
        try:
            html = session.get(json_url,headers=headers)
            hjson = json.loads(html.content)

            #如果超过爬虫频率了，先等20分钟
            if "message" in hjson.keys():
                if "rate" in hjson["message"]:
                    time.sleep(1000)

            with open(downloaddir+"\\" +str(jsonfile.split('\\')[-1])+"-"+str(id)+".json",'w',encoding="utf8")as f:
                json.dump(hjson,f)
                f.close()
            print(i,id,"finished")
            time.sleep(0.2)
        except Exception as e:
            print(e)
            pass
        i=i+1

if __name__ =="__main__":

    #该段命令：下载E:\APIRepair\Data\Raw\\2020\\2020-01文件夹里的内容,下载到"E:\APIRepair\Data\Filter\\2020-01"里，github token是'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'
    #下载从2020年1月1日0时开始的GitHubevent数据，事件编号大于等于11185281240

    download_eventurl_contents("E:\APIRepair\Data\Raw\\2020\\2020-01","E:\APIRepair\Data\Filter\\2020-01",'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',2020,1,1,0,11185281240)
    #爬取github数据需要github_token，生成方法:https://www.cnblogs.com/leon-2016/p/9284837.html
    #多找几个github_token，可以并行下载

