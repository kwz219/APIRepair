from DataProcess.IOHelper import read_lines
def Acc_Beam(refs_f,preds_f,beam_size):
    refs=read_lines(refs_f)
    preds=read_lines(preds_f)
    assert len(preds)/beam_size == len(refs)
    totalnum=len(refs)
    hits=0
    for i in range(len(preds)):
        ref=refs[i]
        pred=preds[i*beam_size:(i+1)*beam_size]
        if len(pred)==1:
            hit=1 if pred[0].split()==ref.split() else 0
        else:
            hit=0
            for pr in pred:
                if pr.split() ==ref.split():
                    hit=1
                    break
        hits+=hit
    print(str(round(hits*100/totalnum,2))+"%")
Acc_Beam("D:\浏览器下载\\fixed.txt","D:\浏览器下载\BFP_46000.pred",1)
