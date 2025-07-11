# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2019-03-30 12:54:14
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-06-11 22:35:32
import json
import random
import os

def goTree(root, index):
    text = root['data'][index]
    text = text.split('@姚晨 六百多条')[0].split('@姚晨: 六百多条')[0]
    text = text.split('@姚晨 :六百多条的转发')[0]
    text = text.split('@姚晨:六百多条的转发')[0]
    text = text.split('姚晨:六百多条的转发')[0]
    text = text.split('姚晨: 六百多条的转发')[0]
    text = text.strip()
    root['data'][index] = text
    for child in root['children']:
        goTree(child, index)

def dealFile(file):
    inpt = open(inputfolder + '/' + file, 'r')

    data = json.load(inpt)
    inpt.close()
    index = data['fields'].index('text')

    goTree(data['tree'], index)

    out = data

    dataStr = json.dumps(out,  ensure_ascii=False)
    output = open(inputfolder + '/' + file, 'w')
    output.write(dataStr)
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
filename = 'nanxiaoqi.json'

dealFile(filename)
# text = '苹果'
# myurl = translate_api(text)
# response = requests.get(myurl)
# print(response.text)
# rans_result = json.loads(response.text)['trans_result'][0]['dst']
# print(rans_result)
