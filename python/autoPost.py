import time
import requests
import json
import pymysql
import smtplib #smtp服务器
from email.mime.text import MIMEText #邮件文本
 


unsign = -10
register_success = 0
undefineError = -100
url = "https://student.wozaixiaoyuan.com/heat/save.json"
data = "answers=%5B%220%22%5D&seq=xxxxx&temperature=36.5&userId=&latitude=23.090164&longitude=113.354053&country=%E4%B8%AD%E5%9B%BD&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&district=%E6%B5%B7%E7%8F%A0%E5%8C%BA&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&township=%E6%B1%9F%E6%B5%B7%E8%A1%97%E9%81%93&street=%E4%B8%8A%E5%86%B2%E4%B8%AD%E7%BA%A6%E6%96%B0%E8%A1%97%E4%B8%80%E5%B7%B7&myArea="
headers={\
"content-length": "360",
"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type": "application/x-www-form-urlencoded",
"token":"6e4cb95e-19a0-4c78-82b4-0e67a5269b73",
"referer": "https://servicewechat.com/wxce6d08f781975d91/148/page-frame.html",
"accept-encoding": "gzip, deflate, br"
}


#邮件构建
def sendemail(receiver,content):
    subject = "我不在校园"#邮件标题
    sender = "13144266321@163.com"#发送方
    recver = receiver #接收方
    password = "CTHECSKYCMLUJRMK"
    message = MIMEText(content,"plain","utf-8")
    #content 发送内容     "plain"文本格式   utf-8 编码格式
    message['Subject'] = subject #邮件标题
    message['To'] = recver #收件人
    message['From'] = sender #发件人
    smtp = smtplib.SMTP_SSL("smtp.163.com",994) #实例化smtp服务器
    smtp.login(sender,password)#发件人登录
    smtp.sendmail(sender,[recver],message.as_string()) #as_string 对 message 的消息进行了封装
    smtp.close()

def log(printsrt):
    strtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    strday = "RUNLOG-"+time.strftime('%Y-%m-%d', time.localtime(time.time()))+".txt"
    print(strtime + "  " + str(printsrt))
    with open ("/home/autopost/"+strday,"a",encoding='utf-8') as logg:
        logg.write(strtime+"  "+str(printsrt)+"\n")

def getnowtime():
    strtime = time.strftime('%H', time.localtime(time.time()))
    strtime = int(strtime)
    if(strtime<=10):
        return "1"
    if(strtime>=11 and strtime<=15):
        return "2"
    if(strtime>=17 and strtime<=21):
        return "3"

def main():
    db_config = {
        'user': 'user',
        'password': '123456',
        'db': 'book',
        'charset':'utf8'
    }
    curseq = getnowtime()
    # 连接mysql数据库
    con = pymysql.connect(**db_config)
    # 创建游标 ， 利用游标来执行sql语句
    cur = con.cursor()
    try:
        # 执行sql语句，不会返回结果，返回其影响的行数
        cur.execute("select sno,token,email from stu_info")
        # 获取结果
        values = cur.fetchall()
        for value in values:
            status = postFormRegister(value[1],curseq)
            if(status==unsign):
                log("id:" + value[0] + " status: token outdated")
                sendemail(value[2],"Token信息已过期，请及时更新")
            elif(status==undefineError):
                sendemail("45567119@qq.com",str(value[0])+"出现未知错误")
                log("id:" + value[0] + " status: undefineError")
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

def postFormRegister(mysql_token,ctime):
    headers['token']=mysql_token
    realdata = data.replace("seq=xxxxx","seq="+ctime)
    try:
        res = requests.post(url=url, data=realdata, headers=headers)
        dict_json = json.loads(res.text)
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

def postFormNightlocate(mysql_token):
    headers['token']=mysql_token


#res = requests.post(url=url,data=data,headers=headers)
#print(res.text)
#postFormRegister("3c7d5fab-a736-4f1c-9886-1f63c9a85db8","2")
#conn_mysql()
main()
