from DataProcess.IOHelper import read_lines
def category_eval(preds,labels):
    category=[0,1,2,3,4]
    category_labels=[0,0,0,0,0]
    category_hits=[0,0,0,0,0]
    assert len(preds)==len(labels)
    for pred,label in zip(preds,labels):
        for p,l in zip(pred,label):
            if l in category:
                category_labels[l]+=1
                if p==l:
                    category_hits[l]+=1
    category_acc=[hit/sample*100 for hit,sample in zip(category_hits,category_labels)]
    return category_acc
def eval_category_ACC(preds_path,label_path):
    preds=read_lines(preds_path)
    labels=read_lines(label_path)
    preds=[list(i) for i in preds]
    labels=[list(i) for i in labels]
    print(category_eval(preds,labels))

print(category_eval([[0,0,2],[0,1,0],[0,0,2,0]],[[0,0,2],[4,0,3],[0,0,1,0]]))