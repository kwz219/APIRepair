import os
from DataProcess.IOHelper import write_lines, read_lines
import json
import shutil
#过滤出所有Java文件
from DataProcess.ReadMongo import load_dict


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
"从BAcode里面找出与BAseq对应的code对"
def match_code2seq(beinfo_f,afinfo_f,becode_f,afcode_f,baseqdict_f):
    beinfo=read_lines(beinfo_f)
    afinfo=read_lines(afinfo_f)
    becode=read_lines(becode_f)
    afcode=read_lines(afcode_f)
    print(len(beinfo),len(afinfo),len(becode),len(afcode))
    #assert len(beinfo)==len(afinfo) and len(becode)==len(afcode) and len(afinfo)==len(becode)
    baseqdict=load_dict(baseqdict_f)
    for binfo,bcode,ainfo,acode in zip(beinfo,afinfo,becode,afcode):
        ainfo_key=bcode.replace('\\','\\\\')
        print(ainfo_key)
if __name__ =="__main__":
    """
    events=filter("D:\浏览器下载\\2015-01-01-15.json")
    for ev in events:
        print(ev["payload"]["commits"][0]["message"])
    """
    match_code2seq("D:\APIMU\Data\\raw_code\\meinfo.be","D:\APIMU\Data\\raw_code\\meinfo.af","D:\APIMU\Data\\raw_code\\code.be","D:\APIMU\Data\\raw_code\\code.af","D:\\apirep\Data\\BA.seq")