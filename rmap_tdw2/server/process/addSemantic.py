import os
import json

stop_words = ["", "转发微博", "转发", "轉發微博", "repost", "Repost"]


def process(filename):
  inputfolder = 'dataPreSemRel'
  semanticfolder = 'semantic_mark/'
  outputfolder = 'dataPreSemRelOp'
  if not os.path.exists(outputfolder):
    os.mkdir(outputfolder)
  fields = ['original_text', 'text', 't', 'username', 'city', 'province',
            'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
            'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count',
            'sentiment', 'confidence', "positive_prob", "following_parent", "followed_by_parent", "oppose_parent"]
  if filename:
    goFile(filename, inputfolder, outputfolder, fields)


def goFile(file, inputfolder, outputfolder, fields):
  inpt = open(inputfolder + '/' + file + '.json', 'r', encoding="utf8")
  data = json.load(inpt)["data"]
  for i in range(len(data)):
    data[i].append(False)

  '''oppose_count = 0
		comments_count = 0
		followers_count = 0
		count = len(data)
		for i in range(len(data)):
			if data[i][fields.index("following_parent")]:
				followers_count = followers_count + 1

		print("following num: " + str(followers_count) + " / " + str(count))
		f = open(semanticfolder + "/" + fi + ".csv", 'rb')

		for i in range(len(data)):
			t = f.readline().decode("utf8", "ignore")
			if i == 0:
				data[i].append(False)
				continue
			t = t.split(',')
			mid = t[1].split("'")[1]
			if mid != data[i][15]:
				print(mid)
				print(data[i][15])
				print(i)
				print("error")
			s = int(t[len(t) - 1])
			if s == -1:
				data[i].append(True)
			else:
				data[i].append(False)

			if data[i][fields.index("oppose_parent")]:
				oppose_count = oppose_count + 1
			if data[i][fields.index("text")] not in stop_words:
				comments_count = comments_count + 1'''

  outputFileName = outputfolder + "/" + file + ".json"
  outputFile = open(outputFileName, "w")
  dataStr = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
  outputFile.write(dataStr)
  outputFile.close()
