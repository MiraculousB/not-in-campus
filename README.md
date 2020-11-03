# not-in-campus

介绍
我不在校园是由nodejs客户端，Javaee服务端，python服务端脚本，c++编写的动态链接库文件构成的自动签到系统。客户端内置抓包模块，原理为中间人攻击。

工作流程
第一次打开程序，首先会安装SSL证书并让本机添加信任，使得代理服务器能够解析HTTPS协议的流量。之后调用dll中已经封装好的方法，打开代理服务器并通知其他应用连接代理服务器。连接完成后，开始过滤封包直到获得home.json，获得并上传包头的token，结束服务器，通知其他应用代理服务器已关闭。

使用方法
首先需要有一台windows系统的电脑，检查端口8001是否已经被占用，在cmd中输入netstat -an -o
确实没有被使用后，先打开程序，提示Start catch token后，再打开电脑版的微信小程序我在校园。成功上传时会显示{code:0}等内容。之后需要每隔4天完成一次上传。系统会自动完成一日四检。

客户端运行环境
nodejs12，python2.7

客户端IDE
Vscode，Visual studio 2017，myeclipse enterprise

服务端运行环境
Tomcat8，mysql
