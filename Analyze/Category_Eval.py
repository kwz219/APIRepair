from DataProcess.IOHelper import read_lines
from sklearn.metrics import classification_report
#计算各个类别的hit_rate
def category_eval(category,preds,labels):
    category_labels=[1 for i in range(len(category))]
    category_hits=[0 for i in range(len(category))]
    category_hitrate={}
    assert len(preds)==len(labels)
    for pred,label in zip(preds,labels):
        for p,l in zip(pred,label):
            if l in category:
                category_labels[l]+=1
                if p==l:
                    category_hits[l]+=1
    for i in range(len(category_labels)):
        category_hitrate[i]=category_hits[i]/category_labels[i]*100
    return category_hitrate
def eval_category(preds_path,label_path):
    preds=read_lines(preds_path)
    labels=read_lines(label_path)
    preds=[eval(i) for i in preds]
    labels=[eval(i) for i in labels]
    print(category_eval([0,1],preds,labels))
def category_CLS_report(preds_f,labels_f,classes=['Correct','Misuse']):
    preds=read_lines(preds_f)
    labels=read_lines(labels_f)
    preds_all,labels_all=[],[]
    for pred,label in zip(preds,labels):
        preds_all+=eval(pred)
        labels_all+=eval(label)
    assert len(preds_all) == len(labels_all)

    return classification_report(labels_all,preds_all,target_names=["class 0","class 1"])
#print(eval_category("D:\BFPPreds\CLS2model_epoch20.pred","D:\BFPPreds\CLS2model_epoch20.label"))
print(category_CLS_report("D:\BFPPreds\CLS2model_epoch50.pred","D:\BFPPreds\CLS2model_epoch50.label"))
