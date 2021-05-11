import os
from DataProcess.IOHelper import write_lines

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
def filter_events(event_list,filter_types,filter_keywords):

    filted_events=[]
    for event in event_list:
        if event['type'] in filter_types and hit(filter_keywords,event['description'])
            filted_events.append(event)
    return filted_events

if __name__ =="__main__":
    path="D:\浏览器下载\java_projects"
    filelist=filter_files("android",path)
    write_lines("API_FileList",filelist)