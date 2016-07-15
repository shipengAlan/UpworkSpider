#! /usr/bin/env python
# coding = utf-8
import pycurl
import StringIO
import re
import time
import random
import json


def getPage(page=1, type_str='web-mobile-software-dev'):
    url = 'https://www.upwork.com/o/jobs/browse/c/%s/?page=%s' % (
        type_str, str(page))
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
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
    with open(type_str + '_tasks.txt', 'a') as f:
        data = m.group(1)[:-1]
        dict_data = json.loads(data)
        if dict_data['jobs'] is not None:
            for job in dict_data['jobs']:
                if job is not None:
                    job_data = {}
                    job_data['ciphertext'] = job['ciphertext']
                    skill_list = []
                    if job['skills'] is not None:
                        for it in job['skills']:
                            skill_list.append(it['name'])
                        job_data['skills'] = skill_list
                        f.write(json.dumps(job_data) + '\n')


def run(page_num, type_str):
    for i in range(1, page_num + 1):
        print i
        r = random.random()
        if r > 0.8:
            print 'sleep:', r * 1
            time.sleep(r * 1)
        try:
            getPage(i, type_str)
        except:
            print 'TIMEOUT'
    print 'Done!'


if __name__ == '__main__':
    """
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
    """
    type_str = ['web-mobile-software-dev',
                'it-networking',
                'data-science-analytics',
                'engineering-architecture',
                'design-creative',
                'writing',
                'translation',
                'legal',
                'admin-support',
                'customer-service',
                'sales-marketing',
                'accounting-consulting']
    page_num = [500,
                329,
                196,
                244,
                500,
                500,
                307,
                71,
                500,
                121,
                500,
                154]

    for i in range(12):
        run(page_num[i], type_str[i])
