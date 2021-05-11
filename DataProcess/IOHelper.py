def write_lines(output_file,list):
    with open(output_file,'w',encoding='utf8')as f:
        for line in list:
            f.write(line+'\n')
        f.close()