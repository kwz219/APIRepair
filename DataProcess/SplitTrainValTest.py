from DataProcess.IOHelper import read_lines, write_lines
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
    write2file(trnset,r"D:\APIMU\Data\raw_l5/train")
    write2file(valset,r"D:\APIMU\Data\raw_l5/val")
    write2file(testset,r"D:\APIMU\Data\raw_l5/test")
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
def split_into(chunk,BAseq_path):
    BAseq = load_dict(BAseq_path)
    chunks=[[] for c in range(chunk)]
    for key in BAseq.keys():
        ind=random.randint(0,chunk-1)
        chunks[ind].append(BAseq[key])
    for i in range(len(chunks)):
        write2file(chunks[i],"D:\APIMU\Data\\raw_l5\\"+"chunk"+str(i))


def writeseq2file(seqlist, pathpre):
    with open(pathpre + ".seq", 'w', encoding='utf8')as bf:
        for line in seqlist:
            bf.write(line + '\n')
        bf.close()


def split_tseq_into(chunk,Tseq_path):
    chunks=[[] for c in range(chunk)]
    with open(Tseq_path,'r',encoding='utf8')as tf:
        for line in tf:
            ind=random.randint(0,chunk-1)
            chunks[ind].append(line.strip())
    for i in range(len(chunks)):
        writeseq2file(chunks[i],"D:\APIMU\Data\\tseq\\"+"chunk"+str(i))
def merge_seq_into(pathpre,mergeids):
    merged_seq=[]
    for ind in mergeids:
        with open(pathpre+"/chunk"+str(ind)+".seq",'r',encoding='utf8') as f:
            for line in f:
                merged_seq.append(line.strip())
            f.close()
    with open(pathpre+"\chunk"+''.join([str(i) for i in mergeids])+".seq",'w',encoding='utf8')as f:
        for line in merged_seq:
            f.write(line+'\n')
        f.close()
def merge_into(pathpre,mergeids):
    merged_be=[]
    merged_af=[]
    for type in ["af","be"]:
        for ind in mergeids:
            with open(pathpre+"/chunk"+str(ind)+"."+type) as f:
                for line in f:
                    if type=="af":
                        merged_af.append(line.strip())
                    else:
                        merged_be.append(line.strip())
                f.close()
    print(len(merged_af),len(merged_be))

    with open(pathpre+"\chunk"+''.join([str(i) for i in mergeids])+".af",'w',encoding='utf8')as f:
        for line in merged_af:
            f.write(line+'\n')
        f.close()
    with open(pathpre+"\chunk"+''.join([str(i) for i in mergeids])+".be",'w',encoding='utf8')as f:
        for line in merged_be:
            f.write(line+'\n')
        f.close()
"分割以code body per line形式存储的dataset"
def split_lines(pathpre,trn_p,val_p,test_p,outputpre):
    becodes=read_lines(pathpre+".be")
    afcodes=read_lines(pathpre+".af")
    assert len(becodes)==len(afcodes)
    trn_be,val_be,test_be=[],[],[]
    trn_af, val_af, test_af = [], [], []
    for bcode,acode in zip(becodes,afcodes):
        seed=random.random()
        if seed <=trn_p:
            trn_be.append(bcode)
            trn_af.append(acode)
        elif seed > trn_p and seed <=(trn_p+val_p):
            val_be.append(bcode)
            val_af.append(acode)
        elif seed > test_p:
            test_be.append(bcode)
            test_af.append(acode)
    write_lines(outputpre+"/trn.be",trn_be)
    write_lines(outputpre + "/trn.af", trn_af)
    write_lines(outputpre + "/val.be", val_be)
    write_lines(outputpre + "/val.af", val_af)
    write_lines(outputpre + "/test.be", test_be)
    write_lines(outputpre + "/test.af", test_af)


#split_tseq_into(10,r"D:\apirep\True.seq")
#merge_seq_into(r"D:\APIMU\Data\tseq",[0,1,2,3,4,5,6,7,8])
#split_into(10,r"D:\apirep\Data\BA_PL5.seq")
#merge_into(r"D:\APIMU\Data\raw_l5",[0,1,2,3,4,5,6,7])
split_lines("D:\APIMU\Data\\raw_code\\code",0.7,0.15,0.15,"D:\APIMU\Data\\raw_code")
