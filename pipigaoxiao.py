
import time
import random
import requests
from tqdm import tqdm

proxies = []
for a in tqdm(range(4),desc='正在准备代理IP: '):
    url = 'https://ip.jiangxianli.com/api/proxy_ip'
    r = requests.get(url)
    time.sleep(random.random())
    proxies.append('http://' + r.json()['data']['ip'] + ':' + r.json()['data']['port'])
proxy = {'HTTP': random.choice(proxies)}
print(proxy)

class PPGX():  # 皮皮搞笑
    def __init__(self, url):
        s_url = url
        self.headers = {
            'Host': 'share.ippzone.com',
            'Origin': 'http://share.ippzone.com',
            'Referer': s_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
        }
        self.JSON = {
            "pid": int(str(s_url).split('=')[-1]),
            "mid": int(str(s_url).split('&')[-2].split('=')[-1]),
            "type": "post"
        }

    def ppgx_download(self):
        URL = 'http://share.ippzone.com/ppapi/share/fetch_content'
        r = requests.post(URL, proxies=proxy, headers=self.headers, json=self.JSON)
        video_name = r.json()['data']['post']['content'].replace(' ','')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['data']['post']['videos'][str(r.json()['data']['post']['imgs'][0]['id'])]['url']
        video = requests.get(video_url, proxies=proxy).content
        with open('./' + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【皮皮搞笑】: {}.mp4 无水印视频下载完成！".format(video_name))


def user_ui():
    print('*' * 10 + '\t 短视频平台无水印聚合下载\t' + '*' * 10)
    print('*' * 5 + "\t\tAuthor: Jackson-art\t\t" + '*' * 5)
    print('*' * 5 + '  (直接粘贴复制内容，程序会自动提取链接)  ' + '*' * 5)
    share_url = input('请输入分享链接: ')
    if 'ippzone.com' in share_url:  # 皮皮搞笑
        PPGX(share_url).ppgx_download()


if __name__ == '__main__':
    user_ui()
