""" Download GFS wind data from old windguru website """

import urllib.request

import bs4
import re
import datetime

import pandas as pd



def read_data_from_windguru_html(text_html, table_name, dt_table):

    # read targetted table
    temp = table_name + "([\s\S]*?)" + table_name
    text_table = re.findall(temp, text_html)
    text_table = text_table[0]

    # inside the table, change "null" with "0"
    text_table = text_table.replace("null", "0")

    # identify targets variables
    targets = re.findall(r',"([A-Z]+)":\[',text_table)

    # loop on targets to create data for dataframe
    data = []
    for target in targets:
        # select stings : targetstrings]
        pattern = target + r'([\s\S]*?)\]'
        strings = re.findall(pattern, text_table)
        # select only  first string
        temp = re.findall(r"[-+]?\d*\.\d+|\d+", strings[0])
        # save
        data.append(temp)

     # create dataframe
    df = pd.DataFrame(data)
    df = df.T
    df.columns = targets

    # create date times index
    temp = re.findall(r"\"initstamp\":([\s\S]*?)\,",
                            text_table)
    time0 = datetime.datetime.fromtimestamp(int(temp[0]))
    nt = len(df.iloc[:, 0])
    dti = pd.date_range(time0, periods=nt, freq=dt_table)

    # set index
    df.index = dti

    return df

def gfswind(p_html):
    
    url = r"https://old.windguru.cz/fr/index.php?sc=48572"
    contents = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(contents, "html.parser")
    text_html = soup.prettify()
    
    # get GFS 13km data
    df = read_data_from_windguru_html(text_html, "wg_fcst_tab_data_2", "3H")
    df.index.names = ["time"]
    df = df.astype("float")
    
    return df

def aromewind(p_html):
    
    url = r"https://old.windguru.cz/fr/index.php?sc=48572"
    contents = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(contents, "html.parser")
    text_html = soup.prettify()
    
    # get AROME 1.3km data
    df = read_data_from_windguru_html(text_html, "wg_fcst_tab_data_5", "1H")
    df.index.names = ["time"]
    df = df.astype("float")
    
    return df