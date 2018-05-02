__author__ = 'Administrator'
# -*- coding: utf-8 -*-
from aip import AipSpeech
import requests
import re
from bs4 import BeautifulSoup
import time
'''
爬取天气网-广州
http://www.weather.com.cn/weather/101280101.shtml
'''
def getHtmlText(url,code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''
def makeSoup(html):
    wstr = ''
    if html == '':
        return '哎呀~今天我也不知道广州的天气了！'
    else:
        soup = BeautifulSoup(html,'html.parser')
        soup1 = soup.find_all('li',attrs = {'class':'on'})[1]
        str1 = re.findall(r'>(.*)</',str(soup1))
        b = ''
        try:
            slist = re.findall(r'^(.*)</span>(.*)<i>(.*)$',str1[4])
            for x in range(len(slist[0])):
                b += slist[0][x]
        except:
            b = str1[4]
        if '/' in b:
            b = b.replace('/','-')
        str1[4] = '，广州的温度是'+b
        #print(str1[4])
        str1[6] = '，有风，风级是'+str1[6]
        for i in str1:
            if i != '':
                wstr = wstr +i
        if '雨' in wstr:
            wstr += '，如果出门的话，记得带上雨伞！'
        #去除掉字符串里面多余的字符
        wstr = wstr.replace('&lt;','')
        #print(wstr)
        print('今天有'+wstr[7:])
        return '今天有'+wstr[7:]
def transform_week():
    now_time_2 =time.strftime('%a',time.localtime())
    if now_time_2 == 'Mon':
        week = '星期一'
    elif now_time_2 == 'Tues':
        week = '星期二'
    elif now_time_2 == 'Wed':
        week = '星期三'
    elif now_time_2 == 'Thur':
        week = '星期四'
    elif now_time_2 == 'Fri':
        week = '星期五'
    elif now_time_2 == 'Sat':
        week = '星期六'
    else:
        week = '星期天'
    return week
'''
用百度的AIP
把文字变成mp3文件
'''
def stringToMp3(strings_txt):
    now_time_1 = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    strings_txt = '起床啦~爸爸~妈妈~奶奶~舅妈~还有最可爱的小豆宝~现在的时间是：' + now_time_1 + ',' + transform_week() + ',' + strings_txt
    print(strings_txt)
    APPID = '11157799'
    APIKey = 'X7I4xHQfa1iviwC59ueTdu0k'
    SecretKey = 'BjGhCaGdl8NKPi8TqQHyqiwwLIvzpRaS'

    aipSpeech = AipSpeech(APPID, APIKey, SecretKey)
    result = aipSpeech.synthesis(strings_txt,'zh','1',\
                                {'vol':10,
                                'per':4,
                                'spd':4})
    if not isinstance(result,dict):
        with open('test_tmp.mp3','wb') as f:
            f.write(result)

'''
执行的主函数
'''
def main():
    url = 'http://www.weather.com.cn/weather/101280101.shtml'
    html=getHtmlText(url)
    stringToMp3(makeSoup(html))

if __name__ == '__main__':
    main()