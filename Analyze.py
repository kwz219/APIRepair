from Analyze.DataAnalyze import Analyze_API4Fix,Analyze_JDKAPI_percent
from DataProcess.ReadMongo import load_dict
if __name__ =="__main__":
    #Count_APIMU_APIPercent("D:\\apirep\Data\\BAdif.dict","D:\\apirep\Data\\API4FixCount.dict")
    Analyze_JDKAPI_percent("D:\\apirep\Data\\API4FixCount.dict")
    Analyze_JDKAPI_percent("D:\\apirep\Data\\APIVocab.dict")
