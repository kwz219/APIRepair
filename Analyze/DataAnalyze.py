import pymongo
from DataProcess.ReadMongo import getInOutparam,load_dict,write_dict
def Count_AMUpercent(logfile):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["APISeq"]
    methodCol = mydb['method_info']
    results=methodCol.aggregate(
        [

            {
                '$lookup':
                    {
                        "from": "jdk_api",  # 需要联合查询的另一张表B
                        "localField": "apiSeq.$id",  # 表A的字段
                        "foreignField": "_id",  # 表B的字段
                        "as": "task_docs"  # 根据A、B联合生成的新字段名
                    },
            },
            {
              '$project':
                  {
                      "task_docs._id":0,
                      "task_docs.apiName":0,
                      "task_docs.className":0,
                      "task_docs._class":0,
                      'task_docs.inParams':0,
                      'task_docs.outParams':0,
                      'commithash':0,
                      'project_info':0,
                      'inParams':0,
                      'apiSeq':0,
                      'className':0,
                      '_class':0,

                  }
            },
        ]
    )
    beforedict={}
    afterdict={}
    BASeqDict=load_dict("E:\PyCharmProjects\APIRepair\Data\\filtered_BA.txt")
    for re in results:

        codes=re['code']
        in_out=getInOutparam(codes)
        status=re['status']
        path=re['filepath']+r"\\"+re['methodName']+r"\\"+(in_out)

        if status=="after":
            afterdict[path]=codes
            print("after",len(afterdict))

        elif status=="before":
            beforedict[path]=codes
            print("before",len(beforedict))
    ind=0
    print("Counting APIMU percent......")
    log_info=[]
    BA_CodeDict={}
    apichangecount=0
    apiunchangecount=0
    for key in beforedict.keys():
        afterkey=key.replace("P_dir","F_dir")
        if afterkey in afterdict.keys():
            before_code=beforedict[key]
            after_code=afterdict[afterkey]
            if before_code != after_code:
                BA_CodeDict[key]={"before":before_code,"after":after_code}
                if key in BASeqDict.keys():
                    log_info.append(key+" "+"code changed "+" apiseq changed")
                    apichangecount+=1
                else:
                    log_info.append(key + " " + "code changed " + " apiseq unchange")
                    apiunchangecount+=1
                ind += 1
                print(ind, log_info[-1])
    with open(logfile,'w',encoding='utf8')as f:
        for line in log_info:
            f.write(line+'\n')
        f.write("Total: APISeq changed: "+str(apichangecount)+" , unchange: "+str(apiunchangecount)+" Total Code changed: "+str(len(BA_CodeDict)))
        f.close()
    print(len(BASeqDict))
    write_dict(BA_CodeDict, "E:\PyCharmProjects\APIRepair\Data\\filtered_BA_rawcode.txt")

def apiseq_compare(befseq,afterseq):
    ptr=0
    while(ptr<max(len(befseq),len(afterseq))):
        pass

"统计修复APIMU过程中用到的各个API的占比"
def Count_APIMU_APIPercent(BAdict_path,FixAPICount_path):
    BAdict=load_dict(BAdict_path)
    APICount={}
    ind=0
    for key in BAdict.keys():
        bef_api=BAdict[key]["before"]
        aft_api=BAdict[key]["after"]
        Dif=[]
        for api in aft_api:
            if api not in bef_api:
                Dif.append(api)
        for ap in Dif:
            if ap in APICount.keys():
                APICount[ap]=APICount[ap]+1
            else:
                APICount[ap]=1
        print(ind)
        ind+=1
    write_dict(APICount,FixAPICount_path)
