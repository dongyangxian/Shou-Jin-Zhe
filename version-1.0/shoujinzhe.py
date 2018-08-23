import re
import pymysql

"""用于处理动态页面的请求，与web服务器对接的函数"""
"""
按照事先约定好的协议实现双方的通信(web服务器与框架应用程序)
    - web服务器把请求报文信息以字典形式传递给框架应用程序对接的函数
        env={"PATH_INFO":"/index.html"}
    - 在框架应用程序把处理的结果以返回值的形式返回给web服务器
        return '200 OK',[('Content-Type','text/html;charset=utf-8')],'response body'
"""
g_route_list = []

def route(url):
    def wrapper(func):
        g_route_list.append((url, func))  # 装饰器直接先初始化
        def inner():
            print("")
            func()
        return inner
    return wrapper

@route("/index.html")  # TODO route("/index.html"): url == /index.html, @wrapper
# @wrapper  本质：index=wrapper(index)
def index():

    line_data = ""  # 用来接收从数据库查询到的，以前端形式展现的数据部分

    # TODO 连接数据库，获取数据
    # 1、建立连接
    conn = pymysql.connect(host='192.168.41.50', port=3306, database='shoujinzhe', user='root', passwd='mysql', charset='utf8')
    print("已连接数据库...")

    # 2、取得游标
    cs1 = conn.cursor()

    # 3、查询
    sql = 'select * from hot limit 0,5'
    cs1.execute(sql)
    data_from_sql = cs1.fetchall()




    # 4、打开对应的页面
    with open("index1.html", encoding="utf-8") as f:  # TODO linux系统下可以不用写encoding
        content = f.read()

    # 5、将从数据库查询到的数据以前端形式组合起来
    for data in data_from_sql:
        # print(data)
        line_data += """
                        <li>
                            <div class="col-lg-3 col-md-3 cont-cont4-list1-pic">
                                <div>
                                    <img src="%s"/>
                                </div>
                            </div>
                            <div class="col-lg-8 col-md-8 col-lg-offset-1 col-md-offset-1 cont-cont4-list1-word">
                                    <h5><a href="#">%s</a></h5>
                                    <p style="">%s</p>
                                    <span style="">%s</span>
                            </div>
                        </li>
                    """ % (data[4], data[1], data[2], data[3])

    # 6、前端数据部分的内容替换
    content = re.sub(r'{%content%}', line_data, content)

    return content

@route("/center.html")
def center():

    line_data = ""  # 用来接收从数据库查询到的，以前端形式展现的数据部分

    # TODO 连接数据库，获取数据
    # 1、建立连接
    conn = pymysql.connect(host='192.168.41.50', port=3306, database='stock_db', user='root', passwd='mysql',
                           charset='utf8')
    print("已连接数据库...")

    # 2、取得游标
    cs1 = conn.cursor()

    # 3、查询
    sql = 'select info.code, info.short, info.chg, info.turnover, info.price, info.highs, focus.note_info' \
          ' from info inner join focus ON info.id = focus.info_id'
    cs1.execute(sql)
    data_from_sql = cs1.fetchall()

    # 4、打开对应的页面
    with open("center.html", encoding="utf-8") as f:  # TODO linux系统下可以不用写encoding
        content = f.read()

    # 5、前端内容部分组合
    for data in data_from_sql:
        line_data += """
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>
                                <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                            </td>
                            <td>
                                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300268">
                            </td>
                        </tr> 
                     """ % (data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    # 6、内容替换
    content = re.sub(r'{%content%}', line_data, content)

    return content

@route("/gettime.html")
def gettime():
    data_from_sql = "时间数据来自于数据库"

    # 打开对应的页面
    with open("../templates/gettime.html", encoding="utf-8") as f:  # TODO linux系统下可以不用写encoding
        content = f.read()

    # 内容替换
    content = re.sub(r'{%content%}', data_from_sql, content)

    return content

def error_pag():
    data_from_sql = "动态页面请求错误！<a href='index.html'>返回首页</a>"

    # 打开对应的页面
    with open("../templates/404.html", encoding="utf-8") as f:  # TODO linux系统下可以不用写encoding
        content = f.read()

    # 内容替换
    content = re.sub(r'{%content%}', data_from_sql, content)

    content = re.sub(r'<p>', "<p style='font-size: 200px'>", content)

    return content


def app(env):
    # 1. 解析字典，获取请求信息
    request_url = env["PATH_INFO"]
    print("请求路径:", request_url)

    # 2. 区别不同的请求，请求不同，返回的数据也不同
    # TODO 里面的数据由两部分组成(url,func)。 根据路由('/index.html',index)，由url进行映射，找到要调用的方法
    # 遍历路由列表
    for url, func in g_route_list:
        if url == request_url:
            return '200 OK', [('Content-Type', 'text/html;charset=utf-8')], func()
    else:
        return '404 Not Found', [('Content-Type', 'text/html;charset=utf-8')], error_pag()
