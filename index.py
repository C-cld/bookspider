import pages
import time
import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 控制台
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
# 文件
fileHandler = logging.FileHandler('log/book.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

tag_urls = pages.get_all_tag_url()
for tag_url in tag_urls:
    page_urls = pages.get_all_page_url(tag_url)
    for page_url in page_urls:
        logger.info('===============================' + page_url + '===============================')
        books = pages.get_books_per_page(page_url)
        for book in books:
            book_url = book.get('href')
            book_info = pages.get_book_info(book_url)
            title = book.get('title')
            img = book_info.find('img').get('src')
            bb = book_info.find('div', id='info').text
            # isbn不在标签中，所以直接截取字符串
            isbn_start = bb.find('ISBN:')
            isbn = bb[isbn_start:-1].replace('ISBN: ', '')
            logger.info(title + ' | ' + isbn + ' | ' + img)
