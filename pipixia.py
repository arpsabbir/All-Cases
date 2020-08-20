
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

class PPX():  # 皮皮虾
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72 '
    }

    def __init__(self, url):
        self.url = url

    def ppx_download(self):
        video_num = str(requests.get(self.url, proxies=proxy, headers=self.headers).url).split('/')[-1].split('?')[0]
        URL = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id=' + video_num + '&source=share'
        r = requests.get(URL, proxies=proxy, headers=self.headers)
        video_name = r.json()['data']['item']['content'].replace(' ','')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['data']['item']['origin_video_download']['url_list'][0]['url']
        video = requests.get(video_url, proxies=proxy).content
        with open('./' + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【皮皮虾】: {}.mp4 无水印视频下载完成！".format(video_name))
        
def user_ui():
    print('*' * 10 + '\t 短视频平台无水印聚合下载\t' + '*' * 10)
    print('*' * 5 + "\t\t\tAuthor:  Jackson-art\t\t\t" + '*' * 5)
    print('*' * 5 + '  (直接粘贴复制内容，程序会自动提取链接)  ' + '*' * 5)
    share_url = input('请输入分享链接: ')
    if 'h5.pipix.com' in share_url:  # 皮皮虾
        PPX(share_url).ppx_download()


if __name__ == '__main__':
    user_ui()
