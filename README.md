#项目名及简介

* 基于python3的自动化接口测试框架
* 采用对每组接口参数组合的方式进行请求测试,采用的PICT组合参数工具,所有请自己配置好PICT的运行环境

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
  is_first: 1 # 预览的登陆接口
  login_key: user_id # 返回给其他接口使用的key
- id: 1002
  ...
  get_login_param: 1 # 需要登陆接口返回过来的参数
  
```

- 注意配置信息error的值 0正常，1无此参数，2参数的值为空，3在数据库中不存.0和3查数据库，1,2直接读取接口返回信息

### 结果分析

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
