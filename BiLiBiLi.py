import json
import random
import re
from urllib.parse import quote

import requests

ip_url = 'https://ip.jiangxianli.com/api/proxy_ip'
r = requests.get(ip_url)
proxy = {'HTTP': 'http://' + r.json()['data']['ip'] + ':' + r.json()['data']['port']}
print(proxy)
path = 'C:/Users/Jackson-art/Desktop/'


class BiLiBiLi_phone():
    def __init__(self, s_url):
        self.url = s_url
        self.headers = {
            'origin': 'https://m.bilibili.com',
            'referer': self.url,
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
        }

    def bili_Download(self):
        r = requests.get(self.url, proxies=proxy, headers=self.headers)
        video_name = re.findall(',"title":"(.*?)","pubdate":', r.text)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = re.findall(',"url":"(.*?)","backup_url"', r.text)[0].encode('utf-8').decode('unicode_escape')
        r = requests.get(video_url, proxies=proxy, headers=self.headers)
        with open(path + video_name + '.mp4', 'wb')as f:
            f.write(r.content)
        print("【BiLiBiLi】: {} 下载完成！".format(video_name))


class BiLiBiLi_api():
    def __init__(self, s_url):
        self.url = s_url.split('?')[0]
        self.header1 = {
            'Host': 'www.shipinyu.com',
            'Origin': 'http://www.shipinyu.com',
            'Referer': quote('http://www.shipinyu.com/video?url={}&page=video&submit=视频下载'.format(self.url)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }
        self.data = {
            'url': self.url,
            'format': 'flv',
            'from': 'parse',
            'retry': '1'
        }
        self.header2 = {
            'origin': 'https://www.bilibili.com/',
            'referer': self.url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def BL_api_Download(self):
        r = requests.post('http://www.shipinyu.com/parse', proxies=proxy, data=self.data, headers=self.header1)
        video_name = re.findall('data-clipboard-text="(.*?)"', r.json()['msg'])[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = re.findall('href="(.*?)"', r.json()['msg'])[0].replace('amp;', '')
        r1 = requests.get(video_url, proxies=proxy, headers=self.header2)
        with open(path + video_name + '.flv', 'wb')as f:
            f.write(r1.content)
        print("【BiLiBiLi】: {} 下载完成！".format(video_name))


class BiLiBiLi():
    def __init__(self, s_url):
        self.url = s_url
        self.header = {
            'Range': 'bytes=0-',
            'referer': self.url,
            'origin': 'https://www.bilibili.com/',
            # 'cookie':'填写自己的B站大会员cookie',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def BL_download(self):
        html = requests.get(self.url, headers=self.header).text
        json_data = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        video_name=re.findall(',"title":"(.*?)","', html)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video = json.loads(json_data)['data']['dash']['video'][0]['baseUrl']
        self.download(video,path+video_name+'.flv')
        print("【BiLiBiLi】: {} 视频下载完成！".format(video_name))
        audio = json.loads(json_data)['data']['dash']['audio'][0]['baseUrl']
        self.download(audio, path + video_name + '.mp3')
        print("【BiLiBiLi】: {} 音频下载完成！".format(video_name))

    def download(self,url,rel_path):
        r = requests.get(url, headers=self.header)
        with open(rel_path, 'wb')as f:
            f.write(r.content)

def user_ui():
    print('*' * 10 + '\t BiLiBiLi视频下载\t' + '*' * 10)
    print('*' * 5 + "\t\tAuthor:  高智商白痴\t\t" + '*' * 5)
    share_url = input('请输入分享链接: ')
    choice = int(input("1、模拟手机端下载  2、调用接口下载  3、直接下载\n选择下载方式："))
    if choice == 1:
        BiLiBiLi_phone(share_url).bili_Download()
    if choice == 2:
        BiLiBiLi_api(share_url).BL_api_Download()
    if choice == 3:
        BiLiBiLi(share_url).BL_download()


if __name__ == '__main__':
    user_ui()

# https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid=6823116&page_num=0&page_size=500&biz=all
# https://space.bilibili.com/6823116/album
