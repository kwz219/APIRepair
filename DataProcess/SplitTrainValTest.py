from DataProcess.ReadMongo import load_dict
import random

"按trn_p,val_p,test_p的概率划分训练集、验证集、测试集"
def Split_TrnValTest(BAseq_path,trn_p,val_p,test_p):
    BAseq=load_dict(BAseq_path)
    trnset=[]
    valset=[]
    testset=[]
    for key in BAseq.keys():
        seed=random.random()
        if seed <=trn_p:
            trnset.append(BAseq[key])
        elif seed > trn_p and seed <=(trn_p+val_p):
            valset.append(BAseq[key])
        elif seed > test_p:
            testset.append(BAseq[key])
    write2file(trnset,"../Data/train")
    write2file(valset,"../Data/val")
    write2file(testset,"../Data/test")
def write2file(set,pathpre):
    be=[]
    afs=[]
    for dic in set:
        be.append(" ".join(dic["before"]))
        afs.append(" ".join(dic["after"]))
    with open(pathpre+".be",'w',encoding='utf8')as bf:
        for line in be:
            bf.write(line+'\n')
        bf.close()
    with open(pathpre+".af",'w',encoding='utf8')as af:
        for line in afs:
            af.write(line+'\n')
        af.close()
def eval_datasize(srcfile,tgtfile):
    with open(srcfile,'r',encoding="utf8")as sf:
        be=sf.readlines()
        print(len(be))
        sf.close()
    with open(tgtfile,'r',encoding="utf8")as tf:
        af=tf.readlines()
        print(len(af))
        tf.close()
    assert len(be)==len(af)

Split_TrnValTest(r"D:\apirep\Data\BA.seq",0.8,0.1,0.1)
eval_datasize("../Data/train.be","../Data/train.af")
eval_datasize("../Data/val.be","../Data/val.af")
eval_datasize("../Data/test.be","../Data/test.af")
