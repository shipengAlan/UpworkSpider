#! /usr/bin/env python
# coding = utf-8
import pycurl
import StringIO
from lxml import etree
import os
import re
import json
import time
import random


def getUid(tid):
    url = 'https://www.upwork.com/o/profiles/users/%s/' % tid
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
    result = None
    try:
        m = re.search('"uid":"(\d+)",', html_item_list)
        result = m.group(1)
    except:
        f = open('error.html', 'w')
        f.write(html_item_list)
        f.close()
    return result


def Login():
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    # clear old cookie file
    if os.path.exists("cookie_file"):
        os.remove("cookie_file")
    # pre-visit to get hidden perms
    url = "https://www.upwork.com/login"
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    # set proxy for debug
    # crl.setopt(pycurl.PROXY, 'http://127.0.0.1:8080')
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.NOSIGNAL, True)
    # auto cookie and save in file
    crl.setopt(pycurl.COOKIEFILE, "cookie_file")
    # use the cookie file
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    # output the html page
    html = s.getvalue()
    f = open('login.html', 'w')
    f.write(html)
    f.close()
    tree = etree.HTML(html)
    # get hidden tag which is related to the cookie
    node = tree.xpath('//*[@id="login_redir"]')
    data = {}
    data['login[redir]'] = node[0].get('value')
    node = tree.xpath('//*[@id="login_iovation"]')
    data['login[iovation]'] = '0400JapG4txqVP4Nf94lis1ztln1Bau9lgpsG5mKV1GZGzZSop9ypcPEXKmcgnppqWW9dUsprl5Sq8nl3OCiMt8Ua81mEx5T4nMe8QddY13Dt9esblX8c4ErVQz1gslwtNv6MLejutG4hxLDBnE+/kQV4SgO+Uqpxb++AfOPjzqyODId+TYQ4ximvqXakoCa7XCWI2oesI0NTjkTaYlyf4WWCbtFJUKhVg7gZkyjofMrjz7r2TF5eO491fUJiL5MGqved8wB3Yb8E8/gW8ZhSfRnYZjJNfHTy27cv203ZX2OtqS5M3CXK4MOT9YSi0BUVGHO8WjkCWAGL2Y85h7zmVcUJOHu8xzS9QXZYt9JBUxxiSl3SYyEah9gr9yNGoBvwOkDSAWH/rrXQgXvsD8Ae2HMhGn9cJjqZjvIjNXsgMEghG2DHm3gJbBd7AkH+zgzCnlu2IdccHc397xLnTJfJEuqk7y0LJm5v4M2Yg8CuMOt5MLq4WCiHMbq2Lmq4v4ZaMFsX0MxxgXyLa5LMrPrMVvJlgYGvLM7K5i8+EbOW/+6IbiqWvTbz/c+r6i3sz6LGFTJQEdu2XYvr463cJQOlIif4JLWOlxpt0YU9cmKrLQxcxA7Et2ah6cqo1JO1SuKjjw/m0kKalTW2Q0gqHxyPWh5ilXwux+TgczyugE9BZ98f/eC8Kxc/WslAHfTiz/KBNtSH2g0p48QibxHjahu0NsbTnMY4fvhL8ILOCLbZR7h7p+9KpGjlnjaGdSY5LP1meO4zgAmotjzAwjnVb7uHgXQGX7ojYa45C7OGMW1OJGB+yu6psCbeWacXMFAgCtF9qJG2lft62Puvm/y/tB+TSAcZhcWvEsMdd2++6bKel2Ouf8MzVuR9ICxistLs8Eiejf/xRNviuW67I0XD33a7oOGJJ01jtB35jxEHe6KMpO079KdizKgcTSmkihvGmukvw8/EPNOpFjI2/774f2H/cwW6YlWmk8yGwSZIi7SoUevORpyfchyF93OALdSkBGbeBwmodQA24pXHXjBaQjMMbHuP2Kgjbp7tix7hiykUtJuOoY='
    node = tree.xpath('//*[@id="login__token"]')
    data['login[_token]'] = node[0].get('value')
    data['login[password]'] = 'code@321'
    data['login[username]'] = '840032057@qq.com'
    #print data
    # post login
    crl.setopt(pycurl.URL, url)
    renquest = 'login[_token]=%s&login[iovation]=%s&login[redir]=%s&login[password]=%s&login[username]=%s' % (
        data['login[_token]'], data['login[iovation]'], data['login[redir]'], data['login[password]'], data['login[username]'])
    crl.setopt(pycurl.POSTFIELDS, renquest)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.USERAGENT, useragent)
    # load cookie
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.perform()
    return crl


def getTid(string):
    result = string.split('/')
    return result[1], result[2]


def getPage(crl, page=1):
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    ss = StringIO.StringIO()
    info_url = "https://www.upwork.com/o/profiles/browse/?q=JAVA&page=%s" % str(
        page)
    crl.setopt(pycurl.URL, info_url)
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.REFERER,
               "https://www.upwork.com/ab/jobs-home/1617062?cell=Treatment3")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.WRITEFUNCTION, ss.write)
    crl.perform()
    html_item_list = ss.getvalue()
    tree = etree.HTML(html_item_list)
    result = []
    for i in range(1, 11):
        href = tree.xpath(
            '//*[@id="contractorTiles"]/section[%s]/article/div/div[2]/div/span/a' % str(i))
        result.append(href[0].get('href'))
    return result


def getPersonHistory(uid, crl):
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    purl = 'https://www.upwork.com/freelancers/api/v1/profile/%s' % uid
    print purl
    ss = StringIO.StringIO()
    crl.setopt(pycurl.URL, purl)
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.WRITEFUNCTION, ss.write)
    crl.perform()
    html_item_list = ss.getvalue()
    return html_item_list
    #f = open('items.json', 'w')
    #f.write(html_item_list)
    #f.close()
    """
    for i in range(1, len(items) + 1):
        print i, 'tt'
        date = items[i].xpath('./div/div[1]/div[1]')
        print date.text
        result.append(date.text)
    """
    # result is the person's history
    # return result


def formatResult(final_result):
    f = open('result.txt', 'a')
    for k in final_result.keys():
        content = ','.join(final_result[k])
        f.write(k + ':' + content + '\n')
    f.close()


def outputResult(key, result):
    f = open('result.txt', 'a')
    js = json.loads(result)
    content = js['assignments']
    f.write(key + ':' + json.dumps(content) + '\n')
    f.close()

if __name__ == "__main__":
    crl = Login()
    print 'Login Success!'
    for i in range(1, 501):  # 1001
        print 'page', i
        try:
            result_urls = getPage(crl, i)
        # traverse the all person of one page
            for k in range(len(result_urls)):
                t = random.random()
                if t > 0.5:
                    time.sleep(t * 1.5)
                    print 'sleep:', t * 1.5
                Type, Tid = getTid(result_urls[k])
                if Type != 'freelancers':
                    continue
                print Tid
                uid = getUid(Tid)
                if uid is None:
                    f = open('RestictWorker.txt', 'a')
                    f.write(Tid + '\n')
                    f.close()
                    continue
                result_history = getPersonHistory(uid, crl)
                # final_result[url_id] = result_history
                outputResult(uid, result_history)
        except:
            print 'TIMEOUT'
    # formatResult()
