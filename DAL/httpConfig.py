__author__ = "shikun"
import requests
import ast
import json

class ConfigHttp():
    def __init__(self, dict_http):
        '''
        http请求的封装，传入dict
        :param dict_http:
        '''
        self.dict_http = dict_http
    def get(self, dict_get, param):
        result = {}
        url = self.dict_http["protocol"] + self.dict_http["host"] + ":" + str(self.dict_http["port"]) + dict_get["url"]
        # print(url)
        r = requests.get(url, headers=self.dict_http["header"], params=param)
        r.encoding = 'UTF-8'
        if r.status_code == 200:
            result = json.loads(r.text)
        result["status_code"] = r.status_code
        return result
    def post(self, dict_post, param):
        url = self.dict_http["protocol"] + self.dict_http["host"] + ':' + str(self.dict_http["port"]) + dict_post["url"]
        r = requests.post(url, files=None, data=param)
        result = {}
        if r.status_code == 200:
            result = json.loads(r.text)
        result["status_code"] = r.status_code
        return result
if __name__=="__main__":
    param = {"id": 1, "rsa":"2123121", "token": "232131231"}
    r = requests.get("http://rap.taobao.org/mockjs/11463/getUserInfo", params=param)
    r.encoding = 'UTF-8'
    if r.status_code == 200:
        result = json.loads(r.text)
        print(result)
