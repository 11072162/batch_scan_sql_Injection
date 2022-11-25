#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os
import json
from urllib.parse import urlparse
from datetime import date
import shutil
import platform
today = date.today()

import sys
import getopt

def site():
    param = None
    url_list = []
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "u:r:p:vh",
                                   ["url=","file=","param=","version","help"])
    except:
        print("Parameter format error"+'\n')
        return False
    for opt, arg in opts:
        if opt in ['-u', '--url']:
            url_list.append(arg)
        elif opt in ['-r', '--file']:
            f = open(arg, "r")
            lines = f.readlines()  # 读取全部内容
            for line in lines:
                url_list.append(line.rstrip())
        elif opt in ['-p', '--param']:
            param = arg
        elif opt in ['-v', '--version']:
            print('2.0.1'+'\n')
            return False
        elif opt in ['-h', '--help']:
            str = '''
            
        ___
       __H__
 ___ ___[)]_____ ___ ___  {2.0.1}
|_ -| . [,]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://github.com/11072162
            
Usage: sqlinject.py [options]

Options:
  -h, --help            Show basic help message and exit
  -v, --version         Show version information
 
  Target:
      At least one of these options has to be provided to define the
      target(s)
    
      -u URL, --url=URL     Target URL (e.g. "http://www.site.com/vuln.php?id=1")
      -r File, --file=File  Target File (e.g. "/home/test/text.txt")
  Request:
      These options can be used to specify how to connect to the target URL
      
      -p Parameter, --param=Parameter (e.g. "?id=1" or "id=1")

[!] to see full list of options run with '-hh'
            '''
            print(str)
            input("Press Enter to continue...")
            return False

    for url in url_list:
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if (re.match(regex, url) is not None) == False:
            print('The domain name format is incorrect. Please re-enter it')
            return False

        path = os.getcwd()
        # 调用rad爬虫抓取url地址给sqlmap使用
        rad_result = path+'/rad/rad.json'
        if os.path.exists(rad_result):
            os.remove(rad_result)
        if os.path.exists('result.txt'):
            os.remove('result.txt')
        if platform.system().lower() == 'windows':
            cmd = path + '/rad/rad_windows_amd64.exe -t ' + url + " -json " + rad_result
        else:
            cmd = path + '/rad/rad_linux_amd64 -t ' + url + " -json " + rad_result
        os.system(cmd)
        blackExt = ['.gif','.jpg','jpeg','.png','.psd','.bmp','.wmv','.mov','.mp4','.avi','.wav','.mp3','.txt','.doc','.wps','.docx','.xls','.xlsx','.pdf','.rar','.zip','.exe','.iso','.tmp','.js','.css','.log','.apk','.dll','.xml','.chm']
        url_data = []
        i = 1  # 初始化一个变量
        is_rad = 0
        while i <= 1:
            if os.path.isfile(rad_result) and os.path.getsize(rad_result):
                is_rad = 1
                i = 2
        if is_rad:
            with open(rad_result, 'r') as fr:
                url_list = json.load(fr)
                i = 0
                for data in url_list:
                    url = data['URL']
                    _url = urlparse(url)
                    if _url.query == '' and param == None:
                        continue
                    status = 1
                    for key in blackExt:
                        if url.lower().find(key) != -1:
                            status = 0
                            break
                    if status:  #调用sqlmap检测是否存在sql注入漏洞
                        if i >= 10:
                            continue
                        i += 1
                        if param != None:
                            if param.startswith('?'):
                                if _url.query:
                                    url = url+'&'+ param.lstrip('?')
                                else:
                                    url += param
                            else:
                                if _url.query:
                                    url = url+'&'+ param
                                else:
                                    url = url + '?'+param
                        shutil.rmtree(os.getcwd() + '/sqlmap/log/')
                        cmd = "python "+os.getcwd()+"/sqlmap/sqlmap.py -u \""+url+"\" --batch --retries=1 --random-agent --output-dir="+os.getcwd()+"/sqlmap/log"
                        os.system(cmd)
                        url_port = _url.netloc
                        path = os.getcwd() + '/sqlmap/log/'+url_port
                        if os.path.exists(path) == False or os.path.exists(path+'/log') == False or os.path.getsize(path+'/log') == 0:
                            print('No injection point found：'+url+'\n')
                            continue
                        else:
                            print('There is an injection point for this URL：'+url+'\n')
                            with open(os.getcwd()+'/result.txt', mode='a') as filename:
                                filename.write(url+'\n')
                            url_data.append(url)
        for url in url_data:
            print(url)