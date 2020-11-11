# 我不在校园

## 概述  
我不在校园是由nodejs客户端，Javaee服务端，python服务端脚本，c++编写的动态链接库文件构成的自动签到系统。可以在客户端上传token后自动完成一日四检。客户端内置抓包模块，原理为中间人攻击。  

## 客户端工作流程  
第一次打开程序，首先会安装SSL证书并让本机添加信任，使得代理服务器能够解析HTTPS协议的流量。之后调用dll中已经封装好的方法，打开代理服务器并通知其他应用连接代理服务器。连接完成后，开始过滤封包直到获得home.json，获得并上传包头的token，关闭服务器，通知其他应用代理服务器已关闭。  

## 服务端工作流程  
获得客户端发来的ID与token后，插入到临时存放Token的数据库的临时表中，每天在四次签到前一分钟都会更新用户的数据，获取用户邮箱，晚点名接口等信息，插入或更新到主表中，脚本运行时间为每次签到开始的一分钟后。如果Token已过期会发邮件提醒用户更新。  

## 使用方法  
首先需要有一台windows系统的电脑，先打开程序，提示Start catch token后，再打开电脑版的微信小程序我在校园。注意需要从公众号聊天界面中点击学生端打开。从小程序面板中打开会获取不到。  
<img src="https://s3.ax1x.com/2020/11/11/Bv6qv8.png" alt="TIP" width="600" align="bottom" />  
成功上传时会显示{code:0}等内容。之后需要每隔4天完成一次上传。系统会自动完成一日四检。  

## 已知BUG  
部分电脑不能抓取https协议的封包，点开学生端后没有反应，仍然显示Start catch token。如果不能使用建议使用其他人电脑上传token。或后续等待更换抓包核心的新版本。  

## 部署教程  

### 客户端
首先需要在PC上安装nodejs12，python2.7，Visual studio 2017，myeclipse enterprise  
在nodejs文件夹中包含有myRuleModule.js，打开后找到以下代码，将url修改为你的对应的服务器IP。  
之后使用windows命令行全局安装nodejs模块nexe后，对客户端进行打包。
```javascript
*beforeSendResponse(requestDetail, responseDetail) {
  var url = '';
  if (requestDetail.url.indexOf('https://student.wozaixiaoyuan.com/login/index.json') === 0) {
    var http = require("http");
    console.log(responseDetail.response.body.toString());// consume response body
    var datatojson = JSON.parse(responseDetail.response.body.toString());
    var url = 'http://你的云服务器IP:8080/jsp_work/saveIDToken.jsp?'+'token='+datatojson.data.token+"&id="+datatojson.data.id;
    http.get(url, (res) => {
      res.resume();
    }).on('error', (e) => {
      console.log(`Got error: ${e.message}`);
    });
    http.get(`http://127.0.0.1:8081/getToken`, (res) => {
      res.resume();
    }).on('error', (e) => {
      console.log(`Got error: ${e.message}`);
    });
  }
  return null;
},
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
| id    | char(100) | NO   | PRI | NULL    |       |
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
<br>
##### autoCheck.py  
```python
def sendemail(receiver,content):
    sender = "xx@163.com"#发送方
    password = "口令"
```
注册163邮箱，打开stmp服务，获得口令与用户名并修改。
```python
data ='{"id": "243827894752446733","signId": "243827893926168576","latitude": 23.090164,"longitude": 113.354053,"country": "中国","province": "广东省","city": "广州市","district": "海珠区","township": "官洲街道"}'
```
将latitude与longitude修改为签到学校的经纬度，后面的城市信息也可以修改成对应的地点。

##### autopost.py
```python
def sendemail(receiver,content):
    sender = "xx@163.com"#发送方
    password = "口令"
```
注册163邮箱，打开stmp服务，获得口令与用户名并修改。
```python
data = "answers=%5B%220%22%5D&seq=xxxxx&temperature=36.5&userId=&latitude=23.090164&longitude=113.354053&country=%E4%B8%AD%E5%9B%BD&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&district=%E6%B5%B7%E7%8F%A0%E5%8C%BA&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&township=%E6%B1%9F%E6%B5%B7%E8%A1%97%E9%81%93&street=%E4%B8%8A%E5%86%B2%E4%B8%AD%E7%BA%A6%E6%96%B0%E8%A1%97%E4%B8%80%E5%B7%B7&myArea="
```
url编码转义，修改经纬度，省市即可。
