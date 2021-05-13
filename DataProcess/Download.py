import wget
import ssl
def IsLeap(year):
    if (year%4==0 and year%100!=0) or (year%400==0):
        return True
    return False
def download_events(year):
    ssl._create_default_https_context = ssl._create_unverified_context
    hours=[str(i) for i in range(24)]
    tenstr=["01","02","03","04","05","06","07","08","09"]
    months_normal={"1":tenstr+[str(i) for i in range(10,32)],"2":tenstr+[str(i) for i in range(10,29)],"3":tenstr+[str(i) for i in range(10,32)],
                   "4":tenstr+[str(i) for i in range(10,31)],"5":tenstr+[str(i) for i in range(10,32)],"6":tenstr+[str(i) for i in range(10,31)],
                   "7":tenstr+[str(i) for i in range(10,32)],"8":tenstr+[str(i) for i in range(10,32)],"9":tenstr+[str(i) for i in range(10,31)],
                   "10":tenstr+[str(i) for i in range(10,32)],"11":tenstr+[str(i) for i in range(10,31)],"12":tenstr+[str(i) for i in range(10,32)]}
    months_leap={"1":tenstr+[str(i) for i in range(10,32)],"2":tenstr+[str(i) for i in range(10,30)],"3":tenstr+[str(i) for i in range(10,32)],
                   "4":tenstr+[str(i) for i in range(10,31)],"5":tenstr+[str(i) for i in range(10,32)],"6":tenstr+[str(i) for i in range(10,31)],
                   "7":tenstr+[str(i) for i in range(10,32)],"8":tenstr+[str(i) for i in range(10,32)],"9":tenstr+[str(i) for i in range(10,31)],
                   "10":tenstr+[str(i) for i in range(10,32)],"11":tenstr+[str(i) for i in range(10,31)],"12":tenstr+[str(i) for i in range(10,32)]}
    if IsLeap(year):
        months=months_leap
    else:
        months=months_normal
    for i in range(1,13):
        days=months[str(i)]
        if i<10:
            month=tenstr[i-1]
        else:
            month=str(i)
        for day in days:
            for hour in hours:
                url="https://data.gharchive.org/"+str(year)+"-"+month+"-"+day+"-"+hour+".json.gz"
                print(url)
                wget.download(url, 'W:\PycharmProjects\APIRepair\Data\Raw\\'+str(year)+"-"+day+"-"+hour+".json")
                print(str(year)+"-"+day+"-"+hour+"finished")
    print(months_normal)
download_events(2017)