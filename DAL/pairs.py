__author__ = "shikun"
import os
from common import operateFile
from common.customConst import Const
import time
def pict_param(**kwargs):
    '''
    pict处理请求的参数
    :param kwargs:
    params: 请求的参数列表，类型为list
    pict_param: 用配对处理好的参数存储的
    :return:
    '''

    for item in kwargs["params"]:
        operateFile.write_txt(kwargs["pict_params"], item)
    os.popen("pict " + kwargs["pict_params"] + ">"+kwargs["pict_params_result"])

def read_pict_param(pict_params):
    '''
    读取本地e生成好了的接口请求参数
    :param pict_params:  本地路径
    :return: list
    '''
    result = operateFile.read_txt(pict_params)
    l_result = []
    if result:
        for info in range(len(result)):
            for item in range(len(result[info])):
                t_result = result[info][item].split(",")
                d_t = {}
                for i in t_result:
                    temp = i.split(":")
                    t = {}
                    t[temp[1]] = temp[2]
                    if len(temp) >= 4:
                        t[temp[3]] = temp[4]
                        t[temp[5]] = temp[6]
                    d_t[temp[0]] = t
                l_result.append(d_t)
    return l_result
if __name__ == "__main__":
    t = read_pict_param(Const.PICT_PARAMS_RESULT)
    print(t)