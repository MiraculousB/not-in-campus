import time
import requests
import json
import pymysql
import smtplib #smtp服务器
from email.mime.text import MIMEText #邮件文本
import urllib.parse
import datetime

unsign = -10
register_success = 0
undefineError = -100
notintime = -999
alreadyCheck = -9999
noCheck = -99999

url = "https://student.wozaixiaoyuan.com/sign/doSign.json"
url_locate = "https://student.wozaixiaoyuan.com/sign/getSignMessage.json"
data ='{"id": "243827894752446733","signId": "243827893926168576","latitude": 23.090164,"longitude": 113.354053,"country": "中国","province": "广东省","city": "广州市","district": "海珠区","township": "官洲街道"}'
listdata = "page=1&size=5"
headers={\
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type": "application/json",
"Referer":  "https://servicewechat.com/wxce6d08f781975d91/148/page-frame.html",
"accept-encoding":"gzip, deflate, br"
}
headers_locate={\
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type":	"application/x-www-form-urlencoded",
"Referer":  "https://servicewechat.com/wxce6d08f781975d91/148/page-frame.html",
"accept-encoding":"gzip, deflate, br",
"content-length":"13"
}
def sendemail(receiver,content):
    subject = "我不在校园"#邮件标题
    sender = "xx@163.com"#发送方
    recver = receiver #接收方
    password = "xx"
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
        logg.write("[autoCheckv2]: "+strtime+"  "+str(printsrt)+"\n")

def postFormNightlocate(mysql_token):
    try:
        headers['token']=mysql_token
        headers_locate['token']=mysql_token
        res = requests.post(url=url_locate,data=listdata,headers=headers_locate)
        dict_json = json.loads(res.text)
        if(dict_json['code']==-10):
            return unsign
        if(len(dict_json['data'])==0):
            return noCheck
        starttime = dict_json['data'][0]['start']
        endtime = dict_json['data'][0]['end']
        atype = dict_json['data'][0]['type']
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M') 
        timeArray_starttime = time.strptime(starttime, "%Y-%m-%d %H:%M")
        timeArray_endtime = time.strptime(endtime, "%Y-%m-%d %H:%M")
        timeArray_nowtime = time.strptime(nowtime, "%Y-%m-%d %H:%M")
        timeStamp_starttime = int(time.mktime(timeArray_starttime))
        timeStamp_endtime = int(time.mktime(timeArray_endtime))
        timeStamp_nowtime = int(time.mktime(timeArray_nowtime))
        id= dict_json["data"][0]["logId"]
        signid= dict_json["data"][0]["id"]
        #print(id,signid)
        realdata = data.replace("243827894752446733",id)
        realdata = realdata.replace("243827893926168576",signid)
        realdata = str(realdata).encode('utf-8')
        if not (timeStamp_starttime<timeStamp_nowtime and timeStamp_nowtime<timeStamp_endtime):
            return notintime
        if(str(atype)=='1'):
            return alreadyCheck
    except Exception as e:
        log(e)
    try:
        res = requests.get(url=url, data=realdata, headers=headers)
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
def main():
    db_config = {
        'user': 'user',
        'password': '123456',
        'db': 'book',
        'charset':'utf8'
    }
    # 连接mysql数据库
    con = pymysql.connect(**db_config)
    # 创建游标 ， 利用游标来执行sql语句
    cur = con.cursor()
    try:
        # 执行sql语句，不会返回结果，返回其影响的行数
        cur.execute("select sno,token,email,sendemail from stu_info")
        # 获取结果
        values = cur.fetchall()
        for value in values:
            status = postFormNightlocate(value[1])
            if(status==unsign):
                if(value[3]=='1'):
                    log("id:" + value[0] + " status: sendemail succeed")
                    sendemail(value[2],r"Token信息已过期，请及时更新。最新版本的客户端在ftp://172.27.183.4/下载，需要连接校园网。")
                    cur.execute("update stu_info set sendemail="+"'"+"0"+"'"+"where sno="+"'"+value[0]+"'")
            elif(status==noCheck):
                #log("id:" + value[0] + " status: noCheck")
                pass
            elif(status==alreadyCheck):
                #log("id:" + value[0] + " status: alreadyCheck")
                pass
            elif(status==notintime):
                #log("id:" + value[0] + " status: notintime")
                pass
            elif(status==undefineError):
                log("id:" + value[0] + " status: undefineError")
                sendemail("xx@qq.com",str(value[0])+"出现未知错误")
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
