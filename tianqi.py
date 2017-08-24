# -*- coding = utf-8 -*-
# coding=gbk
# @author : wiley

from bs4 import BeautifulSoup
import requests
import xlwt
import os
from click._compat import raw_input

def getListByUrl(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    weathers = soup.select("#tool_site")
    title = weathers[1].select("h3")[0].text
    weatherInfos = weathers[1].select("ul")
    weatherList = list()
    for weatherInfo in weatherInfos:
        singleWeather = list()
        for li in weatherInfo.select('li'):
            singleWeather.append(li.text)
        weatherList.append(singleWeather)
    print(title)
    return weatherList, title

def getListByAddress(addressUrl, excelSavePath):
    # url = "http://lishi.tianqi.com/hefei/index.html"
    url = addressUrl
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    dates = soup.select(".tqtongji1 ul li a")
    workbook = xlwt.Workbook(encoding='utf-8')
    for d in dates:
        weatherList, title = getListByUrl(d["href"])
        booksheet = workbook.add_sheet(title, cell_overwrite_ok = True)
        for i, row in enumerate(weatherList):
            for j, col in enumerate(row):
                booksheet.write(i, j, col)
    workbook.save(excelSavePath)
        
if __name__ == "__main__":
    addressName = raw_input("input��\n")
    address = BeautifulSoup(requests.get('http://lishi.tianqi.com/').text, "html.parser")
    queryAddress = address.find_all('a', text=addressName)
    if len(queryAddress):
        savePath = raw_input("���⵽�иó������ݣ������뼴�������������ݵ�·�������������룬��Ĭ�ϱ��浽d:"+addressName+".xls��:\n")
        if not savePath.strip():
            if not os.path.exists('d:/'):
                os.makedirs('d:/')
            savePath =  "d:/"+addressName+".xls"
        for q in queryAddress:
            getListByAddress(q["href"], savePath)
            print("�������浽��" + savePath)
    else:
        print("����������")
