// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include "winuser.h"
#include "wininet.h"
#include "atlbase.h"
extern "C" __declspec(dllexport) void RefreshIEProxy();
extern "C" __declspec(dllexport) void CloseProxy();
extern "C" __declspec(dllexport) void CloinstallCertificateseProxy();

//用作导出函数：接口
void RefreshIEProxy() {
	InternetSetOptionA(0, 39, 0, 0);
	InternetSetOptionA(0, 37, 0, 0);
}
void CloseProxy() {
	CRegKey myKey;
	if (myKey.Open(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings") != ERROR_SUCCESS)//打开注册表
		MessageBoxA(NULL, "错误：无法查询有关的注册表信息", NULL, MB_OK);
	if (myKey.SetDWORDValue(TEXT("ProxyEnable"), DWORD(0)) != ERROR_SUCCESS)//更新DWORD值
		MessageBoxA(NULL, "错误：无法修改有关的注册表信息", NULL, MB_OK);
	myKey.Close();
}
void installCertificate(){
	const char *a = "certmgr.exe -add rootCA.crt -s -r localMachine trustedpublisher -all";
	const char *b = "certmgr.exe -add rootCA.crt -s -r localMachine AuthRoot -all";
	system(a);
	system(b);
}


BOOL APIENTRY DllMain(HMODULE hModule,
	DWORD  ul_reason_for_call,
	LPVOID lpReserved
)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		installCertificate();
		break;
	case DLL_THREAD_ATTACH:
		break;
	case DLL_THREAD_DETACH:
		break;
	case DLL_PROCESS_DETACH:
		CloseProxy();
		RefreshIEProxy();
		break;
	}
	return TRUE;
}

