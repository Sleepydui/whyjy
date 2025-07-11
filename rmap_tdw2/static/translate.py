# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2019-03-30 12:54:14
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-04-29 19:09:26
import json
import random
import requests
import urllib.parse
from hashlib import md5
import os


def translate_api(text):
    appid = '20190330000282580'
    secretKey = 'rP9jI8f3_XF0d76tt4NY'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = text
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()

    myurl = myurl+'?' + '&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+ '&appid='+appid+'&salt='+str(salt)+'&sign='+sign
    return myurl

def parse(myurl):
    response = requests.get(myurl)
    try:
      rans_result = json.loads(response.text)['trans_result'][0]['dst']
    except Exception as e:
      print(json.loads(response.text))
    return rans_result
def goTree(root, index, dictionary):
    words = root['data'][index]
    for word in words:
      if not word in dictionary:
        try:
          ans = parse(translate_api(word)).lower()
          dictionary[word] = ans
        except Exception as e:
          print(e)
    for child in root['children']:
      goTree(child, index, dictionary)

def calWordsCnt(root, index, wordCnt):
    words = root['data'][index]
    # print(words)
    for word in words:
      if not word in wordCnt:
        try:
          wordCnt[word] = 0
        except Exception as e:
          print(e)
      wordCnt[word] = wordCnt[word] + 1
    for child in root['children']:
      calWordsCnt(child, index, wordCnt)


def dealFile(file):
    inpt = open(inputfolder + '/' + file, 'r')
    data = json.load(inpt)
    dictionary = {}
    index = data['fields'].index('words')
    wordCnt = {}
    calWordsCnt(data['tree'], index, wordCnt)
    finalWords = []
    for word in wordCnt:
      if wordCnt[word] > 1:
        # print(word)
        finalWords.append(word)

    print(len(finalWords))

    for word in finalWords:
      try:
        text = parse(translate_api(word)).lower()
        dictionary[word] = text
        print(word, text)
      except Exception as e:
        print(e)

    out = {'dict': dictionary}
    output = open(outputfolder + '/' + file, 'w')   
    json.dump(out, output, ensure_ascii=False)
    inpt.close()
    output.close()


inputfolder = 'data'
outputfolder = 'translate'
# for root, dirs, files in os.walk(inputfolder):
#     for file in files:
#         if '.json' in file:
#             try:
#                 dealFile(file)
#             except Exception as e:
#                 print(e)
filename = 'chunwan.json'

dealFile(filename)
# text = '苹果'
# myurl = translate_api(text)
# response = requests.get(myurl)
# print(response.text)
# rans_result = json.loads(response.text)['trans_result'][0]['dst']
# print(rans_result)
