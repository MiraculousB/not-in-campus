import time
import requests
import json
import pymysql

unsign = -10
register_success = 0
undefineError = -100

url = "https://student.wozaixiaoyuan.com/my/getStudentSecretInfo.json"
headers={\
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type": "application/json",
"Referer":  "https://servicewechat.com/wxce6d08f781975d91/148/page-frame.html",
"token" : "576209d1-c240-44e4-b548-2ca7186acbf7"
}
def log(printsrt):
    strtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    strday = "RUNLOG-"+time.strftime('%Y-%m-%d', time.localtime(time.time()))+".txt"
    print(strtime + "  " + str(printsrt))
    with open (strday,"a",encoding='utf-8') as logg:
        logg.write(strtime+"  "+str(printsrt)+"\n")

def postFormNightlocate(mysql_token):
    headers['token']=mysql_token
    try:
        res = requests.get(url=url, headers=headers)
        info_dict = json.loads(res.text)
        return info_dict
    except Exception as e:
        log(e)
        #print(e)

def main():
    db_config = {
        'user': 'user',
        'password': '123456',
        'db': 'book',
        'charset':'utf8'
    }
    info_config = {
        'user': 'user',
        'password': '123456',
        'db': 'book',
        'charset':'utf8'
    }
    # 连接mysql数据库
    con = pymysql.connect(**db_config)
    # 创建游标 ， 利用游标来执行sql语句
    cur = con.cursor()
    # 连接mysql数据库
    con_info = pymysql.connect(**info_config)
    # 创建游标 ， 利用游标来执行sql语句
    cur_info = con_info.cursor()
    tmpcur = con_info.cursor()
    try:
        # 执行sql语句，不会返回结果，返回其影响的行数
        cur.execute("select * from id_name")
        # 获取结果
        values = cur.fetchall()
        for value in values:
            info_dict = postFormNightlocate(value[1])
            print(info_dict["data"]["number"], info_dict["data"]["email"], info_dict["data"]["name"],
                  info_dict["data"]["phone"],value[1])
            tmpcur.execute("select * from stu_info where sno ="+"'"+info_dict["data"]["number"]+"'")
            res = tmpcur.fetchall()
            if(len(res)):
                cur_info.execute("update stu_info set token="+"'"+value[1]+"'"+"where sno="+"'"+info_dict["data"]["number"]+"'")
                cur.execute("delete from id_name where id =" + value[0])
            else:
                query = 'insert into stu_info(sno, email, name, phone, token) values(%s, %s, %s, %s, %s)'
                sno = info_dict["data"]["number"]
                email = info_dict["data"]["email"]
                name = info_dict["data"]["name"]
                phone =  info_dict["data"]["phone"]
                token = value[1]
                values = (sno, email, name, phone, token)
                cur_info.execute(query, values)
                cur.execute("delete from id_name where id =" + value[0])
        # 提交到数据库，真正把数据插入或者更新到数据
        con.commit()
        con_info.commit()
    except Exception as e:
        log(e)
        # 发生了异常，回滚
        con.rollback()
        con_info.rollback()
    finally:
        # 在最后使用完关闭游标和连接
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        # 关闭游标
        cur_info.close()
        # 关闭连接
        cur_info.close()




main()
# res = requests.get(url=url, headers=headers)
# info_dict = json.loads(res.text)
# print(info_dict["data"]["number"],info_dict["data"]["email"],info_dict["data"]["name"],info_dict["data"]["phone"])

