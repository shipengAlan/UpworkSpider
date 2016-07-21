#! /usr/bin/env python
#coding=utf-8
import pycurl
import StringIO
from lxml import etree
import os
import re
import json
import time
import random

def getList(page=1):
    url = 'https://www.upwork.com/o/profiles/browse/?page=%s' % str(page)
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    # output the html page
    html = s.getvalue()
    tree = etree.HTML(html)
    persons = tree.xpath('//*[@id="contractorTiles"]/section')
    out = open('worker_country_city.txt', 'a+')
    for i in range(10):
        item = {}
        country = persons[i].xpath('./article/div/div[2]/div/p[1]/strong')
        item['country'] = country[0].text
        ciper_text = persons[i].xpath('./article')[0].get('data-cipher-text')
        item['ciper_text'] = ciper_text
        item['city'] = getCity(ciper_text)
        # //*[@id="optimizely-header-container-default"]/div[2]/span[2]/span
        skill_list = persons[i].xpath('./article/div/div[2]/ul/li')
        # print len(skill_list)
        skill_set = []
        for sk in skill_list:
            s = sk.xpath('./a')[0].get('data-skill')
            skill_set.append(s)
            # print s
        item['skills'] = skill_set
        out.write(json.dumps(item) + '\n')
    out.close()


def getCity(ciper_text):
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    url = "https://www.upwork.com/o/profiles/users/_%s/" % ciper_text
    # print url
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    # output the html page
    html = s.getvalue()
    m = re.search('var phpVars = (.+)', html)
    data = m.group(1)[:-1]
    dict_data = json.loads(data)
    if 'profile' in dict_data:
        if 'profile' in dict_data['profile']:
            if 'location' in dict_data['profile']['profile']:
                if 'city' in dict_data['profile']['profile']['location']:
                    city = dict_data['profile']['profile']['location']['city'].encode('utf-8')
                    return city
    return None

if __name__ == "__main__":
    for p in range(1, 501):
        print 'page ', p
        r = random.random()
        if r > 0.8:
            print 'sleep: ', r
            time.sleep(r)
        try:
            getList(p)
        except:
            print p, 'is error'
    print 'over'
