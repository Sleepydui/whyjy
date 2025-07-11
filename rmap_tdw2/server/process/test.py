import jieba
import requests
post_url = "http://api.pullword.com/post.php"

class ServerError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


def split_word(words):
  words = words.split()
  words_list = []
  for i in words:
    if len(i) == 0:
      continue
    words_list.append(i.decode().split(":"))
  return words_list


def pullword(source="", threshold=0, debug=1):
  payload = {"source": source.encode(
      "utf8"), "param1": threshold, "param2": debug}
  pw = requests.get(post_url, data=payload)
  if pw.status_code != 200:
    raise ServerError("server return %s" % pw.status_code)
  return split_word(pw.content)


text = '我喜欢你很久了'
word_list = pullword(text, threshold=0.7)

a = ""
