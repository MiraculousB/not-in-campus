// ConsoleApplication3.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "wininet.h"
#include "atlbase.h"
int main()
{


	const char *a = "certmgr.exe -add rootCA.crt -s -r localMachine trustedpublisher -all";
	const char *b = "certmgr.exe -add rootCA.crt -s -r localMachine AuthRoot -all";
	//const char *c = "certmgr.exe -del -c -n rootCA.crt -s my";
	//system(c);
	system(a);
	system(b);
	//system("certmgr.exe /v /s my");
	//system("pause");



	//CRegKey myKey;
	//if (myKey.Open(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings") != ERROR_SUCCESS)//打开注册表
	//	MessageBoxA(NULL, "错误：无法查询有关的注册表信息", NULL, MB_OK);
	//if (myKey.SetDWORDValue(TEXT("ProxyEnable"), DWORD(0)) != ERROR_SUCCESS)//更新DWORD值
	//	MessageBoxA(NULL, "错误：无法修改有关的注册表信息", NULL, MB_OK);
	//myKey.Close();
}
	//HKEY key;
	//auto ret = RegOpenKeyEx(HKEY_CURRENT_USER, R"(Software\Microsoft\Windows\CurrentVersion\Internet Settings)", 0, KEY_ALL_ACCESS, &key);
	//if (ret != ERROR_SUCCESS) {
	//	std::cout << "open failed: " << ret << std::endl;
	//	return -1;
	//}

	//DWORD values_count, max_value_name_len, max_value_len;
	//ret = RegQueryInfoKey(key, NULL, NULL, NULL, NULL, NULL, NULL,
	//	&values_count, &max_value_name_len, &max_value_len, NULL, NULL);
	//if (ret != ERROR_SUCCESS) {
	//	std::cout << "query failed" << std::endl;
	//	return -1;
	//}

	//std::vector<std::tuple<std::shared_ptr<char>, DWORD, std::shared_ptr<BYTE>>> values;
	//for (int i = 0; i < values_count; i++) {
	//	std::shared_ptr<char> value_name(new char[max_value_name_len + 1],
	//		std::default_delete<char[]>());
	//	DWORD value_name_len = max_value_name_len + 1;
	//	DWORD value_type, value_len;
	//	RegEnumValue(key, i, value_name.get(), &value_name_len, NULL, &value_type, NULL, &value_len);
	//	std::shared_ptr<BYTE> value(new BYTE[value_len],
	//		std::default_delete<BYTE[]>());
	//	value_name_len = max_value_name_len + 1;
	//	RegEnumValue(key, i, value_name.get(), &value_name_len, NULL, &value_type, value.get(), &value_len);
	//	values.push_back(std::make_tuple(value_name, value_type, value));
	//}

	//DWORD ProxyEnable = 0;
	//for (auto x : values) {
	//	if (strcmp(std::get<0>(x).get(), "ProxyEnable") == 0) {
	//		ProxyEnable = *(DWORD*)(std::get<2>(x).get());
	//	}
	//}

	//if (ProxyEnable) {
	//	for (auto x : values) {
	//		if (strcmp(std::get<0>(x).get(), "ProxyServer") == 0) {
	//			std::cout << "ProxyServer: " << (char*)(std::get<2>(x).get()) << std::endl;
	//		}
	//	}
	//}
	//else {
	//	std::cout << "Proxy not Enabled" << std::endl;
	//}

