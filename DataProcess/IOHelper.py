import json
def write_lines(output_file,list):
    with open(output_file,'w',encoding='utf8')as f:
        for line in list:
            f.write(line+'\n')
        f.close()
def read_from_json(json_file):
    event_list=[]
    with open(json_file,'r',encoding='utf8')as jf:
        for line in jf:
            event_list.append(json.loads(line.strip()))
        jf.close()
    return event_list
def read_lines(file):
    lines=[]
    with open(file,'r',encoding='utf8')as f:
        for line in f:
            lines.append(line.strip())
    return lines
def write_TokenCLSoutput(dir,preds,labels,epoch,model,max_seq_len):
    pred_lines=[]
    label_lines=[]
    assert len(labels)==len(preds) and len(labels)%max_seq_len==0
    lens=int(len(labels)/max_seq_len)
    print(len(labels),len(labels)/max_seq_len)
    for i in range(lens):
        one_pred=preds[i*max_seq_len:i*(max_seq_len+1)]
        one_label=labels[i * max_seq_len:i * (max_seq_len + 1)]
        ignore_len=one_label.count(-100)#-100是用于pad的无效标签
        pred_lines.append(str(one_label[:-ignore_len]))
        label_lines.append(str(one_pred[:-ignore_len]))
    write_lines(dir+model+'_'+'epoch'+str(epoch)+'.pred',pred_lines)
    write_lines(dir + model + '_' + 'epoch' + str(epoch) + '.label', label_lines)

if __name__ =="__main__":
    ev_list=read_from_json("D:\浏览器下载\\2015-01-01-15.json")
    print(ev_list[0])
    print(ev_list[10000])