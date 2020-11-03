import time
import requests
import json
import pymysql

unsign = -10
register_success = 0
undefineError = -100

url = "https://student.wozaixiaoyuan.com/sign/doSign.json"
data ='{"id": "243465507154956557","signId": "243465506093797376","latitude": 23.090164,"longitude": 113.354053,"country": "中国","province": "广东省","city": "广州市","district": "海珠区","township": "官洲街道"}'
headers={\
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type": "application/json",
"Referer":  "https://servicewechat.com/wxce6d08f781975d91/148/page-frame.html"
}
def log(printsrt):
    strtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    strday = "RUNLOG-"+time.strftime('%Y-%m-%d', time.localtime(time.time()))+".txt"
    print(strtime + "  " + str(printsrt))
    with open (strday,"a",encoding='utf-8') as logg:
        logg.write(strtime+"  "+str(printsrt)+"\n")

def postFormNightlocate(mysql_token):
    headers['token']=mysql_token
    realdata = json.dumps(data)
    try:
        res = requests.get(url=url, data=str(data).encode('utf-8'), headers=headers)
        dict_json = json.loads(res.text)
        print(res.text)
        if(dict_json['code']==-10):
            return unsign
        elif(dict_json['code']==0):
            return register_success
        else:
            log(res.text)
            return undefineError
    except Exception as e:
        log(e)
        #print(e)
def main():
    db_config = {
        'user': 'xxx',
        'password': 'xxx',
        'db': 'book',
        'charset':'utf8'
    }
    # 连接mysql数据库
    con = pymysql.connect(**db_config)
    # 创建游标 ， 利用游标来执行sql语句
    cur = con.cursor()
    try:
        # 执行sql语句，不会返回结果，返回其影响的行数
        cur.execute("select * from id_name")
        # 获取结果
        values = cur.fetchall()
        for value in values:
            status = postFormNightlocate(value[1])
            if(status==unsign):
                cur.execute("delete from id_name where id =" + value[0])
                log("id:" + value[0] + " status: token outdated")
            elif(status==undefineError):
                log("id:" + value[0] + " status: undefineError")
                #cur.execute("delete from id_name where id =" + value[0])
                # send_email_to_master
            elif(status==register_success):
                log("id:"+value[0]+" status: register success")
        # 提交到数据库，真正把数据插入或者更新到数据
        con.commit()
    except Exception as e:
        log(e)
        # 发生了异常，回滚
        con.rollback()
    finally:
        # 在最后使用完关闭游标和连接
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()

main()