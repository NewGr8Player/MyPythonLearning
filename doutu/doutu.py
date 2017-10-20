# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

global count


def maxCount():
    global path
    path = os.path.abspath('.') + '\\pictures'
    number = 0
    for root, dirs, files in os.walk(path):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files) # 当前路径下所有非目录子文件
        for file in files:
            if int(file.split('.')[0]) > number:
                number = int(file.split('.')[0])
    print(number)
    return number


class doutuSpider(object):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}

    def get_url(self, url):
        data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(data.content, 'lxml')
        totals = soup.findAll("a", {"class": "list-group-item"})
        for one in totals:
            sub_url = one.get('href')
            global path
            path = os.path.abspath('.') + '\\pictures'
            if not os.path.exists(path):
                os.mkdir(path)
            try:
                self.get_img_url(sub_url)
            except:
                pass

    def get_img_url(self, url):
        data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(data.content, 'lxml')
        totals = soup.find_all('div', {'class': 'artile_des'})
        for one in totals:
            img = one.find('img')
            try:
                sub_url = img.get('src')
            except:
                pass
            finally:
                urls = 'http:' + sub_url
            try:
                self.get_img(urls)
            except:
                pass

    def get_img(self, url):
        filetype = url.split('/')[-1].split('.')[-1]
        global path, count
        img_path = path + '\\' + str(count) + '.' + filetype
        img = requests.get(url, headers=self.headers)
        try:
            with open(img_path, 'wb') as f:
                print(img_path)
                f.write(img.content)
                count += 1
        except:
            pass

    def create(self, start=1, end=100):
        for count in range(start, end):
            url = 'https://www.doutula.com/article/list/?page={}'.format(count)
            print('开始下载第{}页'.format(count))
            self.get_url(url)


if __name__ == '__main__':
    global count
    count = maxCount()
    doutu = doutuSpider()
    doutu.create()
