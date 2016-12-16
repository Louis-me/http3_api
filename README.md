#项目名及简介

* 基于python3的自动化接口测试框架
* 采用对每组接口参数组合的方式进行请求测试,采用的PICT组合参数工具

## 组合测试介绍

用更少的组合更简洁的用例，让覆盖率不减少，组合测试的分类：
* 两因素组合测试（也称配对测试、全对偶测试）生成的测试集可以覆盖任意两个变量的所有取值组合。在理论上，该用例集可以暴露所有由两个变量共同作用而引发的缺陷。
* 多因素组合测试生成的测试集可以覆盖任意n和变量的所有取值组合。在理论上，该测试用例集可以发现所有n个因素共同作用引发的缺陷。

较好的测试组合的原则就是
* 每个因子的水平值都能被测试到；
* 任意两个因子的各个水平值组合都能被测试到，这就叫配对测试法。
	* 此网站列出了所有的快速组合测试工具： http://www.pairwise.org/tools.asp
* 比如对一个接口中的三个参数生成了12组不同组合（1次是所有参数都对此接口验证通过，其他11次都是接口为失败的情况）

## 使用方式

```
python httpRequest.py
```

## 其他功能介绍

* 对每组参数采用协程压测的方式进行压测
* yaml管理用例
* 支持登陆成功后返回token或者user_id给其他接口使用,如果接参数需要多个加密参数，留了扩展，自己去封装
* 检查点采用检查接口和访问数据库的方式进行检查
	* 如果正常参数直接访问数据库，如果是异常参数直接读取接口返回值
* 注意此框架暂时还是探索阶段，目标是实现平台化

### 常用配置

* 全局变量

```
PICT_PARAMS = "d:/params.txt" # 请求参数存放地址txt
PICT_PARAMS_RESULT = "d:/t2.txt" # 参数配对后的路径excel
# 数据库的常用字段
FIND_BY_SQL = "findBySql" # 根据sql查找
COUNT_BY_SQL = "countBySql" # 自定义sql 统计影响行数
INSERT = "insert" # 插入
UPDATE_BY_ATTR = "updateByAttr" # 更新数据
DELETE_BY_ATTR = "deleteByAttr" # 删除数据
FIND_BY_ATTR = "findByAttr" # 根据条件查询一条记录
FIND_ALL_BY_ATTR = "findAllByAttr"  #根据条件查询多条记录
COUNT = "count" # 统计行
EXIST = "exist" # 是否存在该记录
#接口简单点中的erro定义
NORMAL = "0" # 正常参数，可以到表里面找到
DEFAULT = "1" # 无此参数
EMPTY = "2" # 参数为空值，如name=''
DROP = "3" # 数据库中找不到此参数
# 接口统计
LOGIN_KEY = ""  # 登陆后返回的key
LOGIN_VALUE = ""  # 登陆后返回的value
RESULT = {"info": []} # 存最后结果
```

* api.yaml

```
---
title: XXXX接口测试
host: rap.taobao.org
port: 80
protocol: http://
header: {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}
database: {"databaseName":userinfo,"host":"127.0.0.1", "user": "root", "password": "", "port": 3306, "charset": "utf8"} #配置数据库
api_list:
- id: 1001
  name: 登陆
  method: post
  url: /mockjs/11463/login
  stress: 2
  hope_sql: {"findKey": "findBySql", "sql": "select * from info", "params": { }} #注意findKey的值，要对应全局变量里面的值
  params:
  - "user_name:user_name:error:0:send_keys:333:type:str,user_name:error:1,user_name:error:2,user_name:error:3:send_keys:22222:type:str"
  - "pwd:pwd:error:0:send_keys:111:type:str,pwd:error:1,pwd:error:2,pwd:error:3:send_keys:32321:type:str"
  # 注意这里的error,对应全局变量里面的error
  is_first: 1 # 预览的登陆接口
  login_key: user_id # 返回给其他接口使用的key
- id: 1002
  ...
  get_login_param: 1 # 需要登陆接口返回过来的参数
  
```


## 代码分析

* 入口代码

```
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

   
```

* 结果分析

```
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
```



# 其他

* 后面会简单把结果记录到excel中，发邮件
* 最终的目的是想做成平台化
