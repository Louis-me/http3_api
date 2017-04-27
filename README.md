# 项目名及简介

* 基于python3的自动化接口测试框架
* 采用对每组接口参数组合的方式进行请求测试,采用的PICT组合参数工具,所有请自己配置好PICT的运行环境

## 组合测试介绍

用更少的组合更简洁的用例，让覆盖率不减少，组合测试的分类

* 两因素组合测试（也称配对测试、全对偶测试）生成的测试集可以覆盖任意两个变量的所有取值组合。在理论上，该用例集可以暴露所有由两个变量共同作用而引发的缺陷。
* 多因素组合测试生成的测试集可以覆盖任意n和变量的所有取值组合。在理论上，该测试用例集可以发现所有n个因素共同作用引发的缺陷。

较好的测试组合的原则就是:

* 每个因子的水平值都能被测试到；
* 任意两个因子的各个水平值组合都能被测试到，这就叫配对测试法。
	* 此网站列出了所有的快速组合测试工具： http://www.pairwise.org/tools.asp
* 比如对一个接口中的三个参数生成了12组不同组合（1次是所有参数都对此接口验证通过，其他11次都是接口为失败的情况）

## 使用方式1

```
python httpRequest.py
```

## 其他功能介绍

* 对每组参数asyncio+aiohttp 进行压力测试
* yaml管理用例
* 检查点采用检查接口和访问数据库的方式进行检查
	* 如果正常参数直接访问数据库，如果是异常参数直接读取接口返回值

* 接口的参数的机密规则不提供，自己在代码中的传参中处理
* 接口依赖，建议在数据准备的时候进行处理好，每个接口都是独立测试

### 常用配置

* api.yaml

```
---
title: XXXX接口测试
host: int.dpool.sina.com.cn
port: 80
protocol: http://
header: {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}
database: {"databaseName":userinfo,"host":"1111", "user": "root", "password": "111", "port": 3306, "charset": "utf8"}
api_list:
- id: 1001
  name: 得到ip的归属地
  method: get
  url: /iplookup/iplookup.php
  stress: 1
  hope_sql: {"findKey": "findBySql", "sql": "select * from 1111", "params": { }}
  params:
  - "ip:ip:error:0:send_keys:218.4.255.255:type:str,ip:error:1,ip:error:2,ip:error:3:send_keys:22222:type:str"
  - "format:format:error:0:send_keys:json:type:str,format:error:1,format:error:2,format:error:3:send_keys:32321:type:str"
- id: 1002
  stress: 1
  method: post
  name: 得到个人信息
  url: /iplookup/iplookup.php
  hope_sql: {"findKey": "findBySql", "sql": "select * from info", "params": { }}
  params:
   - "ip:ip:error:0:send_keys:218.4.255.255:type:str,ip:error:1,ip:error:2,ip:error:3:send_keys:22222:type:str"
   - "format2:format2:error:0:send_keys:json:type:str,format2:error:1,format2:error:2,format2:error:3:send_keys:32321:type:str
  
```

- 注意配置信息error的值 0正常，1无此参数，2参数的值为空，3在数据库中不存.0和3查数据库，1,2直接读取接口返回信息

### 结果分析

待扩展

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
* 其他的坑待填，还是探索阶段

