# 我不在校园

## 概述  
我不在校园是由 C#客户端，Javaee服务端，python服务端脚本，构成的自动签到系统。可以在客户端上传token后自动完成日检日报和签到。客户端内置抓包模块，原理为中间人攻击。  

## 客户端工作流程  
第一次打开程序，首先会安装SSL证书并让本机添加信任，使得代理服务器能够解析HTTPS协议的流量。之后调用FiddlerCore4.dll中已经封装好的方法，打开代理服务器并通知其他应用连接代理服务器。连接完成后，开始过滤封包直到获得home.json，获得并上传包头的token，关闭服务器，通知其他应用代理服务器已关闭。  

## 服务端工作流程  
获得客户端发来的ID与token后，插入到临时存放Token的数据库的临时表中，每5分钟将用户的临时表中的token，更新到主表中。每半小时运行一次签到脚本。如果Token已过期会发邮件提醒用户更新。  

## 使用方法  
首先需要有一台windows系统的电脑，先打开程序后，再打开电脑版的微信小程序我在校园。点击主界面的‘日检日报’模块。
<img src="https://s3.ax1x.com/2020/11/11/Bv6qv8.png" alt="TIP" width="600" align="bottom" />  
成功上传时会显示上传成功等内容。之后需要每隔4天完成一次上传。系统会自动完成日检日报模块的打卡。  

## 已知BUG  
强制关闭C#客户端会导致不能联网，原因是软件关闭时不能自动关闭系统代理，重启软件，正常退出即可  
windows defender会对C#客户端报毒，换成火绒或者其他杀毒软件即可  
2021/3/18:签到模块不能自动打卡了，因为没账号，有机会再修。估计是传的json数据变化了  
2021/7/13:我在校园小程序更新了，不过可以通过小程序主界面点击‘我的’，回到旧版。不影响获取token

## 项目源码
https://github.com/MiraculousB/not-in-campus

## 部署教程  

### 客户端
首先需要在PC上安装.net Framework 4.0，Visual studio 2017，myeclipse enterprise  
在C#文件夹中包含有program.cs，打开后找到以下代码，将url修改为你的对应的服务器IP。  
```C++
private static void getIDToken(Session session)
{
    String a = "index.json";
    if (session.fullUrl.IndexOf(a)>=0)
    {
        Console.WriteLine(session.GetResponseBodyAsString());
        Status body = JsonConvert.DeserializeObject<Status>(session.GetResponseBodyAsString());
        String id = body.data.id;
        String token = body.data.token;
        String url = @"http://你的IP:8080/jsp_work/saveIDToken.jsp?id="+id+@"&token="+token;
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
        if(response.StatusCode.ToString()=="OK")
        {
            Console.WriteLine("上传Token成功");
            FiddlerApplication.Shutdown();

        }
    }
}
```
打开MyEclipse，导入JAVAEE包，找到webroot文件夹中的saveIDToken.jsp。修改以下代码为服务器mysql新增用户的用户名和密码。
```java
String user = "xxx";
String password = "xxx";
```
修改完毕后倒出war包，在export界面搜索war即刻找到。获得war包后，将其放入服务端/var/lib/tomcat8/webapps/  
重启tomcat8服务即刻完成javaee项目部署。


### 服务端
首先需要在服务器上安装Tomcat8，mysql，python3。
#### Mysql  
创建一个新的用户，并授予所有权限。用户名与密码需要与JAVAEE一致  
创建数据库book，创建表id_name与stu_info。  
```
+-------+-----------+------+-----+---------+-------+
| Field | Type      | Null | Key | Default | Extra |
+-------+-----------+------+-----+---------+-------+
| id    | char(100) | NO   |     | NULL    |       |
| token | char(100) | NO   |     | NULL    |       |
+-------+-----------+------+-----+---------+-------+
```
```
+-----------+--------------+------+-----+---------+-------+
| Field     | Type         | Null | Key | Default | Extra |
+-----------+--------------+------+-----+---------+-------+
| sno       | varchar(100) | NO   | PRI | NULL    |       |
| email     | varchar(100) | NO   |     | NULL    |       |
| phone     | varchar(100) | NO   |     | NULL    |       |
| name      | varchar(100) | NO   |     | NULL    |       |
| token     | varchar(100) | NO   |     | NULL    |       |
| sendemail | varchar(20)  | NO   |     | 1       |       |
+-----------+--------------+------+-----+---------+-------+
```
#### Tomcat8
服务端需要有JDBC驱动，具体百度搜索JDBC LINUX TOMCAT8
#### Python3  
```
db_config = {
    'user': 'user',
    'password': '123456',
    'db': 'book',
    'charset':'utf8'
}
#修改每个py脚本中的db_config。
```

```python
#autoCheck.py
def sendemail(receiver,content):
    sender = "xx@163.com"#发送方
    password = "口令"
```
注册163邮箱，打开stmp服务，获得口令与用户名并修改。
```python
#autoCheck.py
data ='{"id": "243827894752446733","signId": "243827893926168576","latitude": 23.090164,"longitude": 113.354053,"country": "中国","province": "广东省","city": "广州市","district": "海珠区","township": "官洲街道"}'
```
将latitude与longitude修改为签到学校的经纬度，后面的城市信息也可以修改成对应的地点。

```python
#autopost.py
def sendemail(receiver,content):
    sender = "xx@163.com"#发送方
    password = "口令"
```
注册163邮箱，打开stmp服务，获得口令与用户名并修改。
```python
#autopost.py
data = "answers=%5B%220%22%5D&seq=xxxxx&temperature=36.5&userId=&latitude=23.090164&longitude=113.354053&country=%E4%B8%AD%E5%9B%BD&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&district=%E6%B5%B7%E7%8F%A0%E5%8C%BA&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&township=%E6%B1%9F%E6%B5%B7%E8%A1%97%E9%81%93&street=%E4%B8%8A%E5%86%B2%E4%B8%AD%E7%BA%A6%E6%96%B0%E8%A1%97%E4%B8%80%E5%B7%B7&myArea="
```
url编码转义，修改经纬度，省市即可。
#### 定时启动脚本
服务端输入`crontab -e`,在最后加上以下代码，需要修改为自己脚本的对应路径。
```
1 * * * * python3 /home/autopost/autoEnroll.py
31 * * * * python3 /home/autopost/autoEnroll.py
6 * * * * python3 /home/autopost/autoCheckv2.py
36 * * * * python3 /home/autopost/autoCheckv2.py
*/5 * * * * python3 /home/autopost/getInfo.py
```
