using System;
using System.Net;
using System.Reflection;
using System.Security.Cryptography.X509Certificates;
using System.Threading;
using Fiddler;
using Newtonsoft.Json;
using System.Runtime.InteropServices;
 


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
            X509Certificate2 oRootCert;
            if (null == CertMaker.GetRootCertificate())
            {
                CertMaker.createRootCert();
                oRootCert = CertMaker.GetRootCertificate();
                X509Store certStore = new X509Store(StoreName.Root, StoreLocation.LocalMachine);
                certStore.Open(OpenFlags.ReadWrite);
                try
                {
                    certStore.Add(oRootCert);
                }
                finally
                {
                    certStore.Close();
                }
            }
            else
            {
                oRootCert = CertMaker.GetRootCertificate();
            }


            FiddlerApplication.oDefaultClientCertificate = oRootCert;
            CONFIG.IgnoreServerCertErrors = true;
            CertMaker.trustRootCert();
            FiddlerApplication.Prefs.SetBoolPref("fiddler.network.streaming.abortifclientaborts", true);
            FiddlerApplication.AfterSessionComplete += session => getIDToken(session);
            FiddlerApplication.Startup(8001, FiddlerCoreStartupFlags.DecryptSSL|FiddlerCoreStartupFlags.AllowRemoteClients|FiddlerCoreStartupFlags.Default);
            Console.Write("开始捕获token，请通过学生端打开我在校园获得4天有效期的TOKEN。\n");
            Console.ReadLine();

            // Shutdown:
            FiddlerApplication.Shutdown();
        }

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