"""
time: 2023.10.23
cron: 23 0 * * *
new Env('sockboom签到');
地址：https://sockboom.link/
环境变量 bd_sockboom = 邮箱#密码
多账号用&分开
"""

import json
import time
import requests
from os import environ, path
from bs4 import BeautifulSoup


# 读取通知
def load_send():
    global send
    cur_path = path.abspath(path.dirname(__file__))
    if path.exists(cur_path + "/SendNotify.py"):
        try:
            from SendNotify import send
            print("加载通知服务成功！")
        except:
            send = False
            print(
                '''加载通知服务失败~\n请使用以下拉库地址\nql repo https://github.com/Bidepanlong/ql.git "bd_" "README" "SendNotify"''')
    else:
        send = False
        print(
            '''加载通知服务失败~\n请使用以下拉库地址\nql repo https://github.com/Bidepanlong/ql.git "bd_" "README" "SendNotify"''')


load_send()


def get_env(key, default='', output=True, In=False):
    def no_read():
        if In:
            return input('请输入sockboom key:')
        if output:
            print(f"未填写环境变量 {key} 请添加")
            exit(0)
        return default

    return environ.get(key) if environ.get(key) else no_read()


class sockboom():
    def __init__(self, ck):
        self.msg = ''
        self.ck = ck
        self.cks = ''
        self.index_url = 'https://sockboom.link'

    def sign(self):
        time.sleep(0.5)
        check_url = self.index_url+'/user/checkin'
        login_url = self.index_url+'/auth/login'
        usr_url = self.index_url+"/user"
        login_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        login_data = "email={}&passwd={}&code=".format(self.ck[0], self.ck[1])
        response = requests.post(
            login_url, headers=login_header, data=login_data)
        result = json.loads(response.content)
        if result.get('ret') != 1:
            self.msg += "登录失败，{}\n".format(result.get('msg'))
            return self.msg
        self.msg += '登录成功,用户：{}, {}\n'.format(
            result.get('user'), result.get('msg'))

        cookies = response.cookies
        cookies_dict = cookies.get_dict()
        for key, value in cookies_dict.items():
            ck = f"{key}={value}"
            self.cks += ck + ';'

        sign_header = {
            'cookie': self.cks,
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"'
        }
        response = requests.post(check_url, headers=sign_header)
        if response.status_code == 200:
            result = json.loads(response.text)
            self.msg += result.get('msg')+'\n'
        return self.msg

    def get_sign_msg(self):
        return self.sign()


if __name__ == '__main__':
    token = get_env('bd_sockboom')

    msg = ''
    cks = token.split('&')
    print("检测到{}个ck记录\n开始sockboom签到续命\n".format(len(cks)))
    for ck in cks:
        up = ck.split('#')
        run = sockboom(up)
        msg += run.get_sign_msg()
        print(msg)
    if send:
        send("ikuuu签到通知", msg)
