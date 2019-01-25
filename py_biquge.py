#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author;cuich time:2019/01/21
import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
}


def search_book(book_name):
    url = 'https://sou.xanbhx.com/search?siteid=qula&q={}'.format(book_name)
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    content = r.text
    return content


def locate_book(book_name):
    content = search_book(book_name)
    soup = BeautifulSoup(content, "html.parser")
    name = soup.ul.find_all('span', class_='s2')
    names = []
    hrefs = []
    for i in name:
        names.append(i.get_text().strip())
        try:
            hrefs.append((i.a['href']))
        except:
            pass
    names = names[1:4]
    hrefs = hrefs[0:3]           # 由于names[0]为作者简介，所以切去。保留前三个
    info = dict(zip(names, hrefs))
    return info


def show_book(book_name):
    info = locate_book(book_name)
    names = []
    hrefs = []
    for k, v in info.items():
        names.append(k)
        hrefs.append(v)
    for i in range(len(info)):
        print(str(i)+'------'+names[i])
    num = int(input('搜索后有以上书籍符合条件，请输入序号： '))
    print('该书链接为{}'.format(hrefs[num])+'请稍等，正在准备从该网页下载内容...')
    href = hrefs[num]
    r = requests.get(href, headers=headers)
    html = etree.HTML(r.text)
    return html


def get_content(book_name):
    html = show_book(book_name)
    chapter = html.xpath('//*[@id="list"]/dl/dd/a/text()')[12:]
    href = html.xpath('//*[@id="list"]/dl/dd/a/@href')[12:]
    hrefs = []
    for i in href:
        i = "https://www.qu.la"+i
        hrefs.append(i)
    for i in range(len(hrefs)):
        r = requests.get(hrefs[i], headers=headers)
        html = etree.HTML(r.text)
        contents = html.xpath('//*[@id="content"]/text()')
        s = ' '
        for content in contents:
            s = s+content
        with open('F:/novel/{}.txt'.format(book_name), 'ab')as f:
            f.write(chapter[i].encode('utf-8'))
            f.write(s.encode('utf-8'))
        print("已完成" + str(i) + '-----' + str(len(hrefs)))
    f.close()


if __name__ == '__main__':
    book_name = input('请输入书名： ')
    get_content(book_name)
