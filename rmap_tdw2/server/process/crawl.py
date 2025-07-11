# coding=utf-8
import requests
import json
import time
import sys
import re
import random
import copy
import os
from datetime import datetime

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_decode(string, alphabet=ALPHABET):
  base = len(alphabet)
  strlen = len(string)
  num = 0
  idx = 0
  for char in string:
    power = (strlen - (idx + 1))
    num += alphabet.index(char) * (base ** power)
    idx += 1
  return num


def url_to_mid(url):
  url = str(url)[::-1]
  size = len(url) / 4 if len(url) % 4 == 0 else len(url) // 4 + 1
  result = []
  for i in range(size):
    s = url[i * 4: (i + 1) * 4][::-1]
    s = str(base62_decode(str(s)))
    s_len = len(s)
    if i < size - 1 and s_len < 7:
      s = (7 - s_len) * '0' + s
    result.append(s)
  result.reverse()
  return int(''.join(result))


def parse_url_suffix(url):
  pattern = re.compile(r'http.*/.*/(\w*)\??')
  match = pattern.match(url)
  if match:
    return match.groups()[0]
  else:
    print("Error: can not parse url", url)
  return ""


def convert(t):
  month = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  loc = t.find("+0800")
  t = t[0:loc]+t[loc+5:]
  nt = ''
  m = month.index(t[4:7])+1
  if m < 10:
    nt = str(0)+str(m)
  else:
    nt = str(m)
  for i in range(8, len(t)):
    if t[i] <= '9' and t[i] >= '0':
      nt += t[i]
  return int(time.mktime(time.strptime(nt, '%m%d%H%M%S%Y')))


fields = ['original_text', 'text', 't', 'username', 'city', 'province',
          'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
          'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'picture']


def extract(pdata):
  data = []
  # return pdata
  for i in range(len(pdata)):
    # tmp={}
    tmp = []
    try:
      # print(pdata[i])
      tmp.append(pdata[i]['text'])
      tmp.append(pdata[i]['text'].split('//@')[0])
      tmp.append(convert(pdata[i]['created_at']))
      tmp.append(pdata[i]['user']['name'])
      tmp.append(int(pdata[i]['user']['city']))
      tmp.append(int(pdata[i]['user']['province']))
      tmp.append(pdata[i]['user']['gender'])
      tmp.append(pdata[i]['user']['verified'])
      tmp.append(pdata[i]['user']['verified_type'])
      tmp.append(pdata[i]['user']['verified_reason'])
      tmp.append(pdata[i]['user']['description'])
      tmp.append(int(pdata[i]['user']['friends_count']))
      tmp.append(int(pdata[i]['user']['statuses_count']))
      tmp.append(int(pdata[i]['user']['followers_count']))
      tmp.append(str(pdata[i]['user']['id']))
      tmp.append(str(pdata[i]['mid']))
      tmp.append(str(pdata[i].get('pid', '')))
      tmp.append(str(pdata[i]['user']['avatar_large']))
    except Exception as e:
      print(e)
    data.append(tmp)

  return data


def single_query(url):
  # print(url)
  sys.stdout.flush()
  total_number = ''
  data = []
  queryTime = 0
  while True:
    tag = False
    try:
      queryTime = queryTime + 1
      response = requests.request("GET", url, timeout=3000)
      data = json.loads(response.text)
      total_number = data["total_number"]
      tag = True
    except Exception as e:
      tag = False
    if tag:
      break
    if queryTime > 5:
      break
  print("return total_number", total_number)
  print("len", len(data["reposts"]))
  return (total_number, data)


def crawl_original(mid):
  base_url = "http://162.105.92.147:18080/weibova/moapi/apiv2/statuses/show?"
  url = base_url + "id=" + str(mid)
  response = requests.request("GET", url, timeout=3000)
  print(response)
  data = json.loads(response.text)
  return data


def fix_data(data):
  pid = data[0]['mid']
  for i in range(1, len(data)):
    if data[i]['parent'] == '':
      data[i]['parent'] = pid
  data[0]['parent'] = ''

  return data


def crawl_repost(mid=0, url_suffix="", full_url="", folder_name="data/"):
  if mid == 0 and url_suffix == "" and full_url == "":
    print("Error: required params are empty")
  if url_suffix != "":
    mid = url_to_mid(url_suffix)
  if full_url != "":
    mid = url_to_mid(parse_url_suffix(full_url))
  # print parse_url_suffix(full_url)
  # print mid
  # mid='3946317799518331'
  base_url = "http://162.105.92.147:18080/weibova/moapi/apiv2/statuses/repost_timeline?count=100&"

  # base_url = "http://162.105.92.117:18080/weibova/moapi/apiv2/statuses/repost_timeline?count=100&";
  # base_url = "http://192.168.10.9:18080/weibova/moapi/apiv2/statuses/repost_timeline?count=100&";
  url = base_url + "id=" + str(mid) + "&"
  count_each_page = 100
  total_number = 1000000
  return_total_page = 0
  page = 1
  data = []
  flag = False

  try:
    data += extract([crawl_original(mid)])
  except Exception as e:
    print(e)
    print('mid wrong')
    return
  while (page - 1) * count_each_page <= total_number:
    time.sleep(random.random() * 10 + 1)
    try:
      # print single_query(url + "page=" + str(page)

      begin = datetime.now()
      return_total_number, page_data = single_query(url + "page=" + str(page))
      if page == 2:
        total_number = return_total_number
      simple_data = extract(page_data["reposts"])
      data += simple_data
      if len(data) > 2000000:
        with open(folder_name + str(page) + '.json', 'w') as f:
          json.dump(data, f, ensure_ascii=False)
          data = []
      print('time', (datetime.now() - begin).seconds)
      # print 'ss'
      # print len(page_data['reposts'])
    except Exception as e:
      print(e)
      print('while loop wrong')
      sys.stdout.flush()
      time.sleep(10)
    page += 1
    print(page)
  try:
    # data=sorted(data,key=lambda x: x['t'])
    # data=fix_data(data)
    global username
    outputFileName = folder_name + username + ".json"
    outputFile = open(outputFileName, "w")
    data = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
    outputFile.write(data)
    outputFile.close()
    print("Data is saved in", outputFileName)
  except Exception as e:
    print('write wrong')
    return
isOriginal = 0
root = {}
username = 'dama'
# https://weibo.com/1618051664/HxMv1yv0b?refer_flag=1001030103_ gaokaozuowen2
url = 'https://weibo.com/6567313061/Hx5nqdcb3?from=page_1005056567313061_profile&wvr=6&mod=weibotime'
if os.path.exists('data/' + username + '.json'):
    print('file exists')
else:
    crawl_repost(full_url = url, folder_name= 'data/')

 
# crawl_repost(url_suffix = "DixLhxl4b")
# fin=open("wujunlink",'r')
# lines=list(set(fin.readlinesMy
 
# for i,line in enumerate(lines):
#     print i
#     # print line
#     # if i<1185  :
#     #     continue
#     time.sleep(random.randint(10,20))
#     crawl_repost(full_url = line)
# crawl_repost(full_url =\
#     "http://weibo.com/1283022704/DjeHa3IvF?from=page_1005051283022704_profile&wvr=6&mod=weibotime")
#  200万条，10%
