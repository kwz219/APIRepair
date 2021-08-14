from DataProcess.IOHelper import write_lines,read_lines
from DataProcess.ReadMongo import load_dict
import difflib

EDIT_TYPE={"equal":"0","delete":"1","replace":"1","insert_before":"1","insert_after":"1"}#insert这一类型的错误单独考虑
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
        labellist.append(' '.join(build_label(buggyseq,fixedseq)))
        seqlist.append(' '.join(buggyseq))
        print(ind)
        ind+=1
    print(len(seqlist),len(labellist))
    write_lines(outputpre+".seq",seqlist)
    write_lines(outputpre+".2type.label",labellist)

#分成5类(实际上可能不需要)
def build_label(false_seq,true_seq):
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
#只分成正确、错误两大类
def build_label(false_seq,true_seq):
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
                labels[i1]=EDIT_TYPE["insert_before"]

            elif i1==len(false_seq) and i2==len(false_seq):
                "在末尾插入"
                labels[i1-1]=EDIT_TYPE["insert_after"]
            else:
                "其他情况"
                labels[i1-1]=EDIT_TYPE["insert_after"]
    assert len(labels)==len(false_seq)
    return labels
def merge_labels(old_f,new_f):
    old_lines=read_lines(old_f)
    new_lines=[]
    for line in old_lines:
            line=line.replace('4','1')
            line=line.replace('2','1')
            new_lines.append(line)
    write_lines(new_f,new_lines)
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
    print(label_count)


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
#build_errorLabels()
merge_labels(r"D:\APIMU\MUCLS\test.label",r"D:\APIMU\MUCLS\test.2type.label")
merge_labels(r"D:\APIMU\MUCLS\trn.label",r"D:\APIMU\MUCLS\trn.2type.label")
merge_labels(r"D:\APIMU\MUCLS\val.label",r"D:\APIMU\MUCLS\val.2type.label")
count_labels(r"D:\APIMU\MUCLS\trn.2type.label")