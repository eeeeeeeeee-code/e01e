# e01e

### 1.前言

在这之前我接触到了另一个大哥的https://github.com/Lay0us1/Londly02，但是用的不太尽人意，然后去看了一下代码发现挺简单就是调用，于是自己也想自己搞搞

现在主要的流程就是：

- 根域名流程：subfinder搞子域名 -> httpx处理，过滤302、404状态码 -> fanger指纹识别(可选) -> xray -> nuclei
- ​	url列表流程： httpx处理，过滤302、404状态码 -> fanger指纹识别(可选) -> xray -> nuclei

这里选择subfinder，看重它速度比较快，然后可以设置多个key、毕竟很多免费key都有限制，这样就比较好，对了，别忘了添加subfinder的key哦，运行一次后就在key位置就在$HOME/.config/subfinder/provider-config.yaml了，可以去参考https://github.com/projectdiscovery/subfinder，或者网上找个文章



**待优化：加入路径爆破、代理池、fanger指纹添加和优化等操作，后续更新**

已优化：1.加入拒绝扫描的url列表，支持使用*，但是不要加https://或者http://

​				2.加入config.yaml，来控制速率之类的操作

​				3.对于超过行数限制的url列表，可以选择进行去重处理，20秒没有回答会自动去重，去重对比的是状态码、大小、标题、简单的指纹，行数限制在config.yaml设置

### 2.使用方法

```
环境：
	暂时只支持linux
	python版本3.7~3.9

下载后使用：
	chmod +x run.sh
	./run.sh
```

帮助信息

```
optional arguments:
  -h, --help            show this help message and exit
  -d [DOMAIN], --domain [DOMAIN]
                        单个根域名
  -df [DOMAIN_FILE], --domain-file [DOMAIN_FILE]
                        根域名列表文件
  -uf [URL_FILE], --url-file [URL_FILE]
                        指定url列表文件
  -xf [NOT_FILE], --not-url [NOT_FILE]
                        指定拒绝不扫描的url列表文件
  --not-xray            不使用xray
  --not-nuclei          不使用nuclei
  --finger              启用Finger指纹识别

```

```
正常使用：扫描根域名列表
	python3 e01e.py -df do.txt
不使用xray：
	python3 e01e.py -df do.txt --f --not-xray
```

```
使用注意：
	-xf指定拒绝扫描url列表，举例：
		*.cont.test.com
		1.1.*.test.com
		test.com
	支持*，但是不要加https://或者http://
```



### 3.免责声明

该项目仅供授权下使用，禁止使用该项目进行违法操作，否则自行承担后果，请各位遵守《中华人民共和国网络安全法》！

