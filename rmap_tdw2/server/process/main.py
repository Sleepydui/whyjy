import os
import preprocess
import semantics
import relation
import addSemantic
import addWords
import data2tree
import downloadImg

filename = 'nanxiaoqi'

preprocess.process(filename) # data中有新数据再进行
print('sentiment analysis')
semantics.process(filename) # 同上
# print('following relation')
# relation.process(filename)
# print('opinion')
# addSemantic.process(filename)
# print('keywords')
# addWords.process(filename)
# data2tree.process(filename)
# downloadImg.process(filename)