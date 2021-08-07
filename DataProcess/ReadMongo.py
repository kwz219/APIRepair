import pymongo
from bson.objectid import ObjectId

from DataProcess.IOHelper import write_lines

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["APISeq"]
apiCol=mydb["jdk_api"]
methodCol=mydb['method_info']
projectCol=mydb['project_info']
def read_Trueseq(apidictpath,seqpath):
    apidict=load_dict(apidictpath)
    print("apidict loaded")

    seqs=[]
    ind=0
    for me in methodCol.find():
        objid=str(me.get("_id"))
        refapiseq=me.get('apiSeq')
        apiseq = [apidict[str(api.id)] for api in refapiseq]
        seqs.append(apiseq)
        print(ind,objid,apiseq)
        ind+=1
    with open(seqpath,'w',encoding='utf8')as wf:
        for seq in seqs:
            wf.write(' '.join(seq)+'\n')
        wf.close()

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

#找出commit之后code有改变的java文件
def read_code(BAcode_path):
    b_dict={}
    a_dict={}
    BAdict=load_dict("D:\\apirep\Data\\BA.seq")
    becode=[]
    afcode=[]
    ind=0
    for me in methodCol.find():
        objid=str(me.get("_id"))
        filepath=me.get('filepath')
        mename=me.get('methodName')
        code=me.get('code')

        code_line=code.replace('\n',' ')
        code_line = code_line.replace('\r', ' ')
        InOut=getInOutparam(code)
        Meinfo=','.join([filepath,mename,InOut])
        Meinfo=Meinfo.replace('\\','\\\\')
        if len(code_line)>=10:
            if me.get('status')=="before":
                    b_dict[Meinfo]=code_line
            elif me.get('status')=="after":
                    a_dict[Meinfo]=code_line
            print(ind,objid,Meinfo)
            ind+=1
    ind=0
    beMeinfolist=[]
    becodelist=[]
    afMeinfolist=[]
    afcodelist=[]
    for key in BAdict.keys():
        a_key=key.replace("P_dir","F_dir")
        b_key=key.replace("F_dir","P_dir")
        if a_key in a_dict.keys() and b_key in b_dict.keys():
            afMeinfolist.append(a_key)
            beMeinfolist.append(b_key)
            afcodelist.append(a_dict[a_key])
            becodelist.append(b_dict[b_key])
            print(ind)
            ind+=1

    write_lines("D:\APIMU\Data\\raw_code\meinfo_filter.af",afMeinfolist)
    write_lines("D:\APIMU\Data\\raw_code\meinfo_filter.be", beMeinfolist)
    write_lines("D:\APIMU\Data\\raw_code\code_filter.af", afcodelist)
    write_lines("D:\APIMU\Data\\raw_code\code_filter.be", becodelist)



def write_objidjdk():
    jdkdict={}
    ind=0
    for jdk in apiCol.find():
        objid=jdk.get('_id')
        inParam = jdk.get("inParams")
        apiName=jdk.get("apiName")
        if inParam == None:
            sig=jdk.get("signature")
        else:
            sig=jdk.get("className")+"."+apiName+"("+",".join(inParam)+")"
        jdkdict[str(objid)]=sig
        ind+=1
        print(ind,sig)
    with open("D:\\apirep\\True_id_api.dict",'w',encoding='utf8')as f:
        f.write(str(jdkdict))
        f.close()


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
def build_API_vocab(BAdict_path,vocab_path):
    BAdict=load_dict(BAdict_path)
    apivocab={}
    ind=0
    for key in BAdict.keys():
        befseq=BAdict[key]["before"]
        aftseq=BAdict[key]["after"]
        for api in befseq:
            if api not in apivocab.keys():
                apivocab[api]=1
            else:
                apivocab[api]=apivocab[api]+1
        for api in aftseq:
            if api not in apivocab.keys():
                apivocab[api]=1
            else:
                apivocab[api]=apivocab[api]+1
        print(ind)
        ind+=1
    write_dict(apivocab,vocab_path)

if __name__ =="__main__":
    #filter_FixPair()
    #generate_FixPair()
    #read_apiseq("W:\PycharmProjects\APIRepair\Data\objid.txt","W:\PycharmProjects\APIRepair\Data\\apiseq.txt")

    #read_code("D:\\apirep\Data\\BAcodedif.path")
    #build_API_vocab("D:\\apirep\Data\\BAdif.dict","D:\\apirep\Data\\APIVocab.dict")
    #read_seq("D:\\apirep\\id_api.dict","D:\\apirep\Data\\BA.seq")
    read_code("")

