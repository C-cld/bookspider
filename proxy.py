# 代理来自阿布云https://center.abuyun.com http代理动态版

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": "http-dyn.abuyun.com",
    "port": "9020",
    "user": "",
    "pass": "",
}


def get_proxy():
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies