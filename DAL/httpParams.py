__author__ = "shikun"
from common.customConst import Const
def params_filter(params):
    '''
    请求参数处理
    :param params:
    :return:
    '''

    result = {}
    for wap_key in params:
        for son_key in params[wap_key]:
            if params[wap_key]["error"] == Const.EMPTY:
                pass
            if params[wap_key]["error"] == Const.DEFAULT:
                pass
            if params[wap_key]["error"] == Const.NORMAL or params[wap_key]["error"] == Const.DROP:
                result[wap_key] = change_format(params[wap_key]["type"], params[wap_key]["send_keys"])
            break
    return result


def change_format(key, param):
    param_type = {
        "str": lambda: str(param),
        "int": lambda: int(param),
        "float": lambda: float(param),
        "bool": lambda:  bool(param)
    }
    return param_type[key]()
if  __name__ == "__main__":
    '''
    error: 0正常，1无此参数，2参数的值为空，3在数据库中不存
    '''
    t1 = {'user_name': {'error': '2'}, 'pwd': {'error': '1'}, "id":{"error":"0", "send_keys": "333", "type":"str"}, "uid":{"error":"3", "send_keys": "444", "type":"str"}}
    print(params_filter(t1))