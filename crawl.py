#!/usr/bin/python3
# -*- coding: utf8 -*-

import re
import json
import requests
from bs4 import BeautifulSoup
from string import punctuation

js = {}
with open('options.json', 'r') as f:
    js = json.load(f)

url = js["url"]
L = js["crawl_left"]
R = js["crawl_right"]

def cleanHtml(raw_html):
    raw_html = str(raw_html)
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def removePunctuation(s):
    for val in punctuation:
        s = s.replace(val, '')
    return s.replace('“', '')

def getContent(arr):
    s = ''
    for val in arr:
        s += cleanHtml(val) + ' '
    arr = s.split(' ')
    res = ''
    for val in arr:
        if val != '':
            if len(res) > 0:
                res += ' ' + val
            else:
                res += val
    return removePunctuation(res).lower()

ans = ''

for i in range(L, R+1):
    crawlUrl = url + str(i)
    print('Crawling', crawlUrl)
    soup = BeautifulSoup(requests.get(crawlUrl).text, 'html.parser')
    print('Done crawling', crawlUrl)
    for d in soup.find_all('div', {"class": "chapter-c"}):
        content = getContent(d.contents)
        if len(ans) > 0:
            ans += ' ' + content
        else:
            ans += content


outputFile = js["crawl_output"]

print('Crawled', len(ans.split(' ')), 'words')
print('Storing it to', outputFile)

f = open(outputFile, "w")
f.write(ans)
f.close()