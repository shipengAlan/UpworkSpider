#! /usr/bin/env python
# coding = utf-8
import pycurl
import StringIO
import re
import time
import random


def getPage(page=1):
    url = 'https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/?page=%s' % str(page)
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    html_item_list = s.getvalue()
    m = re.search('var phpVars = (.+)', html_item_list)
    with open('tasks.txt', 'a') as f:
        f.write(m.group(1)[:-1] + '\n')

if __name__ == '__main__':
    for i in range(1, 501):
        print i
        r = random.random()
        if r > 0.5:
            print 'sleep:', r * 1.5
            time.sleep(r * 1.5)
        try:
            getPage(i)
        except:
            print 'TIMEOUT'
    print 'Done!'
