
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

class DY():  # 抖音
    headers = {  # 模拟手机端
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
    }

    def __init__(self, s_url):
        self.s_url=str(s_url).replace('\n','')
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接

    def dy_download(self):
        rel_url = str(requests.get(self.url, proxies=proxy, headers=self.headers).url)
        if 'video' == rel_url.split('/')[4]:
            URL = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + rel_url.split('/')[5] + '&dytk='
            r = requests.get(URL, proxies=proxy, headers=self.headers)
            video_url = r.json()['item_list'][0]['video']['play_addr']['url_list'][0].replace('/playwm/', '/play/')
            video_name = r.json()['item_list'][0]['share_info']['share_title'].split('#')[0].split('@')[0].replace(' ','')
            if video_name == '':
                video_name = int(random.random() * 2 * 1000)
            if len(str(video_name)) > 20:
                video_name = video_name[:20]
            video = requests.get(video_url, proxies=proxy, headers=self.headers).content
            with open('./' + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
            if 'www.iesdouyin.com' in self.s_url:
                print("【抖音短视频】: {}.mp4 无水印视频下载完成！".format(video_name))
            if 'v.douyin.com' in self.s_url:
                print("【抖音短视频/抖音极速版】: {}.mp4 无水印视频下载完成！".format(video_name))

def user_ui():
    print('*' * 10 + '\t 短视频平台无水印聚合下载\t' + '*' * 10)
    print('*' * 5 + "\t\tAuthor: Jackson-art\t\t" + '*' * 5)
    print('*' * 5 + '  (直接粘贴复制内容，程序会自动提取链接)  ' + '*' * 5)
    share_url = input('请输入分享链接: ')
    if 'www.iesdouyin.com' in share_url or 'v.douyin.com' in share_url:  # 抖音  /  抖音极速版
        DY(share_url).dy_download()


if __name__ == '__main__':
    user_ui()
