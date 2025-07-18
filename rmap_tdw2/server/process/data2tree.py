# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-12-20 21:22:42
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-06-02 22:15:51
# encoding: utf-8
import csv
import glob
import datetime
import json
import os


def addNode(parent, node):
  if node['parent'] == parent['mid'] or node['parent'] == '':
    node['parent'] = parent['mid']
    parent['children'].append(node)
    return True
  else:
    for child in parent['children']:
      if addNode(child, node):
        return True
  return False


def calRepost(root):
  root['direct_reposts_count'] = len(root['children'])
  root['reposts_count'] = 0
  for child in root['children']:
    calRepost(child)
    root['reposts_count'] = child['reposts_count'] + 1


def simplify(root, fields):
  root['data'] = [0 for i in range(len(fields))]
  global leafnumber
  if len(root['children']) == 0:
    leafnumber = leafnumber + 1
  for key in root:
    if key in fields:
      root['data'][fields.index(key)] = root[key]
  for key in fields:
    del root[key]
  for child in root['children']:
    simplify(child, fields)


def process(file):
  if not os.path.exists(outputfolder):
    os.mkdir(outputfolder)
  root = ''

  inpt = open(inputfolder + '/' + file + '.json', 'r')
  data = json.load(inpt)
  fields = data['fields']
  datalist = data['data']
  datalist = sorted(datalist, key=lambda user: int(user[fields.index('t')]))
  wrong = 0
  print('all node number', len(datalist))
  idList = []
  for i, item in enumerate(datalist):
    node = {}
    node['children'] = []
    for j, filed in enumerate(fields):
      node[filed] = item[j]
    if node['mid'] in idList:
      continue
    idList.append(node['mid'])
    if i == 0:
      root = node
    else:
      if not addNode(root, node):
        wrong = wrong + 1

  calRepost(root)
  fields = []
  for key in root:
    if not key == 'children':
      fields.append(key)
  simplify(root, fields)

  out = {'tree': root, 'fields': fields}

  print('node wrong', wrong)
  output = open(outputfolder + '/' + file + '.json', 'w')
  dataStr = json.dumps(out,  ensure_ascii=False)
  output.write(dataStr)
  inpt.close()
  output.close()


leafnumber = 0


# name = 'leijun'
# inputfolder = 'data/' + name
# outputfolder = 'dataTree/' + name
# if not os.path.exists(outputfolder):
#     os.mkdir(outputfolder)
# for root, dirs, files in os.walk(inputfolder):
#     for file in files:
#         if '.json' in file:
#             try:
#                 dealFile(file)
#             except Exception as e:
#                 print(e)
#

inputfolder = 'dataFull'
# outputfolder = '/server/process/dataTree'
outputfolder = '/Users/wakouboy/Projects/VueProjects/WeiboRepost/client/static/data'


# dealFile('nanxiaoqi.json')
# dealFile('qinshi.json')
# dealFile('leijun.json')
# dealFile('chunwan.json')
# dealFile('huhaiquan.json')
# dealFile('anbeijinsan.json')
# dealFile('liucixin.json')'''
# dealFile('liulangdiqiu.json')
# dealFile('qinghuafushi1.json')
# dealFile('qinghuafushi2.json')
# print(leafnumber)
