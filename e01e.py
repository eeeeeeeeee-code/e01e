# coding:utf-8
import os
import argparse
import subprocess
from yaml import safe_load
from package.file import remove_urls


def argss(args):
    try:
        dmain = str(args.domain)
        dmain_file = str(args.domain_file)
        url_file = args.url_file
        not_file = args.not_file
        functions = [Finder, nuclei, xary]

        if dmain not in "None":
            os.system("rm -fr ./result/sub.txt")
            subfinder(dmain, "None")
            return True
        elif dmain_file not in "None":
            os.system("rm -fr ./result/sub.txt")
            subfinder("None", dmain_file)
            return True
        elif url_file:
            httpx(str(url_file))
            if not_file:
                remove_urls("./result/not_file.txt", str(not_file))
            if not args.run_finger:
                functions.remove(Finder)
            for func in functions:
                func()
            return False
        else:
            if check_command("python3"):
                os.system("python3 e01e.py -h")
            elif check_command("python"):
                os.system("python e01e.py -h")
            else:
                print("没有python环境")
            exit()
    except Exception as e:
        print(e)


def check_command(command):
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def subfinder(domain, domain_file):
    try:
        if domain_file in "None":
            os.system(
                f'./tools/subfinder/subfinder -d {domain} -o ./result/sub.txt -t {str(config_yaml["subfinder"]["subfiner-threads"])}')
        else:
            os.system(
                f'./tools/subfinder/subfinder -dL {domain_file} -o ./result/sub.txt -t {str(config_yaml["subfinder"]["subfiner-threads"])}')
    except Exception as e:
        print("subfinder bug:", e)


def httpx(urlfile):
    try:
        if args.not_file:
            os.system(f"./tools/httpx/httpx -l ./result/sub.txt  -fc {str(config_yaml['httpx']['http-filter-code'])} -t {str(config_yaml['httpx']['httpx-threads'])} -rl {str(config_yaml['httpx']['httpx-limit'])} -o ./result/not_file.txt")
        elif args.url_file:
            os.system(f"./tools/httpx/httpx -l {urlfile} -fc {str(config_yaml['httpx']['http-filter-code'])} -t {str(config_yaml['httpx']['httpx-threads'])} -rl {str(config_yaml['httpx']['httpx-limit'])} -o ./result/url.txt")
        else:
            os.system(f"./tools/httpx/httpx -l ./result/sub.txt -fc {str(config_yaml['httpx']['http-filter-code'])} -t {str(config_yaml['httpx']['httpx-threads'])} -rl {str(config_yaml['httpx']['httpx-limit'])} -o ./result/url.txt")
    except Exception as e:
        print("tools_httpx bug:", e)


def xary():
    try:
        if not args.not_xray:
            os.system(
                f"./tools/xray/xray_linux_amd64 --config ./tools/xray/config.yaml webscan -url-file ./result/url.txt --html-output ./result/xray.html")
        else:
            print("\n" + "-" * 50 + "使用参数--not-xray,跳过xray检测" + "-" * 50)
    except Exception as e:
        print("xary bug:", e)


def nuclei():
    try:
        if not args.not_nuclei:
            os.system(
                f"./tools/nuclei/nuclei -l ./result/url.txt -severity {str(config_yaml['nuclei']['nuclei-severity'])} -stats -o ./result/nuclei.json -t {str(config_yaml['nuclei']['nuclei-threads'])}")
        else:
            print("\n" + "-" * 50 + "使用参数--not-nuclei,跳过nuclei检测" + "-" * 50)
    except Exception as e:
        print("nuclei bug:", e)


def Finder():
    try:
        if check_command("python3"):
            os.system(f"python3 ./tools/Finger/Finger.py -f ./result/url.txt -o xlsx")
        elif check_command("python"):
            os.system(f"python ./tools/Finger/Finger.py -f ./result/url.txt -o xlsx")
        else:
            print("没有python环境")
    except Exception as e:
        print("nuclei bug:", e)


# 初始化
def _main():
    global args, config_yaml
    config_yaml = safe_load(open("./config.yaml"))
    parser = argparse.ArgumentParser(description='File input')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--domain', dest='domain', nargs='?', type=str, help='单个根域名')
    group.add_argument('-df', '--domain-file', dest='domain_file', nargs='?', type=str, help='根域名列表文件')
    group.add_argument('-uf', '--url-file', dest='url_file', nargs='?', type=str, default=False,
                       help='指定url列表文件')
    parser.add_argument('-xf', '--not-url', dest='not_file', nargs='?', type=str, default=False,
                        help='指定拒绝不扫描的url列表文件')
    parser.add_argument('--not-xray', dest='not_xray', action='store_true', help='不使用xray')
    parser.add_argument('--not-nuclei', dest='not_nuclei', action='store_true', help='不使用nuclei')
    parser.add_argument('--finger', dest='run_finger', action='store_true', help='启用Finger指纹识别')
    args = parser.parse_args()

    functions = [Finder, nuclei, xary]
    if argss(args):
        httpx(None)
        if args.not_file:
            remove_urls("./result/not_file.txt", str(args.not_file))
        if not args.run_finger:
            functions.remove(Finder)
        for func in functions:
            func()


if __name__ == "__main__":
    _main()
