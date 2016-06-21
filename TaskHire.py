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


def getPage(crl, page=1):
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    ss = StringIO.StringIO()
    info_url = r"https://www.upwork.com/o/jobs/browse/c/design-creative/?client_hires=1-9,10-&page=" + str(page) + r'&sort=create_time%2Bdesc'
    crl.setopt(pycurl.URL, info_url)
    #rl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.REFERER,
               "https://www.upwork.com/ab/jobs-home/1617062?cell=Treatment3")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.WRITEFUNCTION, ss.write)
    crl.perform()
    html_item_list = ss.getvalue()
    tree = etree.HTML(html_item_list)
    result = []
    article = tree.xpath('//*[@id="jobs-list"]/article')
    for i in range(10):
        href = article[i].xpath('./div[1]/div/header/h2/a')
        result.append(href[0].get('href'))
    return result

def getItem(href, crl):
    url = 'https://www.upwork.com' + href
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    ss = StringIO.StringIO()
    crl.setopt(pycurl.URL, url)
    #rl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.REFERER,
               "https://www.upwork.com/ab/jobs-home/1617062?cell=Treatment3")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.WRITEFUNCTION, ss.write)
    crl.perform()
    html_item_list = ss.getvalue()
    m = re.search("app.value\('otherJobs', (.+)\);", html_item_list)
    """
    tree = etree.HTML(html_item_list)
    h = tree.xpath('//*[@id="layout"]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div/h2')
    print h[0].text
    """
    string = m.group(1)
    # return list
    return json.loads(string)


def getOtherJobs(otherJob, crl):
    url = 'https://www.upwork.com/job/' + otherJob['ciphertext']
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    ss = StringIO.StringIO()
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.REFERER,
               "https://www.upwork.com/ab/jobs-home/1617062?cell=Treatment3")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.WRITEFUNCTION, ss.write)
    crl.perform()
    html_item_list = ss.getvalue()
    html_item_list = html_item_list.replace('\n', '')
    m = re.search('<span class="text-muted">Hires:</span>    (\d+)</p>', html_item_list)
    if m is not None:
        return int(m.group(1))
    else:
        return None


if __name__ == '__main__':
    #
    redundancy = 0
    num = 0
    for i in range(1, 101):
        print 'page:', i
        r = random.random()
        if r > 0.5:
            print 'sleep %ss' % str(r * 1.5)
            time.sleep(r * 1.5)
        try:
            crl = pycurl.Curl()
            pagelist = getPage(crl, i)
            # crl = Login()
            otherJobs_list = []
            for i in range(len(pagelist)):
                item_list = getItem(pagelist[i], crl)
                otherJobs_list.extend(item_list)
            out = open('items.txt', 'a')
            for item in otherJobs_list:
                Hires = getOtherJobs(item, crl)
                if Hires is not None:
                    if int(Hires) > 1:
                        redundancy += 1
                    num += 1
                out.write(str(Hires) + ':' + json.dumps(item) + '\n')
            out.close()
            print num, redundancy
        except:
            print 'timeout!'
    print 'over!'
    print num, redundancy
