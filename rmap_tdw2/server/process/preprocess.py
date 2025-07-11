import os
import json


def process(filename):
  inputfolder = 'data'
  outputfolder = 'dataPre'
  fields = ['original_text', 'text', 't', 'username', 'city', 'province',
            'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
            'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count']
  if not os.path.exists(outputfolder):
    os.mkdir(outputfolder)
  print(filename)
  if filename:
    goFile(filename, inputfolder, outputfolder, fields)
  else:
    goFolder(inputfolder, outputfolder, fields)


def goFile(file, inputfolder, outputfolder, fields):
  root = ''
  inpt = open(inputfolder + '/' + file + '.json', 'r', encoding="utf8")
  inpt = json.load(inpt)
  data = inpt["data"]
  df = inpt["fields"]
  mids = []
  d = []

  data = sorted(data, key = lambda weibo: weibo[df.index('t')])
  # "original_text", "text", "t", "username", "city", "province", "gender", "verified", "verified_type", "verified_reason", "user_description", "friends_count", "statuses_count", "followers_count", "uid", "mid", "parent"
  # "id", "mid", "uid", "parent", "t", "reposts_count", "attitudes_count", "comments_count", "text", "original_text", "user_created_at", "followers_count", "bi_followers_count", "favourites_count", "statuses_count", "friends_count", "username", "screen_name", "user_description", "gender", "province", "city", "verified", "verified_reason", "verified_type", "user_location", "user_avatar", "user_geo_enabled", "picture", "geo"
  for node in data:
    original_text = node[df.index('original_text')]
    text = node[df.index('text')]
    t = node[df.index('t')]
    username = node[df.index('username')]
    city = node[df.index('city')]
    province = node[df.index('province')]
    gender = node[df.index('gender')]
    verified = node[df.index('verified')]
    verified_type = node[df.index('verified_type')]
    verified_reason = node[df.index('verified_reason')]
    user_description = node[df.index('user_description')]
    friends_count = node[df.index('friends_count')]
    statuses_count = node[df.index('statuses_count')]
    followers_count = node[df.index('followers_count')]
    uid = node[df.index('uid')]
    mid = node[df.index('mid')]
    parent = node[df.index('parent')]
    reposts_count = 0
    direct_reposts_count = 0
    if parent == None:
      parent = ""
    if parent != "" and parent not in mids:
      continue
    mids.append(mid)
    tmp = []
    tmp.append(original_text)
    tmp.append(text)
    tmp.append(t)
    tmp.append(username)
    tmp.append(city)
    tmp.append(province)
    tmp.append(gender)
    tmp.append(verified)
    tmp.append(verified_type)
    tmp.append(verified_reason)
    tmp.append(friends_count)
    tmp.append(statuses_count)
    tmp.append(followers_count)
    tmp.append(user_description)
    tmp.append(uid)
    tmp.append(mid) #15
    tmp.append(parent) #16
    tmp.append(reposts_count)
    tmp.append(direct_reposts_count)
    d.append(tmp)
  # print(df[15], df[16], df[17])
  map = {}
  for i in range(len(d)):
    map[d[i][15]] = i
  for i in range(len(d) - 1):
    node = d[len(d) - i - 1]
    if node[16] == '':
      continue
    d[map[node[16]]][17] = d[map[node[16]]][17] + node[17] + 1
    d[map[node[16]]][18] = d[map[node[16]]][18] + 1
  outputFileName = outputfolder + "/" + file + ".json"
  outputFile = open(outputFileName, "w")
  data = json.dumps({'fields': fields, 'data': d}, ensure_ascii=False)
  outputFile.write(data)
  outputFile.close()


def goFolder(inputfolder, outputfolder, fields):
  for root, dirs, files in os.walk(inputfolder):
    for file in files:
      root = ''
      inpt = open(inputfolder + '/' + file, 'r', encoding="utf8")
      data = json.load(inpt)["data"]
      mids = []
      d = []
      # tmp['original_text']=pdata[i]['text']
      # tmp['text']=pdata[i]['text'].split('//@')[0] #去掉第一个//@
      # tmp['t']=convert(pdata[i]['created_at'])
      # tmp['username']=pdata[i]['user']['name']
      # tmp['city']=int(pdata[i]['user']['city'])
      # tmp['province']=int(pdata[i]['user']['province'])
      # tmp['gender']=pdata[i]['user']['gender']
      # tmp['verified']=pdata[i]['user']['verified']
      # tmp['verified_type']=pdata[i]['user']['verified_type']
      # tmp['verified_reason']=pdata[i]['user']['verified_reason']
      # tmp['user_description']=pdata[i]['user']['description']
      # tmp['friends_count']=int(pdata[i]['user']['friends_count'])
      # tmp['statuses_count']=int(pdata[i]['user']['statuses_count'])
      # tmp['followers_count']=int(pdata[i]['user']['followers_count'])
      # tmp['uid']=str(pdata[i]['user']['id'])
      # tmp['mid']=str(pdata[i]['mid'])
      # tmp['parent']=str(pdata[i].get('pid',''))
      for node in data:
        original_text = node[9]
        text = node[8]
        t = node[4]
        username = node[16]
        city = node[21]
        province = node[20]
        gender = node[19]
        verified = node[22]
        verified_type = node[24]
        verified_reason = node[23]
        user_description = node[18]
        friends_count = node[15]
        statuses_count = node[14]
        followers_count = node[11]
        uid = node[2]
        mid = node[1]
        parent = node[3]
        reposts_count = 0
        direct_reposts_count = 0
        if parent == None:
          parent = ""
        if parent != "" and parent not in mids:
          continue
        mids.append(mid)
        tmp = []
        tmp.append(original_text)
        tmp.append(text)
        tmp.append(t)
        tmp.append(username)
        tmp.append(city)
        tmp.append(province)
        tmp.append(gender)
        tmp.append(verified)
        tmp.append(verified_type)
        tmp.append(verified_reason)
        tmp.append(user_description)
        tmp.append(friends_count)
        tmp.append(statuses_count)
        tmp.append(followers_count)
        tmp.append(uid)
        tmp.append(mid)
        tmp.append(parent)
        tmp.append(reposts_count)
        tmp.append(direct_reposts_count)

        d.append(tmp)

      map = {}

      for i in range(len(d)):
        map[d[i][15]] = i

      for i in range(len(d) - 1):
        node = d[len(d) - i - 1]
        d[map[node[16]]][17] = d[map[node[16]]][17] + node[17] + 1
        d[map[node[16]]][18] = d[map[node[16]]][18] + 1
      outputFileName = outputfolder + "/" + file
      outputFile = open(outputFileName, "w")
      data = json.dumps({'fields': fields, 'data': d},
                        outputFile, ensure_ascii=False)
      outputFile.write(data)
      outputFile.close()
