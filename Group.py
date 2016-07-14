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
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
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


def getList(page, ccrl):
    url = 'https://www.upwork.com/o/profiles/browse/?page=%s&pt=agency' % str(page)
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl = pycurl.Curl()
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
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
    html = s.getvalue()
    tree = etree.HTML(html)
    #items = tree.xpath('//*[@id="contractorTiles"]/section[1]/article/div/div[2]/ul/li')
    for c in range(1, 11):
        t = random.random()
        if t > 0.9:
            time.sleep(t * 1.1)
            print 'sleep:', t * 1.1
        article = tree.xpath('//*[@id="contractorTiles"]/section[%s]/article' % str(c))
        print 'page:', page, ' group:', c
        link = article[0].xpath('./div/div[2]/div/span/a')[0].get('href')
        result = getAgencyIdNum(link, ccrl)
        print 'AgencyId:', result
        if result is not None:
            getMember(result, ccrl)


def getAgencyIdNum(link, crl):
    url = 'https://www.upwork.com%s' % link
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.REFERER, url)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    # crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    html_item_list = s.getvalue()
    result = None
    try:
        m = re.search('"agencyUid":"(\d+)",', html_item_list)
        result = m.group(1)
    except:
        print 'Not find'
    return result


def getUid(tid):
    url = 'https://www.upwork.com/o/profiles/users/%s/' % tid
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
    result = None
    try:
        m = re.search('"uid":"(\d+)",', html_item_list)
        result = m.group(1)
    except:
        f = open('error.html', 'w')
        f.write(html_item_list)
        f.close()
    return result


def getMember(idnum, crl):
    result = getGroupProfile(idnum, crl)
    # get developer
    dict_result = json.loads(result)
    
    
    # developer
    developers = []
    dev_skill_set_e = set()
    dev_skill_set_me = set()
    dev_skill_set_m = set()
    e = 0
    if dict_result['developers'] is not None:
        print 'developers:', len(dict_result['developers'])
        for item in dict_result['developers']:
            e += 1
            print 'e', e
            one_developer = {}
            it = item['ciphertext']
            if it is None or it == '':
                continue
            result = getUid(it)
            if result is not None and result != '':
                data = getWorkerProfile(result, crl)
                if data != '' and data is not None:
                    data = getWorkerProfile(result, crl)
                    dict_data = None
                    try:
                        dict_data = json.loads(data)
                    except:
                        pass
                    if dict_data is not None:
                        skill_list = []
                        if dict_data['profile'] is not None and dict_data['profile']['skills'] is not None:
                            for sk in dict_data['profile']['skills']:
                                skill_list.append(sk['name'])
                                dev_skill_set_e.add(sk['name'])
                                dev_skill_set_me.add(sk['name'])
                            one_developer[result] = skill_list
                            developers.append(one_developer)
    # manager
    m = 0
    managers = []
    if dict_result['managers'] is not None:
        print 'managers:', len(dict_result['managers'])
        for item in dict_result['managers']:
            m += 1
            print 'm', m
            one_manager = {}
            it = item['ciphertext']
            if it is None or it == '':
                continue
            result = getUid(it)
            if result is not None and result != '':
                data = getWorkerProfile(result, crl)
                if data != '' and data is not None:
                    dict_data = None
                    try:
                        dict_data = json.loads(data)
                    except:
                        pass
                    if dict_data is not None:
                        skill_list = []
                        if dict_data['profile'] is not None and dict_data['profile']['skills'] is not None:
                            for sk in dict_data['profile']['skills']:
                                skill_list.append(sk['name'])
                                dev_skill_set_me.add(sk['name'])
                                dev_skill_set_m.add(sk['name'])
                            one_manager[result] = skill_list
                            managers.append(one_manager)
    final_result = {}
    final_result['developers'] = developers
    final_result['managers'] = managers
    final_result['gid'] = idnum
    file = open('group.txt', 'a+')
    file.write(json.dumps(final_result) + '\n')
    file.close()
    ###
    file1 = open('group_skill_set_e.txt', 'a+')
    final_result2 = {'gid': idnum, 'skills': list(dev_skill_set_e)}
    file1.write(json.dumps(final_result2) + '\n')
    file1.close()
    ###
    file2 = open('group_skill_set_me.txt', 'a+')
    final_result3 = {'gid': idnum, 'skills': list(dev_skill_set_me)}
    file2.write(json.dumps(final_result3) + '\n')
    file2.close()
    ###
    file3 = open('group_skill_set_m.txt', 'a+')
    final_result4 = {'gid': idnum, 'skills': list(dev_skill_set_m)}
    file3.write(json.dumps(final_result4) + '\n')
    file3.close()


# get group profile
def getGroupProfile(idnum, crl):
    link = 'https://www.upwork.com/agencies/public/api/v1/profile/%s' % str(idnum)
    # print link
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
    crl.setopt(pycurl.URL, link)
    crl.setopt(pycurl.REFERER, link)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    # crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    result = s.getvalue()
    return result
    """
    out = open('link.html', 'w')
    out.write(html)
    out.close()
    """


# get worker's profile and skills
def getWorkerProfile(id_num, crl):
    link = 'https://www.upwork.com/freelancers/api/v1/profile/%s' % str(id_num)
    # print link
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0"
    s = StringIO.StringIO()
    crl.setopt(pycurl.COOKIEJAR, "cookie_file")
    crl.setopt(pycurl.PROXY, 'http://127.0.0.1:1080')
    crl.setopt(pycurl.URL, link)
    crl.setopt(pycurl.REFERER, link)
    crl.setopt(pycurl.FOLLOWLOCATION, True)
    crl.setopt(pycurl.TIMEOUT, 60)
    crl.setopt(pycurl.ENCODING, 'gzip')
    crl.setopt(pycurl.USERAGENT, useragent)
    # crl.setopt(pycurl.NOSIGNAL, True)
    crl.setopt(pycurl.WRITEFUNCTION, s.write)
    crl.perform()
    result = s.getvalue()
    return result

if __name__ == "__main__":
    crl = Login()
    print 'Login success!'
    for i in range(1, 501):
        try:
            getList(i, crl)
        except Exception as e:
            print 'TIMEOUT', e
    """
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
    """
