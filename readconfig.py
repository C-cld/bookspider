import configparser

cf = configparser.ConfigParser()
cf.read('config.conf', encoding="utf-8-sig")

proxy_host = cf.get('proxy', 'proxy_host')
proxy_port = cf.get('proxy', 'proxy_port')
proxy_user = cf.get('proxy', 'proxy_user')
proxy_pass = cf.get('proxy', 'proxy_pass')

db_host = cf.get('db', 'db_host')
db_port = cf.get('db', 'db_port')
db_user = cf.get('db', 'db_user')
db_pass = cf.get('db', 'db_pass')
db_name = cf.get('db', 'db_name')

process_num = cf.get('process', 'process_num')
