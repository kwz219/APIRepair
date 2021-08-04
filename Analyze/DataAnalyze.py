import pymongo
from DataProcess.ReadMongo import getInOutparam,load_dict,write_dict

CONTROL_NODES=[ "<try>", "</try>", "<catch>", "</catch>", "<finally>", "</finally>",
                "<while_condition>", "</while_condition>", "<while_body>", "</while_body>",
                "<if_condition>", "</if_condition>", "<if_body>", "</if_body>",
                "<else_body>", "</else_body>",
                "<for_condition>", "</for_condition>", "<for_body>", "</for_body>",
                "<switch_condition>", "</switch_condition>", "<case_body>", "</case_body>"]
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
def Count_API4FixPercent(BAdict_path,FixAPICount_path):
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
def Analyze_API4Fix(FixAPICount_path):
    API4Fixdict=load_dict(FixAPICount_path)
    rank=sorted(API4Fixdict.items(),key=lambda x:x[1],reverse=True)
    filtered_rank=[]
    for r in rank:
        if "java" not in r[0] and '<' not in r[0]:
            filtered_rank.append(r)
    print(filtered_rank[:20])
def Analyze_JDKAPI_percent(dict_path):
    apidict=load_dict(dict_path)
    print(len(apidict))
    CONTROL_COUNT=0
    JDK_API_COUNT=0
    OTHER_API_COUNT=0
    for key in apidict.keys():
        if str(key).startswith("java"):
            JDK_API_COUNT+=int(apidict[key])
        elif str(key) in CONTROL_NODES:
            CONTROL_COUNT+=int(apidict[key])
        else:
            OTHER_API_COUNT+=int(apidict[key])
    total_count=CONTROL_COUNT+JDK_API_COUNT+OTHER_API_COUNT
    print(JDK_API_COUNT,JDK_API_COUNT/total_count*100)
    print(CONTROL_COUNT, CONTROL_COUNT / total_count * 100)
    print(OTHER_API_COUNT, OTHER_API_COUNT / total_count * 100)

def Count_PatchLength(BAdict_path):
    BAdict = load_dict(BAdict_path)
    PL_count={}
    for key in BAdict.keys():
        bef_api=BAdict[key]["before"]
        aft_api=BAdict[key]["after"]
        length=str(len(aft_api)-len(bef_api))
        if length not in PL_count.keys():
            PL_count[length]=1
        else:
            PL_count[length]=PL_count[length]+1
    print(PL_count)
    write_dict(PL_count,"PLcount.dict")

def Filter_byPL(BAdict_path,PL_length):
    BAdict=load_dict(BAdict_path)
    filtered_dict={}
    for key in BAdict.keys():
        val=BAdict[key]
        bef_api=val["before"]
        aft_api=val["after"]
        length=abs(len(aft_api)-len(bef_api))
        if length<=PL_length:
            filtered_dict[key]=val
    write_dict(filtered_dict,"D:\\apirep\Data\\BA_PL5.seq")

Filter_byPL("D:\\apirep\Data\\BA.seq",5)