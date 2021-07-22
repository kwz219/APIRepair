import os
from DataProcess.IOHelper import write_lines
import json
import shutil
#过滤出所有Java文件
def filter_files(APIname,RootDir):
    count=0
    filenames=[]
    for root, dirs, files in os.walk(RootDir):
        for file in files:
            if file.endswith("java"):
                fullname = os.path.join(root, file)
                try:
                    with open(fullname,'r',errors="ignore")as f:
                         for line in f:
                             if APIname in line:
                                 print(fullname)
                                 filenames.append(fullname)
                                 break
                                 count+=1
                except Exception as e:
                    pass
                continue
    print(count)
    return filenames

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
def filter_fromCodeRep(org_dir,change_dict):
    pathlist=[]
    with open(change_dict,'r',encoding='utf8')as cf:
        for line in cf:
            pathlist.append(line.strip())
        cf.close()
    for path in pathlist:

    shutil.copy(r"E:\bug-fix\000021ead7afe80b8eb1d34d61fbaf6d41f30555\F_dir\src\main\java\jp\igapyon\diary\v3\gendiary\TodayDiaryGenerator.java",r"E:\bug-fix-Filter\000021ead7afe80b8eb1d34d61fbaf6d41f30555\F_dir\src\main\java\jp\igapyon\diary\v3\gendiary\TodayDiaryGenerator.java")
if __name__ =="__main__":
    """
    events=filter("D:\浏览器下载\\2015-01-01-15.json")
    for ev in events:
        print(ev["payload"]["commits"][0]["message"])
    """
    filter_fromCodeRep("","")