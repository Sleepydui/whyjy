import os
import json
import jieba
import codecs

no_comments = ["", "转发微博", "转发", "轉發微博", "repost", "Repost"]


def process(filename):
  files = filename
  inputfolder = 'dataPreSemRelOp'
  outputfolder = 'dataFull'
  fields = ['original_text', 'text', 't', 'username', 'city', 'province',
            'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
            'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count',
            'sentiment', 'confidence', "positive_prob", "following_parent", "followed_by_parent", "oppose_parent", "words"]
  inpt = codecs.open("stop_words", "r", "utf-8")
  stop_words = [a.split('\n')[0] for a in inpt.readlines()]
  if not os.path.exists(outputfolder):
    os.mkdir(outputfolder)

  if filename:
    goFile(filename, inputfolder, outputfolder, fields, stop_words)


def goFile(file, inputfolder, outputfolder, fields, stop_words):
  inpt = open(inputfolder + '/' + file + '.json', 'r', encoding="utf8")
  data = json.load(inpt)["data"]
  '''oppose_count = 0
		followers_count = 0
		count = len(data)
		for i in range(len(data)):
			if data[i][fields.index("following_parent")]:
				followers_count += 1
			if data[i][fields.index("oppose_parent")]:
				oppose_count += 1

		print("following num: " + str(followers_count) + " / " + str(count))
		print("oppose num: " + str(oppose_count) + " / " + str(count))'''

  for i in range(len(data)):
    data[i].append([])
    text = data[i][fields.index("text")]
    if text in no_comments:
      continue
    t = jieba.cut(text)
    for w in t:
      w = w.strip()
      if w == "":
        continue
      if w not in stop_words:
        data[i][fields.index("words")].append(w)

  data[i][fields.index("words")] = list(set(data[i][fields.index("words")]))

  outputFileName = outputfolder + "/" + file + ".json"
  outputFile = open(outputFileName, "w")
  data = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
  outputFile.write(data)
  outputFile.close()
