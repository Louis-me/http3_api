__author__ = 'shikun'
# -*- coding:utf-8 -*-
import yaml
def getYam(homeyaml):
    try:
        with open(homeyaml, encoding='utf-8') as f:
            x = yaml.load(f)
            # print(x)
            return x
    except FileNotFoundError:
        print(u"找不到文件")
if __name__ == "__main__":
    import os
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    # getYam(PATH("../api.ymal"))

    http_config = {}
    api_config = []
    get_api_list = getYam(PATH("../api.ymal"))
    for key in get_api_list:
        if type(get_api_list[key]) != list:
            http_config[key] = get_api_list[key]
        else:
            api_config = get_api_list[key]
    print(http_config)
    print("------")
    print(list(api_config[0]["hopesql"].keys())[0])