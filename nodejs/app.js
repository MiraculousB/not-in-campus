'use strict';

let Ut = require("./common");
var nodeCmd = require('node-cmd');
var http = require('http');
var AnyProxy = require('anyproxy');
var ffi = require('ffi-napi'); // ����ffi-napi
var fs = require('fs');
const IEDll = new ffi.Library('ProxyHandle.dll', {
    'RefreshIEProxy': ['void ', []],
});

const exec = require('child_process').exec;

if (!AnyProxy.utils.certMgr.ifRootCAFileExists()) {
  AnyProxy.utils.certMgr.generateRootCA((error, keyPath) => {
    // let users to trust this CA before using proxy
    if (!error) {
      const certDir = require('path').dirname(keyPath);
      const isWin = /^win/.test(process.platform);
      fs.copyFile(`${certDir}\\rootCA.crt`,'./rootCA.crt',function(err){
        if(err) console.log('something wrong was happened')
        else console.log('copy rootCA succeed');
    })
    } else {
      console.error('error when generating rootCA', error);
    }
  });
}

nodeCmd.run('InstallAccess');

const options = {
    port: 8001,
    rule: require('./myRuleModule'),
    webInterface: {
        enable: true,
        webPort: 8002
    },
    throttle: 10000,
    forceProxyHttps: false,
    wsIntercept: false, // ������websocket����
    silent: true
};
AnyProxy.utils.systemProxyMgr.enableGlobalProxy('127.0.0.1', '8003');
IEDll.RefreshIEProxy();
const proxyServer = new AnyProxy.ProxyServer(options);
proxyServer.on('ready', () => { /* */ });
proxyServer.on('error', (e) => { /* */ });
proxyServer.start();

http.createServer(function(request, response) {
    response.writeHead(200, { 'Content-Type': 'text/plain' });
    response.end('Hello World');
    if (request.url.indexOf("getToken") >= 0) {
        (async () => {
            await Ut.sleep(4000);
            console.log("Token send success");
            await Ut.sleep(1000);
            AnyProxy.utils.systemProxyMgr.disableGlobalProxy();
            IEDll.RefreshIEProxy();
            process.exit();
           })()
    }
}).listen(8081);
console.log("Start catch token");
//AnyProxy.utils.systemProxyMgr.disableGlobalProxy();
