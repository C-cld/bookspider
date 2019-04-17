import pages
import logging
import multiprocessing
import pymysql
import traceback
import readconfig

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 文件
fileHandler = logging.FileHandler('log/book.log', mode='a', encoding='UTF-8')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


def print_book_detail(tag_url):
    try:
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
                try:
                    # 数据库连接
                    connect = pymysql.Connect(host=readconfig.db_host, port=int(readconfig.db_port), user=readconfig.db_user, passwd=readconfig.db_pass, db=readconfig.db_name, charset='utf8')
                    cursor = connect.cursor()
                    sql = 'insert into book(isbn, title, img) values ("%s", "%s", "%s")' % (isbn, title, img)
                    cursor.execute(sql)
                    connect.commit()
                    cursor.close()
                    connect.close()
                except pymysql.err.IntegrityError:
                    logger.error('重复爬取：' + title + ' | ' + isbn + ' | ' + img)
                else:
                    logger.info(title + ' | ' + isbn + ' | ' + img)
    except :
        s = traceback.format_exc()
        print(s)


if __name__ == '__main__':
    tag_urls = pages.get_all_tag_url()
    process_num = int(readconfig.process_num)
    p = multiprocessing.Pool(processes=process_num)
    for tu in tag_urls:
        p.apply_async(print_book_detail, args=(tu,))
    p.close()
    p.join()
    print('All processes done!')
