# 代理来自阿布云https://center.abuyun.com http代理动态版
import readconfig

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": readconfig.proxy_host,
    "port": readconfig.proxy_port,
    "user": readconfig.proxy_user,
    "pass": readconfig.proxy_pass,
}


def get_proxy():
    proxies = {
        "https": proxyMeta,
    }
    return proxies
