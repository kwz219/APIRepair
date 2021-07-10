import pymongo
myclient = pymongo.MongoClient("mongodb://172.29.7.221:27017/")
mydb = myclient["APISeq"]
apiCol=mydb["jdk_api"]
methodCol=mydb['method_info']
projectCol=mydb['project_info']
def read_apiseq():
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
                      '_id':0,
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
    for re in results:
        seq=re["task_docs"]
        methodname=re["methodName"]
        filepath=re["filepath"]
        for api in seq:
            api=str(api['signature'])
            if api not in apidict.keys():
                apidict[str(api)]=len(apidict)+1
                print(len(apidict),str(api)+"  added")
    write_dict(apidict,"apivocab.txt")

def write_dict(dict,save_path):
    with open(save_path,'w',encoding='utf8') as f:
        f.write(str(dict))
        f.close()
def load_dict(dict_path):
    f=open(dict_path,'r',encoding='utf8')
    fdict=f.read()
    return eval(fdict)
if __name__ =="__main__":
    read_apiseq()