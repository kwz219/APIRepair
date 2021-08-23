from DataProcess.IOHelper import write_lines,read_lines
from DataProcess.ReadMongo import load_dict
import difflib

EDIT_TYPE={"equal":"0","delete":"1","replace":"2","insert_after":"3","insert_before":"4"}#insert这一类型的错误单独考虑
INSERT=3
def build_errorLabels(BAseq_path,outputpre):
    BAdict=load_dict(BAseq_path)
    seqlist=[]
    labellist=[]
    ind=0
    for key in BAdict.keys():
        before_seq=BAdict[key]["before"]
        if len(before_seq)<2:
            continue
        after_seq=BAdict[key]["after"]
        labellist.append(' '.join(build_label(before_seq,after_seq)))
        seqlist.append(' '.join(before_seq))
        print(ind)
        ind+=1
    write_lines(outputpre+"/mu.seq",before_seq)
    write_lines(outputpre+"/mu.label",labellist)

def reduce_MASK(seq):
    new_seq=[]
    last_MASK=False
    for ele in seq:
        if ele=='[MASK]':
            if last_MASK!=True:
                new_seq.append('[MASK]')
                last_MASK=True
        else:
            new_seq.append(ele)
            last_MASK=False
    return new_seq

def MASKerror(seq,labels):
    assert len(seq)==len(labels)
    masked_seq=[]
    for i in range(len(labels)):
        label=labels[i]
        if label=="4":
            masked_seq.append('[MASK]')
            masked_seq.append(seq[i])
        elif label=="3":
            masked_seq.append(seq[i])
            masked_seq.append('[MASK]')
        elif label=="0":
            masked_seq.append(seq[i])
        elif label=="1":
            masked_seq.append('[MASK]')
        elif label=="2":
            masked_seq.append('[MASK]')
    finalseq=reduce_MASK(masked_seq)
    return finalseq


def build_errorLabels_and_mask(buggyfile,fixedfile,outputpre):
    buggy_lines=read_lines(buggyfile)
    fixed_lines=read_lines(fixedfile)
    seqlist=[]
    labellist=[]
    assert len(buggy_lines) == len(fixed_lines)
    ind=0
    for buggy,fixed in zip(buggy_lines,fixed_lines):
        buggyseq=buggy.strip().split()
        fixedseq=fixed.strip().split()
        labels=build_label(buggyseq,fixedseq)
        masked_seq=MASKerror(buggyseq,labels)
        labellist.append(' '.join(labels))
        seqlist.append(' '.join(masked_seq))
        print(ind)
        ind+=1
    assert len(labellist)==len(seqlist)
    write_lines(outputpre+".beseq.masked",seqlist)
    write_lines(outputpre + ".label", labellist)
def build_errorLabels(buggyfile,fixedfile,outputpre):
    buggy_lines=read_lines(buggyfile)
    fixed_lines=read_lines(fixedfile)
    seqlist=[]
    labellist=[]
    assert len(buggy_lines) == len(fixed_lines)
    ind=0
    for buggy,fixed in zip(buggy_lines,fixed_lines):
        buggyseq=buggy.strip().split()
        fixedseq=fixed.strip().split()
        labellist.append(' '.join(build_label_2(buggyseq,fixedseq)))
        seqlist.append(' '.join(buggyseq))
        print(ind)
        ind+=1
    print(len(seqlist),len(labellist))
    #write_lines(outputpre+".seq",seqlist)
    write_lines(outputpre+".label",labellist)

#分成2类
def build_label_2(false_seq,true_seq):
    labels=[0 for i in range(len(false_seq))]
    s=difflib.SequenceMatcher(None,false_seq,true_seq)
    for tag,i1,i2,j1,j2 in s.get_opcodes():
        #print("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %(tag, i1, i2, false_seq[i1:i2], j1, j2, true_seq[j1:j2]))
        if tag !="insert":
            for i in range(i1,i2):
                labels[i]=EDIT_TYPE[tag]
        else:
            if i1==0 and i2==0:
                "在开头插入"
                labels[i1]=1
            elif i1==len(false_seq) and i2==len(false_seq):
                "在末尾插入"
                labels[i1-1]=1
            else:
                "其他情况"
                labels[i1-1]=1
    assert len(labels)==len(false_seq)
    return labels
#分成多类
def build_label(false_seq,true_seq):
    labels=[0 for i in range(len(false_seq))]
    s=difflib.SequenceMatcher(None,false_seq,true_seq)
    for tag,i1,i2,j1,j2 in s.get_opcodes():
        #print("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %(tag, i1, i2, false_seq[i1:i2], j1, j2, true_seq[j1:j2]))
        if tag !="insert":
            for i in range(i1,i2):
                if labels[i]==0:
                    labels[i]=EDIT_TYPE[tag]
        else:
            if i1==0 and i2==0:
                "在开头插入"
                #print("k")
                labels[i1]=EDIT_TYPE["insert_before"]

            elif i1==len(false_seq) and i2==len(false_seq):
                "在末尾插入"
                labels[i1-1]=EDIT_TYPE["insert_after"]
            else:
                "其他情况"
                labels[i1-1]=EDIT_TYPE["insert_after"]
    assert len(labels)==len(false_seq)
    return labels
def merge_labels(old_f,new_f,old_seq,new_seq):
    seqs=read_lines(old_seq)
    old_lines=read_lines(old_f)
    assert len(seqs)==len(old_lines)
    new_lines=[]
    new_seqs=[]
    for seq,labels in zip(seqs,old_lines):
            if len(labels.split())>2:
                labels=labels.replace('4','1')
                labels = labels.replace('2', '1')
                new_lines.append(labels)
                new_seqs.append(seq)
    write_lines(new_f,new_lines)
    write_lines(new_seq,new_seqs)
def count_labels(linefile):
    labels=read_lines(linefile)
    label_count={}
    for line in labels:
        label_list=line.strip().split()
        for l in label_list:
            if l in label_count.keys():
                label_count[l]+=1
            else:
                label_count[l]=1
    return label_count



#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\train\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\train\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\train")
#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\eval\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\eval\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\eval")
#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\test\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\test\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\test")
#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\train\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\train\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\train")
#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\eval\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\eval\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\eval")
#build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\test\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\test\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\test")
"""
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\train\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\train\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\train")
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\eval\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\eval\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\eval")
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50\test\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\test\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50\MUCLS\test")
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\train\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\train\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\train")
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\eval\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\eval\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\eval")
build_errorLabels(r"D:\浏览器下载\BFP_datasets\datasets\50-100\test\buggy.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\test\fixed.txt",r"D:\浏览器下载\BFP_datasets\datasets\50-100\MUCLS\test")
"""
#build_errorLabels("D:\APIREP_pred\\chunk9.be","D:\APIREP_pred\\chunk9.af","D:\APIREP_pred\chunk9_true")
#build_errorLabels("D:\APIREP_pred\\chunk9.be","D:\APIREP_pred\\APIREP_transformer_36000.pred","D:\APIREP_pred\chunk9_pred")
#build_errorLabels()
#merge_labels("D:\APIREP_pred\\chunk9.af","D:\APIREP_pred\\APIREP_transformer_36000.pred")
#merge_labels(r"D:\APIMU\MUCLS\trn.label",r"D:\浏览器下载\APIMUCLS_2\trn.label",r"D:\APIMU\MUCLS\trn.seq",r"D:\浏览器下载\APIMUCLS_2\trn.seq")
#merge_labels(r"D:\APIMU\MUCLS\val.label",r"D:\浏览器下载\APIMUCLS_2\val.label",r"D:\APIMU\MUCLS\val.seq",r"D:\浏览器下载\APIMUCLS_2\val.seq")
"""
trn_dic=count_labels(r"D:\BFP_MUCLS2\50\train.2type.label")
val_dic=count_labels(r"D:\BFP_MUCLS2\50\val.2type.label")
test_dic=count_labels(r"D:\BFP_MUCLS2\50\test.2type.label")
for key in trn_dic.keys():
    trn_dic[key]=trn_dic[key]+val_dic[key]+test_dic[key]
print(trn_dic)
"""
build_errorLabels_and_mask(r"D:\raw_code_Pred\raw_l5\chunk01234567.be",r"D:\raw_code_Pred\raw_l5\chunk01234567.af",r"D:\raw_code_Pred\raw_l5\chunk01234567")