from DataProcess.IOHelper import read_lines
#计算各个类别的ACC
def category_eval(category,preds,labels):
    category_labels=[1 for i in range(len(category))]
    category_hits=[0 for i in range(len(category))]
    category_acc={}
    assert len(preds)==len(labels)
    for pred,label in zip(preds,labels):
        for p,l in zip(pred,label):
            if l in category:
                category_labels[l]+=1
                if p==l:
                    category_hits[l]+=1
    for i in range(len(category_labels)):
        category_acc[i]=category_hits[i]/category_labels[i]*100
    return category_acc
def eval_category_ACC(preds_path,label_path):
    preds=read_lines(preds_path)
    labels=read_lines(label_path)
    preds=[eval(i) for i in preds]
    labels=[eval(i) for i in labels]
    print(category_eval([0,1,2,3,4],preds,labels))

print(eval_category_ACC("D:\BFPPreds\model_epoch9.pred","D:\BFPPreds\model_epoch9.label"))