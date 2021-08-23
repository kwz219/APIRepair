from DataProcess.IOHelper import read_lines
def Acc_Beam(refs_f,preds_f,beam_size):
    refs=read_lines(refs_f)
    preds=read_lines(preds_f)
    assert len(preds)/beam_size == len(refs)
    totalnum=0
    hits=0
    count=22115
    for i in range(len(preds)):

        ref=refs[i]
        pred=preds[i*beam_size:(i+1)*beam_size]
        if len(pred)==1:
            if len(ref.split())<=1000:
                hit=1 if pred[0].split()==ref.split() else 0
                totalnum+=1
        else:
            hit=0
            for pr in pred:
                if pr.split() ==ref.split():
                    hit=1
                    break
        hits+=hit
    print(str(round(hits*100/totalnum,2))+"%")
#分析定位正确与修复正确的关系
def analyze1(true_label_f,pred_label_f,true_f,pred_f):
    t_CLS=read_lines(true_label_f)
    p_CLS=read_lines(pred_label_f)
    t_lbl=read_lines(true_f)
    p_l=read_lines(pred_f)
    assert len(t_CLS)==len(p_CLS) and len(t_lbl)==len(p_l) and len(p_CLS)==len(p_l)
    fl_right=[]
    rep_right=[]
    ind=1
    for tc,pc,tl,pl in zip(t_CLS,p_CLS,t_lbl,p_l):
        if tc==pc:
            fl_right.append(ind)
        if tl==pl:
            rep_right.append(ind)
        ind+=1
    flr_repn=set(fl_right)-set(rep_right)#定位正确修复错误
    fln_repr=set(rep_right)-set(fl_right)#定位错误修复正确(理论上应该没有)
    assert len(fln_repr)==0
    return {"fl_rightrate":len(fl_right)/len(t_CLS)*100.0,"flRight_repNot":len(flr_repn)/len(fl_right)*100.0}
def count_length(file,MAX_LEN):
    lines=read_lines(file)
    count=0
    for line in lines:
        if len(line.split())>MAX_LEN:
            count+=1
    print(count/len(lines))

Acc_Beam("D:\\APIREP_pred\\chunk9.af","D:\\APIREP_pred\\APIREP_masked_s68000.pred",1)
Acc_Beam("D:\\raw_code_Pred\\test.be.mtok.f.1h","D:\\raw_code_Pred\\m50w_s12w.pred.1h",1)
Acc_Beam("D:\\raw_code_Pred\\test.be.mtok.f.4h","D:\\raw_code_Pred\\m50w_s12w.pred.4h",1)
count_length("D:\APIREP_pred\chunk9.af",110)
count_length("D:\APIREP_pred\chunk9.af",100)
#print(analyze1("D:\APIREP_pred\chunk9_true.2type.label","D:\APIREP_pred\chunk9_pred.2type.label","D:\APIREP_pred\chunk9.af","D:\APIREP_pred\APIREP_transformer_36000.pred"))