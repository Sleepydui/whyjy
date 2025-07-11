# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2019-03-30 12:54:14
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-05-30 10:25:48
import json
import random
import os


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
outputfolder = 'data'
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
