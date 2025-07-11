# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-12-20 21:22:42
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-06-02 22:42:34
# encoding: utf-8
import csv
import glob
import datetime
import json
import os
import requests

inputfolder = 'data'

outputfolder = '/Users/wakouboy/Projects/VueProjects/WeiboRepost/client/static/images'
def process(file):
  inpt = open(inputfolder + '/' + file + '.json', 'r')
  data = json.load(inpt)
  index = data['fields'].index('user_avatar')
  datalist = data['data']
  for item in datalist:
    url = item[index]
    print(url)
    uid = item[data['fields'].index('uid')]
    try:
      picture = requests.get(url)
      with open(outputfolder + '/' + str(uid) + '.jpg', 'wb') as f:
        f.write(picture.content)
    except Exception as e:
      print(e)

if __name__=='__main__':
  process('jiyinbianji')



