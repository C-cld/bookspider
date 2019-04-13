import proxy
import requests
from bs4 import BeautifulSoup

home_url = 'https://book.douban.com'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'https://book.douban.com'
}


# 取得每个标签的链接
def get_all_tag_url():
    px = proxy.get_proxy()
    # tag_page_html = requests.get(home_url + '/tag/', proxies=px, headers=header)
    tag_page_html = requests.get(home_url + '/tag/', headers=header)
    tag_page_content = BeautifulSoup(tag_page_html.text, 'html.parser')
    tags = tag_page_content.find('div', class_='article').find_all('a')
    tag_urls = []
    for a in tags:
        if not a.get('href') is None:
            tag_urls.append(home_url + a.get('href'))
    del tag_urls[0]
    return tag_urls


# 取得每个标签的最大页数
def find_max_page(tag_url):
    home_html = requests.get(tag_url, headers=header)
    page_content = BeautifulSoup(home_html.text, 'html.parser')
    # 取得页数div中倒数第二个标签，即为最大页数
    paginator = page_content.find('div', class_='paginator').find_all('a')
    if paginator is not None:
        size = int(paginator[len(paginator) - 2].text)
    else:
        size = 0
    # 豆瓣傻逼，虽然页数很多，但是50页后全都是空的。
    if size > 50:
        size = 50
    return size


# 每个标签下的每个页链接
def get_all_page_url(tag_url):
    max_page = find_max_page(tag_url)
    page_urls = []
    # 遍历每一个标签里的每一页
    for n in range(0, max_page):
        page_url = tag_url + '?start=' + str(n * 20) + '&type=T'
        page_urls.append(page_url)
    return page_urls


# 取得每一页的书
def get_books_per_page(page_url):
    px = proxy.get_proxy()
    # book_list_html = requests.get(page_url, proxies=px, headers=header)
    book_list_html = requests.get(page_url, headers=header)
    book_list_content = BeautifulSoup(book_list_html.text, 'html.parser')
    book_list = book_list_content.find_all('div', class_='info')
    books = []
    for bl in book_list:
        books.append(bl.find('a'))
    return books


# 取得每本书的详细信息
def get_book_info(book_url):
    px = proxy.get_proxy()
    # book_html = requests.get(book_url, proxies=px, headers=header, timeout=10)
    book_html = requests.get(book_url, headers=header)
    book_content = BeautifulSoup(book_html.text, 'html.parser')
    book_info = book_content.find('div', class_='subject')
    return book_info
