# e01e
### 1.前言

在这之前我接触到了另一个大哥的https://github.com/Lay0us1/Londly02，但是用的不太尽人意，然后去看了一下代码发现挺简单就是调用，于是自己也想自己搞搞

现在主要的流程就是：
	根域名流程：subfinder搞子域名 -> httpx处理，过滤302、404状态码 -> fanger指纹识别(可选) -> xray -> nuclei
	url列表流程： httpx处理，过滤302、404状态码 -> fanger指纹识别(可选) -> xray -> nuclei

待优化：加入路径爆破、代理池、fanger指纹添加和优化等操作，后续更新



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
  --not-xray            不使用xray
  --not-nuclei          不使用nuclei
  --not-xscan           不使用xscan
  --finger              启用Finger指纹识别
```

