from DataProcess.ReadMongo import load_dict
from Analyze.DataAnalyze import CONTROL_NODES
import numpy as np
import matplotlib.pyplot as plt
def drawScatter(dict_path):
    apicount_dict=load_dict(dict_path)
    jdk_var=[]
    control_var=[]
    other_var=[]
    for key in apicount_dict.keys():
        if key in CONTROL_NODES:
            control_var.append(int(apicount_dict[key]))
        elif str(key).startswith("java"):
            jdk_var.append(int(apicount_dict[key]))
        else:
            other_var.append(int(apicount_dict[key]))

    plt.xlabel('api')
    plt.ylabel('count')
    plt.xlim(xmax=10000, xmin=0)
    plt.ylim(ymin=50, ymax=200)
    jdk_x = np.random.normal(5000, 1500, len(jdk_var))
    control_x = np.random.normal(5000, 1500, len(control_var))
    other_x = np.random.normal(5000, 1500, len(other_var))
    jdk_y=np.array(jdk_var)
    control_y=np.array(control_var)
    other_y=np.array(other_var)
    colors1 = '#00CED1'  # 点的颜色
    colors2 = '#DC143C'
    colors3 = 'grey'

    plt.scatter(jdk_x, jdk_y,  c=colors1, alpha=0.6, label='JDK_API')
    plt.scatter(control_x, control_y, c=colors2, alpha=0.6, label='CONTROL_NODE')
    plt.scatter(other_x, other_y, c=colors3, alpha=0.6, label='OTHER_API')
    plt.legend()
    plt.savefig(r'D:\apirep\Picture\50-200.png', dpi=300)
    plt.show()
drawScatter("D:\\apirep\Data\\API4FixCount.dict")