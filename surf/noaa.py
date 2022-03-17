""" Download buoy data from GFS wave forecasting product """

import requests
import bs4
import re
import datetime

import pandas as pd

def gfswave(p_html):
    
    # fecth data
    url = p_html
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    text_html = soup.prettify()
    
    # replace " " with "0"
    text_html = text_html.replace(" ", "0")
    
    # read runtime
    pat = r"(?<=\:).{13}(?=UTC)"
    temp = re.findall(pat,text_html)
    temp = temp[0]
    year = int(temp[1:5])
    month = int(temp[5:7])
    day = int(temp[7:9])
    hour = int(temp[10:12])
    
    rtime = datetime.datetime(year, month, day, hour, 0, 0)
    #stime = datetime.datetime(year, month, 1)
    
    # read table data
    pat = r"(?<=\|).{127}(?=\|)"
    temp = re.findall(pat,text_html)
    
    df = pd.DataFrame(temp)
    df = df[1:]
    df.columns = ["text"]
    
    df["day"] = df.text.apply(lambda x: float(x[1:3]))
    df["hour"] = df.text.apply(lambda x: float(x[4:6]))
    df["hourt"] = (df.index-1).to_list()

    df["hst"] = df.text.apply(lambda x: float(x[9:13]))
    
    df["hs1"] = df.text.apply(lambda x: float(x[23:27]))
    df["tp1"] = df.text.apply(lambda x: float(x[28:32]))
    df["dir1"] = df.text.apply(lambda x: (float(x[33:36])+180)%360)
    
    df["hs2"] = df.text.apply(lambda x: float(x[41:45]))
    df["tp2"] = df.text.apply(lambda x: float(x[45:50]))
    df["dir2"] = df.text.apply(lambda x: (float(x[51:54])+180)%360)
    
    df["hs3"] = df.text.apply(lambda x: float(x[59:63]))
    df["tp3"] = df.text.apply(lambda x: float(x[63:68]))
    df["dir3"] = df.text.apply(lambda x: (float(x[69:72])+180)%360)                             
  
    df["hs4"] = df.text.apply(lambda x: float(x[77:81]))
    df["tp4"] = df.text.apply(lambda x: float(x[81:86]))
    df["dir4"] = df.text.apply(lambda x: (float(x[87:90])+180)%360)
    
    df["hs5"] = df.text.apply(lambda x: float(x[95:99]))
    df["tp5"] = df.text.apply(lambda x: float(x[99:104]))
    df["dir5"] = df.text.apply(lambda x: (float(x[105:108])+180)%360)
    
    df["hs6"] = df.text.apply(lambda x: float(x[113:117]))
    df["tp6"] = df.text.apply(lambda x: float(x[117:122]))
    df["dir6"] = df.text.apply(lambda x: (float(x[123:126])+180)%360)  

    df["time"] = rtime + df["hourt"].map(lambda x: datetime.timedelta(hours=x)) 
    
    df = df.drop(["text", "hour", "day", "hourt"], axis=1)

    df.time = pd.to_datetime(df.time)
    df = df.set_index(["time"])                        
  
    return df