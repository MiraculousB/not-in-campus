# 我不在校园

## 介绍  
我不在校园是由nodejs客户端，Javaee服务端，python服务端脚本，c++编写的动态链接库文件构成的自动签到系统。可以在客户端上传token后自动完成一日四检。客户端内置抓包模块，原理为中间人攻击。  

## 客户端工作流程  
第一次打开程序，首先会安装SSL证书并让本机添加信任，使得代理服务器能够解析HTTPS协议的流量。之后调用dll中已经封装好的方法，打开代理服务器并通知其他应用连接代理服务器。连接完成后，开始过滤封包直到获得home.json，获得并上传包头的token，关闭服务器，通知其他应用代理服务器已关闭。  

## 服务端工作流程  
获得客户端发来的ID与token后，插入到临时存放Token的数据库的临时表中，每天在四次签到前一分钟都会更新用户的数据，获取用户邮箱，晚点名接口等信息，插入或更新到主表中，脚本运行时间为每次签到开始的一分钟后。如果Token已过期会发邮件提醒用户更新。  

## 使用方法  
首先需要有一台windows系统的电脑，先打开程序，提示Start catch token后，再打开电脑版的微信小程序我在校园。注意需要从公众号聊天界面中点击学生端打开。从小程序面板中打开会获取不到。  
<a href="#">
<img src="https://raw.githubusercontent.com/MiraculousB/not-in-campus/master/photo/1.png" alt="TIP" width="600" align="bottom" />  
</a>
成功上传时会显示{code:0}等内容。之后需要每隔4天完成一次上传。系统会自动完成一日四检。  


## 已知BUG  
部分电脑不能抓取https协议的封包，点开学生端后没有反应，仍然显示Start catch token。如果不能使用建议使用其他人电脑上传token。或后续等待更换抓包核心的新版本。  

## 项目源码  
https://github.com/MiraculousB/not-in-campus  

## 客户端运行环境  
nodejs12，python2.7  

## 客户端IDE  
Vscode，Visual studio 2017，myeclipse enterprise  

## 服务端运行环境  
Tomcat8，mysql，python3  
