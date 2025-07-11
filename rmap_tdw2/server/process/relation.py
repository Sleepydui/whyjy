import os
import json
import time
import webbrowser
from sinaweibopy3 import APIClient


def authorize():
	APP_KEY = '1234287835'  # app key
	APP_SECRET = '26a6e726d169a90837d698e2fc46c078'  # app secret
	CALLBACK_URL = 'http://www.weibo.com'  # callback url

	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,
	                   redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()

	print(url)

	# webbrowser.open(url)
	code = input()
	# code = 'a0ade354a95094d799524aecbe074f7a'
	print('get code')
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,
	                   redirect_uri=CALLBACK_URL)
	r = client.request_access_token(code)
	access_token = r.access_token  # 新浪返回的token，类似abc123xyz456
	# token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
	expires_in = r.expires_in
	# TODO: 在此可保存access token
	client.set_access_token(access_token, expires_in)
	return client


'''files = ["3419504597841951", #nanxiaoqi
"4324721216003208", #qinshi
"4336027198186145", #anbeijinsan
"3461549869799578", #leijun
"4311349959956235", #huhaiquan
"4334624489033978", #chunwan
"4336997320073560", #liucixin
"4351272222363401", #qinghuafushi2
"4351275070032028" #qinghuafushi1
]'''


def process(filename):
	inputfolder = 'dataPreSem'
	outputfolder = 'dataPreSemRel'
	fields = ['original_text', 'text', 't', 'username', 'city', 'province',
'gender', 'verified', 'verified_type', 'verified_reason', 'user_description', 'friends_count',
'statuses_count', 'followers_count', 'uid', 'mid', 'parent', 'reposts_count', 'direct_reposts_count',
'sentiment', 'confidence', "positive_prob", "following_parent", "followed_by_parent"]
	if filename:
		goFile(filename, inputfolder, outputfolder, fields)
	else:
		goFolder(inputfolder, outputfolder, fields)


def goFile(file, inputfolder, outputfolder, fields):
	error_code = [10022, 10023, 10024, 21321]
	client = authorize()
	if not os.path.exists(outputfolder):
		os.mkdir(outputfolder)
	inpt = open(inputfolder + '/' + file + '.json', 'r', encoding="utf8")
	data = json.load(inpt)["data"]
	map = {}

	for i in range(len(data)):
		data[i].append(True)
		data[i].append(True)
		map[data[i][15]] = data[i][14]

	candidate = []
	for i in range(len(data)):
		candidate.append([i, data[i][fields.index("reposts_count")]])

	def takeSecond(elem):
		return elem[1]
	candidate.sort(key=takeSecond, reverse=True)

	for t in range(min(101, len(candidate))):
		i = candidate[t][0]
	# for i in range(len(data)):
		if data[i][16] == "":
			continue
		if data[i][fields.index("reposts_count")] == 0:
			continue
		while True:
			r = json.loads(client.friendships_show(data[i][14], map[data[i][16]]))
			if "error" in r:
				print(r["error"])
				if r["error_code"] not in error_code:
					break
				print(str(i) + " / " + str(len(data)))
				client = authorize()
				continue
			data[i][22] = r["source"]["following"]
			data[i][23] = r["source"]["followed_by"]
			break
	print(file + " done")
	outputFileName = outputfolder + "/" + file + ".json"
	outputFile = open(outputFileName, "w")
	dataStr = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
	outputFile.write(dataStr)
	outputFile.close()


def goFolder(inputfolder, outputfolder, fields):
	error_code = [10022, 10023, 10024, 21321]
	client = authorize()

	if not os.path.exists(outputfolder):
		os.mkdir(outputfolder)
	for fi in files:
		file = fi + ".json"
		if os.path.isfile(outputfolder + "/" + file):
			print(file + " already exists")
			continue
		inpt = open(inputfolder + '/' + file, 'r', encoding="utf8")
		data = json.load(inpt)["data"]

		map = {}

		for i in range(len(data)):
			data[i].append(True)
			data[i].append(True)
			map[data[i][15]] = data[i][14]

		candidate = []
		for i in range(len(data)):
			candidate.append([i, data[i][fields.index("reposts_count")]])
		def takeSecond(elem):
			return elem[1]
		candidate.sort(key=takeSecond, reverse=True)

		for t in range(min(101, len(candidate))):
			i = candidate[t][0]
		# for i in range(len(data)):
			if data[i][16] == "":
				continue
			if data[i][fields.index("reposts_count")] == 0:
				continue
			while True:
				r = json.loads(client.friendships_show(data[i][14], map[data[i][16]]))
				if "error" in r:
					print(r["error"])
					if r["error_code"] not in error_code:
						break
					print(str(i) + " / " + str(len(data)))
					client = authorize()
					continue
				data[i][22] = r["source"]["following"]
				data[i][23] = r["source"]["followed_by"]
				break
		print(file + " done")
		outputFileName = outputfolder + "/" + file
		outputFile = open(outputFileName, "w")
		dataStr = json.dumps({'fields': fields, 'data': data}, ensure_ascii=False)
		outputFile.write(dataStr)
		outputFile.close()
