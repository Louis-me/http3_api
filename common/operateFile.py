__author__ = "shikun"
import os
import time
from common.customConst import Const
def check_file(f_path):
    if not os.path.isfile(f_path):
        print('文件不存在' + f_path)
        # sys.exit()
        return False
    else:
        return True
def mk_file(f_path):
    with open(f_path, 'w', encoding="utf-8") as f:
        print("创建文件成功")
        pass
def write_txt(f_path, line):
    if check_file(f_path) == False:
        with open(f_path, "w", encoding="utf-8") as f: #如果文件不存在，则创建文件
            print("创建成功"+f_path)
    time.sleep(1)
    with open(f_path, 'a') as fileHandle:
        fileHandle.write(line + "\n")
def read_txt(f_path):
    reslut = []
    print(f_path)
    if check_file(f_path) == False:
        with open(f_path, "w", encoding="utf-8") as f: #如果文件不存在，则创建文件
            print("创建成功"+f_path)
    time.sleep(1)
    with open(f_path, 'r', encoding="utf-8") as fileHandle:
        file_list = fileHandle.readlines()
        for i in file_list:
            temp = []
            temp.append(i.replace("\t", ",").strip("\n"))
            reslut.append(temp)
        reslut = reslut[1:]
        # print(reslut)
    remove_txt(Const.PICT_PARAMS_RESULT)
    remove_txt(Const.PICT_PARAMS)
    return reslut


def remove_txt(f_path):
    if check_file(f_path):
        os.remove(f_path)
        print("删除成功")