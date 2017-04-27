import asyncio
import aiohttp
import json
from common import asyhttp
# -*- coding:utf-8 -*-

class fetch():
    def __init__(self, dict_http):
        '''
        http请求的封装，传入dict
        :param dict_http:
        '''
        self.dict_http = dict_http
    def get(self, url, param):
        data = {}
        _url = self.dict_http["protocol"] + self.dict_http["host"] + ":" + str(self.dict_http["port"]) + url
        print(_url +" get请求参数为:"+str(param))
        try:
            response = yield from aiohttp.request("GET", _url, headers=self.dict_http["header"], params=param)
            string = (yield from response.read()).decode('utf-8')
            if response.status == 200:
                data = json.loads(string)
            else:
                print("data fetch failed for")
                print(response.content, response.status)
            data["status_code"] = response.status
            print(data)
        except asyncio.TimeoutError:
            print("访问失败")
        except UnicodeDecodeError:
            print("接口崩溃了")
        return data
    def post(self,url, param):
        data = {}
        _url = self.dict_http["protocol"] + self.dict_http["host"] + ':' + str(self.dict_http["port"]) + url
        print(_url + " post接口参数为:" + str(param))
        try:
            response = yield from aiohttp.request('POST', _url, data=param)
            string = (yield from response.read()).decode('utf-8')
            if response.status == 200:
                data = json.loads(string)
            else:
                print("data fetch failed for")
                print(response.content, response.status)
            data["status_code"] = response.status
            print(data)
        except asyncio.TimeoutError:
            print("访问失败")
        return data
if __name__ == '__main__':
    url = '/iplookup/iplookup.php'
    # loop = asyncio.get_event_loop()
    tasks = []
    dict_http = {}
    dict_http["protocol"] = "http://"
    dict_http["host"] = "int.dpool.sina.com.cn"
    dict_http["port"] = 80
    dict_http["header"] = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}
    f = fetch(dict_http)
    asyhttp.asyn(f.get(url, param="format=json&ip=218.4.255.255"))
