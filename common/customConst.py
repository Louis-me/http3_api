__author__ = "shikun"
class Const(object):
    PICT_PARAMS = "d:/params.txt" # 请求参数存放地址txt
    PICT_PARAMS_RESULT = "d:/t2.txt" # 参数配对后的路径excel
    HTTP_POST = "post"
    HTTP_GET = "get"

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


    RESULT = {"info": []} # 存最后结果
    # RESULT = {"info": [{"name": "登陆接口", "sum": 5, "success": 5, "failed": 0, "url": "/api/login", "stress": 2},
    #                    {"name": "得到个人信息", "sum": 5, "success": 5, "failed": 0, "url": "/api/getUserInfo"}]}

