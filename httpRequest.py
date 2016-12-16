__author__ = "shikun"
from DAL import httpConfig as hc
from DAL import gevents, dbConnection, httpParams
from common import operateYaml
from DAL.pairs import *
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
def myRequest(**kwargs):
  # {"appStatus": {"errorCode": 0,"message": "操作成功"},"content": {"nickname":"18576759587","user_id": 30}} 接口定义的规则
  # 现在只是考虑到了登陆后返回token,user_id这方面的需求

    method = kwargs["param_req"]["method"]
    get_login_params = 0 # 标识接受了返回多少个参数（user_id,token），用作后面拓展
    param = httpParams.params_filter(kwargs["param_result"])  # 请求参数的处理，如果这里有各种加密可从此处扩展
    # get_login_param表示此接口需要登陆返回来的id(token),一般登陆成功后返回的字段
    if kwargs["param_req"].get("is_first", "false") == "false" and kwargs["param_req"].get("get_login_param", "false") != "false":
        param[Const.LOGIN_KEY]= Const.LOGIN_VALUE
        get_login_params += 1
    if kwargs["param_req"]["method"] == Const.HTTP_POST:
        really_result = kwargs["http_config"].post(dict_post=kwargs["param_req"], param=param) # 发送post请求
    elif kwargs["param_req"]["method"] == Const.HTTP_GET:
        really_result = kwargs["http_config"].get(dict_get=kwargs["param_req"], param=param)  # 发送get请求
    if really_result.get("status_code") == 200:
        print("请求%s成功鸟" %method)
        if kwargs["param_req"].get("is_first", "false") != "false" :
            # 需要接口返回过来的login_key，如token,user_id）等，此时就不用查数据库作为检查点，检查点为直接读取响应结果
            if really_result["appStatus"]["errorCode"] == 0:
                Const.LOGIN_KEY = kwargs["param_req"]["login_key"]
                Const.LOGIN_VALUE = really_result["content"][Const.LOGIN_KEY]
                print("%s接口验证通过,不查数据库" %method)
                kwargs["result"]["success"] += 1
            else:
                print("%s接口测试失败,不查数据库~" %method)
                kwargs["result"]["failed"] += 1

        #如果实际的参数是异常,is_first表示是非登陆接口，就不查数据库.
        elif len(kwargs["param_result"].keys()) != len(param) - get_login_params:
            #根据接口返回的errorCode判断，假如errorCode=2表示参数异常
            if really_result["appStatus"]["errorCode"] == 2:
                print("%s接口异常参数检测通过" % method)
                kwargs["result"]["success"] += 1
            else:
                print("%s接口异常参数检测失败" % method)
                kwargs["result"]["failed"] += 1
            return
        else: #直接查询数据库作为检查点
            check_sql_key = kwargs["param_req"]["hope_sql"]["findKey"]  # 根据这里的key,来跳转到不同的数据库查询语句
            kwargs["param_req"]["hope_sql"]["params"] = param  # 已经处理好的请求参数传给数据库sql语句参数，结果为：params{"a":"b"}
            for item in kwargs["param_result"]:
                #  error: 0正常，1无此参数，2参数的值为空，3在数据库中不存.0和3查数据库，1,2直接读取接口返回信息
                error = kwargs["param_result"][item]["error"]
                if error == Const.NORMAL or error == Const.DROP:
                    if kwargs["check_sql"].findKeySql(check_sql_key, **kwargs["param_req"]["hope_sql"]):
                        print("%s数据库接口验证成功" %method)
                        kwargs["result"]["success"] += 1
                    else:
                        print("%s数据库接口验证失败" %method)
                        kwargs["result"]["failed"] += 1
                    return
                elif error == Const.DEFAULT or error == Const.EMPTY:
                    if really_result["appStatus"]["errorCode"] == 2: # 接口返回的2为参数异常
                        print("%s接口异常参数检测成功" %method)
                        kwargs["result"]["success"] += 1
                    else:
                        print("%s接口异常参数检测失败" % method)
                        kwargs["result"]["failed"] += 1
                    return
    else:
        print("请求发送失败,状态码为:%s" % really_result.get("status_code"))
def gevent_request(**kwargs):
    for i in kwargs["api_config"]:  # 读取各个接口的配置，api.ymal
        # 生成参数
        pict_param(params=i["params"], pict_params=Const.PICT_PARAMS,
                   pict_params_result=Const.PICT_PARAMS_RESULT)
        # 读取参数
        get_param = read_pict_param(Const.PICT_PARAMS_RESULT)
        count = len(get_param) # 根据不同分组参数，循环请求
        green_let = []
        req = {}
        for key in i:
            if key != "params":  # 过滤请求参数，参数上面已经处理好了
                req[key] = i[key]
        result = {}  # 统计数据
        result["name"] = req["name"]  # 接口名字
        result["method"] = req["method"]
        result["url"] = req["url"]
        result["sum"] = count
        result["stress"] = req["stress"]
        result["success"] = 0
        result["failed"] = 0
        kwargs["result"] = result
        for k in range(0, count):
            kwargs["param_result"] = get_param[k]  # 接口中不同的参数组合，是dict类型
            kwargs["param_req"] = req  #每次请求除组合参数之外的参数，如逾期只，请求的url,method,结束等
            for item in range(kwargs["param_req"]["stress"]):  # 压力测试,启动协程去压测
                green_let.append(gevents.requestGevent(myRequest(**kwargs)))
            for k in range(0, kwargs["param_req"]["stress"]):
                green_let[k].start()
            for k in range(0, kwargs["param_req"]["stress"]):
                green_let[k].join()
        Const.RESULT["info"].append(kwargs["result"])
def get_config(api_ymal):
    '''
    得到api.ymal中的设置的接口信息
    :param api_ymal:
    :return:
    '''
    http_config = {} # http信息的记录
    api_config = [] # api的记录记录
    get_api_list = operateYaml.getYam(api_ymal)
    for key in get_api_list:
        if type(get_api_list[key]) != list:
            http_config[key] = get_api_list[key]
        else:
            api_config = get_api_list[key]
    return http_config, api_config

if __name__ == "__main__":
    start_time = time.time()
    get_api_config = get_config(PATH("api.ymal"))
    http_conf = hc.ConfigHttp(dict_http=get_api_config[0]) # http请求的设置
    apiConfigs = get_api_config[1]
    check_sql = dbConnection. MySQLet(host=get_api_config[0]["database"]["host"], user=get_api_config[0]["database"]["user"],
                                     password=get_api_config[0]["database"]["password"], charset=get_api_config[0]["database"]["charset"],
                                     database=get_api_config[0]["database"]["databaseName"], port=get_api_config[0]["database"]["port"])
    gevent_request(http_config=http_conf, api_config=get_api_config[1], check_sql=check_sql)
    check_sql.close()
    end_time = time.time()
    print("共花费：""%.2f" % (end_time - start_time))
    print(Const.RESULT)

    #{'method': 'post', 'success': 32, 'stress': 2, 'failed': 0, 'url': '/mockjs/11463/login', 'name': '登陆', 'sum': 16}
    '''
    sum 表示此接口有16组参数
    stress: 表示每组参数压测两次
    method: 请求方法
    success: 成功请求次数
    failed:失败请求次数
    url:请求的网址
    name:接口名字
    '''
