import os
import json
import requests
import time
from aip import AipNlp

APP_ID1 = '15501893'
API_KEY1 = 'QAbX8PV0Rxv164AGjeQa4abY'
SECRET_KEY1 = 'aMhFY94go7m6IkfMbmI5kzhRgW7x0PQQ'

APP_ID2 = '15553670'
API_KEY2 = 'MZn2GH9Z7C6I0yV2tQgaLBLK'
SECRET_KEY2 = 'GLxbT64zutkO4nWiuxaZGvD8I0n8L4I3'

APP_ID3 = '15553914'
API_KEY3 = 'QYDH5Y1Z84dD8kjcsVcVVECY'
SECRET_KEY3 = 'GW08UoBO7pMpdxaKKSkWzt6x1SieS08a'

APP_ID4 = '15555372'
API_KEY4 = 'Ovn4O7wmGQQSu3XeoFKwo7TS'
SECRET_KEY4 = 'WpiDFZL9r6LywjebNpGgQFOYKRRjXL0F'

APP_ID5 = '15555404'
API_KEY5 = 'igkho7kNYVU7tWFmmuejKGDZ'
SECRET_KEY5 = 'Ar8It9miQY6PBPRtvGflqgTAU9KEDOgK'

APP_ID6 = '15555407'
API_KEY6 = 'TGuwRDp1QGucxnSNTzsvNmvr'
SECRET_KEY6 = 'xkbY4ffzjmqaZwEKCURKCrrrxg0gG2Gr'
clients = [AipNlp(APP_ID1, API_KEY1, SECRET_KEY1), AipNlp(APP_ID2, API_KEY2, SECRET_KEY2), AipNlp(APP_ID3, API_KEY3, SECRET_KEY3), AipNlp(
    APP_ID4, API_KEY4, SECRET_KEY4), AipNlp(APP_ID5, API_KEY5, SECRET_KEY5), AipNlp(APP_ID6, API_KEY6, SECRET_KEY6)]

stop_words = ["", "转发微博", "转发", "轉發微博", "repost", "Repost"]


def process(filename):
  inputfolder = 'dataPre'
  outputfolder = 'dataPreSem'
  fields = ['original_text', 'text', 't', 'username', 'city', 'province',
            'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
            'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count',
            'sentiment', 'confidence', 'positive_prob']
  APP_ID = '15501893'
  API_KEY = 'QAbX8PV0Rxv164AGjeQa4abY'
  SECRET_KEY = 'aMhFY94go7m6IkfMbmI5kzhRgW7x0PQQ'
  client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

  if not os.path.exists(outputfolder):
    os.mkdir(outputfolder)
  if filename:
    goFile(filename, inputfolder, outputfolder, fields)
  else:
    goFolder(inputfolder, outputfolder, fields)


def goFile(file, inputfolder, outputfolder, fields):
  fileInfos = []
  cnt = 0
  it = 0
  root = ''
  inpt = open(inputfolder + '/' + file + '.json', 'r', encoding="utf-8")
  data = json.load(inpt)["data"]
  for i in range(len(data)):
    text = data[i][1].encode("gbk", "ignore").decode("gbk")
    if text in stop_words:
      data[i].append(0)
      data[i].append(1.0)
      data[i].append(0.5)
      continue
    r = 0
    while True:
      try:
        client = clients[it]
        it = (it + 1) % 6
        r = client.sentimentClassify(text)
        if r.__contains__("error_code"):
          if r["error_code"] == 282134:
            data[i].append(0)
            data[i].append(1.0)
            data[i].append(0.5)
            break
          if r["error_code"] == 18:
            continue
        data[i].append(r["items"][0]["sentiment"] - 1)
        data[i].append(r["items"][0]["confidence"])
        data[i].append(r["items"][0]["positive_prob"])
        cnt = cnt + 1
        break
      except Exception as e:
        print(e)
    if cnt % 200 == 0:
      print(cnt)
  outputFileName = outputfolder + "/" + file + ".json"
  outputFile = open(outputFileName, "w")
  dataStr = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
  outputFile.write(dataStr)
  outputFile.close()


def goFolder(inputfolder, outputfolder, fields):
  fileInfos = []
  cnt = 0
  it = 0
  for root, dirs, files in os.walk(inputfolder):
    for file in files:
      root = ''
      if os.path.isfile(outputfolder + "/" + file):
        print(file + " already exists")
        continue
      inpt = open(inputfolder + '/' + file, 'r', encoding="utf-8")
      data = json.load(inpt)["data"]
      for i in range(len(data)):
        text = data[i][1].encode("gbk", "ignore").decode("gbk")
        if text in stop_words:
          data[i].append(0)
          data[i].append(1.0)
          data[i].append(0.5)
          continue
        r = 0
        while True:
          try:
            client = clients[it]
            it = (it + 1) % 6
            r = client.sentimentClassify(text)
            if r.__contains__("error_code"):
              if r["error_code"] == 282134:
                data[i].append(0)
                data[i].append(1.0)
                data[i].append(0.5)
                break
              if r["error_code"] == 18:
                continue
            data[i].append(r["items"][0]["sentiment"] - 1)
            data[i].append(r["items"][0]["confidence"])
            data[i].append(r["items"][0]["positive_prob"])
            cnt = cnt + 1
            break
          except Exception as e:
            print(e)
        if cnt % 200 == 0:
          print(cnt)
      outputFileName = outputfolder + "/" + file
      outputFile = open(outputFileName, "w")
      json.dump({'fields': fields, 'data': data},
                outputFile, ensure_ascii=True)
      outputFile.close()
