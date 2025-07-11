# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import os
import json
stop_words = ["", "转发微博", "转发", "轉發微博", "repost", "Repost"]

credentials = service_account.Credentials.from_service_account_file("/Users/wakouboy/Documents/key/RMap.json")


client = language.LanguageServiceClient(credentials=credentials)

def get_sentiment(text):
  document = types.Document(
      content=text,
      type=enums.Document.Type.PLAIN_TEXT)
  # Detects the sentiment of the text
  val = client.analyze_sentiment(document=document).document_sentiment
  score = (val.score + 1) / 2
  confidence = val.magnitude
  sentiment = score
  # 0 - 1, 消极，中立，积极
  return [score, confidence, sentiment]

def process(filename):
  inputfolder = 'dataPre'
  outputfolder = 'dataPreSem'
  fields = ['original_text', 'text', 't', 'username', 'city', 'province',
            'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
            'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count',
            'sentiment', 'confidence', 'positive_prob']

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
      data[i].append(0.5)
      data[i].append(5)
      data[i].append(0.5)
      continue
    try:
      ans = get_sentiment(text)
      data[i].append(ans[0])
      data[i].append(ans[1])
      data[i].append(ans[2])
    except Exception as e:
      print(text)
      print(ans)
    cnt = cnt + 1
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




