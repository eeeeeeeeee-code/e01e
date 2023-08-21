# coding:utf-8
import re


def remove_urls(url_list_file, exclude_list_file):
    # 读取url列表文件
    with open(url_list_file, 'r') as f:
        url_list = f.readlines()
    url_list = [url.strip() for url in url_list]

    # 读取不扫描的url列表文件
    with open(exclude_list_file, 'r') as f:
        exclude_list = f.readlines()
    exclude_list = [exclude.strip() for exclude in exclude_list]

    # 使用正则表达式匹配规则，将不扫描的url从url列表中去除
    filtered_urls = []
    for url in url_list:
        match = False
        for exclude in exclude_list:
            pattern = exclude.replace('.', r'\.').replace('*', r'.*')
            if re.search(r'^(https?://)?{}$'.format(pattern), url):
                match = True
                break
        if match:
            continue
        filtered_urls.append(url)

    # 将过滤后的url写入新的文件
    with open('./result/url.txt', 'w') as f:
        f.write('\n'.join(filtered_urls))

    print("已成功过滤URL并保存到./result/url.txt文件中。")
