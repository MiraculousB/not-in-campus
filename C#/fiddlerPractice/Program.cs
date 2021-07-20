using System;
using System.Net;
using System.Reflection;
using System.Security.Cryptography.X509Certificates;
using System.Threading;
using Fiddler;
using Newtonsoft.Json;
using System.Runtime.InteropServices;
using System.Diagnostics;

namespace Demo
{
    class Program
    {
        public delegate bool ControlCtrlDelegate(int CtrlType);
        [DllImport("kernel32.dll")]
        private static extern bool SetConsoleCtrlHandler(ControlCtrlDelegate HandlerRoutine, bool Add);
        private static ControlCtrlDelegate cancelHandler = new ControlCtrlDelegate(HandlerRoutine);

        public static bool HandlerRoutine(int CtrlType)
        {
            switch (CtrlType)
            {
                case 0:
                    FiddlerApplication.Shutdown(); //Ctrl+C关闭  
                    break;
                case 2:
                    FiddlerApplication.Shutdown(); //按控制台关闭按钮关闭  
                    break;
            }
            Console.ReadLine();
            return false;
        }

        static void Main(string[] args)
        {
            SetConsoleCtrlHandler(cancelHandler, true);
            //-----------处理证书-----------
            //伪造的证书
            X509Certificate2 oRootCert;
            //如果没有伪造过证书并把伪造的证书加入本机证书库中
            if (null == CertMaker.GetRootCertificate())
            {
                //创建伪造证书
                CertMaker.createRootCert();

                //重新获取
                oRootCert = CertMaker.GetRootCertificate();

                //打开本地证书库
                X509Store certStore = new X509Store(StoreName.Root, StoreLocation.LocalMachine);
                certStore.Open(OpenFlags.ReadWrite);
                try
                {
                    //将伪造的证书加入到本地的证书库
                    certStore.Add(oRootCert);
                }
                finally
                {
                    certStore.Close();
                }
            }
            else
            {
                //以前伪造过证书，并且本地证书库中保存过伪造的证书
                oRootCert = CertMaker.GetRootCertificate();
            }

            //-----------------------------

            //指定伪造证书
            FiddlerApplication.oDefaultClientCertificate = oRootCert;
            //忽略服务器证书错误
            CONFIG.IgnoreServerCertErrors = true;
            //信任证书
            CertMaker.trustRootCert();
            //看字面意思知道是啥，但实际起到啥作用。。。鬼才知道，官方例程里有这句，加上吧，管它呢。
            FiddlerApplication.Prefs.SetBoolPref("fiddler.network.streaming.abortifclientaborts", true);
            // Attach to events of interest:
            FiddlerApplication.AfterSessionComplete += session => getIDToken(session);
            // Start:
            FiddlerApplication.Startup(8001, FiddlerCoreStartupFlags.DecryptSSL|FiddlerCoreStartupFlags.AllowRemoteClients|FiddlerCoreStartupFlags.Default);
            Console.Write("开始捕获token，请打开小程序日检日报页面获取三天有效期token\n"+ @"项目地址：https://github.com/MiraculousB/not-in-campus"+"\n");
            Console.ReadLine();

            // Shutdown:
            FiddlerApplication.Shutdown();
        }

        private static void getIDToken(Session session)
        {
            String a = "getTodayHeatList.json";
            if (session.fullUrl.IndexOf(a)>=0)
            {

                String token = session.RequestHeaders.AllValues("token");
                Console.WriteLine(token);
                String id = "114514";
                String url = @"http://你的IP:8080/jsp_work/saveIDToken.jsp?id="+id+@"&token="+token;
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                if(response.StatusCode.ToString()=="OK")
                {
                    Console.WriteLine("上传Token成功");
                    FiddlerApplication.Shutdown();
                    Thread.Sleep(2000);
                    Process.GetCurrentProcess().Kill();
                }
            }
        }
        public class Status
        {
            public int code { get; set; }
            public data data { get; set; }
        }
        /// <summary>
        /// 学生班级实体
        /// </summary>
        public class data
        {
            public int status { get; set; }
            public string id { get; set; }
            public string token { get; set; }
        }

    }
}