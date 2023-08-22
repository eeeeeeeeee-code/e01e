# coding:utf-8
import threading
from yaml import safe_load
from os import system


def ask_for_confirmation():
    try:
        answer = ""

        def input_thread():
            nonlocal answer
            answer = input(
                f"url列表文件行数超过{config_yaml['file']['file-long']},是否进行去重，20秒后自动选择去重(yes/no): ")

        input_thread = threading.Thread(target=input_thread)
        input_thread.start()
        input_thread.join(timeout=5)

        if answer not in "no":
            answer = "yes"
        return answer.lower()
    except Exception as e:
        print("package.file.ask_for_confirmation bug:" + str(e))


def de_weight(url_bool):
    try:
        if url_bool:
            system(f"./tools/httpx/httpx -l {str(url_bool)} -sc -title -cl -wc -td | tee ./result/http.txt")
            system("awk '!a[$2,$3,$4,$5]++' ./result/http.txt > ./result/http2.txt")
            system("awk '{print $1}' ./result/http2.txt > ./result/url.txt")
            system("rm -fr ./result/http2.txt ./result/http.txt")
        else:
            system("./tools/httpx/httpx -l ./result/url.txt -sc -title -cl -wc -td | tee ./result/http.txt")
            system("awk '!a[$2,$3,$4,$5]++' ./result/http.txt > ./result/http2.txt")
            system("awk '{print $1}' ./result/http2.txt > ./result/url.txt")
            system("rm -fr ./result/http2.txt ./result/http.txt")
    except Exception as e:
        print("package.file.de_weight() bug:" + str(e))


def de_run(url_bool):
    global config_yaml
    config_yaml = safe_load(open("./config.yaml"))
    # 判断文件长度是否超标
    if int(config_yaml['file']['file-long']) <= len(open(r"./result/url.txt", 'r').readlines()):
        answer = ask_for_confirmation()
        if answer in "":
            print("\n无响应，自动进行去重，去重前行数"+str(len(open(r"./result/url.txt", 'r').readlines())))
            de_weight(url_bool)
            print("-"*25+"去重后行数"+str(len(open(r"./result/url.txt", 'r').readlines()))+"-"*25)
        elif answer in "no":
            print("长度不够取消去重操作")
        else:
            print("好的，进行去重中，去重前行数"+str(len(open(r"./result/url.txt", 'r').readlines())))
            de_weight(url_bool)
            print("-"*25+"去重后行数"+str(len(open(r"./result/url.txt", 'r').readlines()))+"-"*25)
