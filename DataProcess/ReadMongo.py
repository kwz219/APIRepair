import pymongo
from bson.objectid import ObjectId
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["APISeq"]
apiCol=mydb["jdk_api"]
methodCol=mydb['method_info']
projectCol=mydb['project_info']
def read_seq(apidictpath,BApath):
    apidict=load_dict(apidictpath)
    print("apidict loaded")

    b_dict={}
    a_dict={}
    BAdict={}
    ind=0
    for me in methodCol.find():
        objid=str(me.get("_id"))
        refapiseq=me.get('apiSeq')
        filepath=me.get('filepath')
        mename=me.get('methodName')
        InOut=getInOutparam(me.get('code'))
        Meinfo=','.join([filepath,mename,InOut])
        apiseq = [apidict[str(api.id)] for api in refapiseq]
        if me.get('status')=="before":
                b_dict[Meinfo]=apiseq
        elif me.get('status')=="after":
                a_dict[Meinfo]=apiseq
        print(ind,objid,apiseq)
        ind+=1
    ind=0
    for key in a_dict.keys():
        befkey=key.replace("F_dir","P_dir")
        aseq=a_dict[key]
        if len(aseq)>1:
            if befkey in b_dict.keys():
               bseq=b_dict[befkey]
               if aseq != bseq:
                  BAdict[key]={"before":bseq,"after":aseq}
                  print(ind,bseq,aseq)
                  ind+=1
    write_dict(BAdict,BApath)
def read_code(BAcode_path):
    b_dict={}
    a_dict={}
    BAdict={}
    ind=0
    for me in methodCol.find():
        objid=str(me.get("_id"))
        filepath=me.get('filepath')
        mename=me.get('methodName')
        code=me.get('code')
        InOut=getInOutparam(code)
        Meinfo=','.join([filepath,mename,InOut])
        if me.get('status')=="before":
                b_dict[Meinfo]=code
        elif me.get('status')=="after":
                a_dict[Meinfo]=code
        print(ind,objid,Meinfo)
        ind+=1
    ind=0
    for key in a_dict.keys():
        befkey=key.replace("F_dir","P_dir")
        acode=a_dict[key]
        if befkey in b_dict.keys():
            bcode=b_dict[befkey]
            if acode != bcode:
                BAdict[key]={"before":bcode,"after":acode}
                print(ind)
                ind+=1
    print(len(BAdict))
    write_dict(BAdict,BAcode_path)


def write_objidjdk():
    jdkdict={}
    ind=0
    for jdk in apiCol.find():
        objid=jdk.get('_id')
        sig=jdk.get('signature')
        jdkdict[str(objid)]=sig
        ind+=1
        print(ind)
    with open("D:\\apirep\\objid_api.dict",'w',encoding='utf8')as f:
        f.write(str(jdkdict))
        f.close()
def read_apiseq(idfile,seqfile):
    apidict={}
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
                      'status':0,
                      'project_info':0,
                      'inParams':0,
                      'apiSeq':0,
                      'className':0,
                      '_class':0,
                  }
            },


        ]
    )
    idlist=[]
    apiseqlist=[]
    ind=0
    for re in results:
        seq=SimplifySeq(re["task_docs"])
        objid=re["_id"]
        idlist.append(str(objid))
        apiseqlist.append(" ".join(seq))
        print(ind,apiseqlist[-1])
        ind+=1
    with open(idfile,'w',encoding='utf8')as idf:
        for line in idlist:
            idf.write(line+'\n')
        idf.close()
    with open(seqfile,'w',encoding='utf8')as sf:
        for line in apiseqlist:
            sf.write(line+'\n')
        sf.close()



def write_dict(dict,save_path):
    with open(save_path,'w',encoding='utf8') as f:
        f.write(str(dict))
        f.close()
def load_dict(dict_path):
    f=open(dict_path,'r',encoding='utf8')
    fdict=f.read()
    return eval(fdict)
def filter_FixPair():
    afterdict=load_dict("afterdict.txt")
    beforedict=load_dict("beforedict.txt")
    filted_BAdict=dict()
    ind=0
    print("filtering......")
    for key in beforedict.keys():
        before_api=beforedict[key]
        after_api=afterdict[key]
        if before_api!=after_api:
            filted_BAdict[key]={"before":before_api,"after":after_api}
            ind+=1
            print(ind,{"before":before_api,"after":after_api})
    write_dict(filted_BAdict,"E:\PyCharmProjects\APIRepair\Data\\filtered_BA.txt")

def generate_FixPair():
    beforedict={}
    afterdict={}
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
    for re in results:
        seq=re['task_docs']
        codes=re['code']
        in_out=getInOutparam(codes)
        status=re['status']
        path=re['filepath']+r"\\"+re['methodName']+r"\\"+(in_out)

        if status=="after":
            afterdict[path]=SimplifySeq(seq)
            print("after",len(afterdict))

        elif status=="before":
            beforedict[path]=SimplifySeq(seq)
            print("before",len(beforedict))
    filted_BAdict=dict()
    ind=0
    print("filtering......")
    for key in beforedict.keys():
        afterkey=key.replace("P_dir","F_dir")
        if afterkey in afterdict.keys():
            before_api=beforedict[key]
            after_api=afterdict[afterkey]
            if before_api != after_api:
                filted_BAdict[key] = {"before": before_api, "after": after_api}
                ind += 1
                print(ind, {"before": before_api, "after": after_api})
    write_dict(filted_BAdict, "E:\PyCharmProjects\APIRepair\Data\\filtered_BA.txt")
def SimplifySeq(apiseq):
    simlist=[]
    for api in apiseq:
        simlist.append(api['signature'])
    return simlist
def getInOutparam(code):
    lines=code.split("\n")
    fline="ParseError"
    for line in lines:
        if "@" in line or len(line.split())<2:
            continue
        else:
            fline=line
            break
    fline_words=fline.split()
    for word in fline_words:
        if word in ["public","private","protected","static","final","abstract","native","strictfp","synchronized","volatile","transient"]:
            continue
        else:
            outtype=word
            break
    if "(" in fline:
        intype=fline.split("(")[1].split(")")[0]
    else:
        intype="ParseError"
    return(outtype+r"\\"+"("+intype+")")
def load_dict_fromlines(meinfo_filepath,apiseq_filepath):
    meinfo_list=[]
    apiseq_list=[]
    seqdict={}
    with open(meinfo_filepath,'r',encoding='utf8')as mf:
        for line in mf:
            meinfo_list.append(r"\\".join(line.split(",")[1:]))
        mf.close()
    with open(apiseq_filepath,'r',encoding='utf8')as mf:
        for line in mf:
            apiseq_list.append(line.strip().split(","))
        mf.close()
    for meinfo,apiseq in zip(meinfo_list,apiseq_list):
        seqdict[meinfo]=apiseq
    print(len(meinfo_list),len(apiseq_list))
    print("loaded",len(seqdict))
    return seqdict
def filter_BADifference(ameinfo_filepath,aapiseq_filepath,bmeinfo_filepath,bapiseq_filepath,BApath):
    beforedict=load_dict_fromlines(bmeinfo_filepath,bapiseq_filepath)
    afterdict=load_dict_fromlines(ameinfo_filepath,aapiseq_filepath)
    BAdict = {}
    ind=0
    """
    for key in afterdict.keys():
        befkey=key.replace("F_dir","P_dir")
        aseq=afterdict[key]
        if len(aseq)>1:
            if befkey in beforedict.keys():
               bseq=beforedict[befkey]
               if aseq != bseq:
                  BAdict[key]={"before":bseq,"after":aseq}
                  print(ind,bseq,aseq)
                  ind+=1
    write_dict(BAdict,BApath)
    """
if __name__ =="__main__":
    #filter_FixPair()
    #generate_FixPair()
    #read_apiseq("W:\PycharmProjects\APIRepair\Data\objid.txt","W:\PycharmProjects\APIRepair\Data\\apiseq.txt")
    #read_seq("D:\\apirep\Data\objid_api.dict","D:\\apirep\Data\\a_meinfo.txt","D:\\apirep\Data\\a_meseq.txt","D:\\apirep\Data\\b_meinfo.txt","D:\\apirep\Data\\b_meseq.txt")
    read_code("D:\\apirep\Data\\BAcodedif.dict")

